"""Sequential, resumable runner for the complete 66-experiment exit matrix."""

import argparse
import csv
import gc
from datetime import datetime, timezone
from pathlib import Path

from exit_experiment_config import build_experiment_matrix, validate_experiment_matrix
from run_exit_experiments import (
    load_inputs,
    run_one_experiment_with_inputs,
)


OUTPUT_RELATIVE = Path("okxtester/reports/exit_experiments")
MANIFEST_NAME = "exit_experiment_batch_manifest.csv"
COMPARISON_NAME = "exit_experiment_batch_comparison.csv"

# A run is complete only when every expected artifact from the single-run
# runner exists and the summary belongs to the expected experiment.
def expected_artifact_names(experiment_id):
    return (
        f"{experiment_id}_summary.csv",
        f"{experiment_id}_trades.csv",
        f"{experiment_id}_overall_metrics.csv",
        f"{experiment_id}_per_asset_metrics.csv",
        f"{experiment_id}_per_direction_metrics.csv",
        f"{experiment_id}_per_asset_direction_metrics.csv",
        f"{experiment_id}_daily_returns.csv",
        f"{experiment_id}_monthly_returns.csv",
        f"{experiment_id}_exit_reason_breakdown.csv",
        f"{experiment_id}_performance_report.md",
        f"{experiment_id}_report.md",
    )


def read_completed_summary(output_dir, experiment_id):
    """Return the saved summary only when all artifacts are present."""
    output_dir = Path(output_dir)
    for filename in expected_artifact_names(experiment_id):
        path = output_dir / filename
        if not path.is_file() or path.stat().st_size == 0:
            return None

    summary_path = output_dir / f"{experiment_id}_summary.csv"
    with summary_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    if len(rows) != 1 or rows[0].get("experiment_id") != experiment_id:
        return None
    return rows[0]


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


def _group_name(experiment):
    if experiment.trailing_mode == "trailing_stop_loss":
        return "trailing_stop_loss"
    if experiment.trailing_mode == "trailing_take_profit":
        return "trailing_take_profit"
    return "baseline"


def _atomic_write_csv(path, rows, fieldnames):
    """Replace a CSV atomically so an interruption cannot leave half a file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fieldnames, extrasaction="ignore"
        )
        writer.writeheader()
        writer.writerows(rows)
        handle.flush()
    temporary.replace(path)


def write_batch_manifest(output_dir, manifest_rows):
    fields = (
        "experiment_id", "group", "status",
        "started_utc", "completed_utc", "error",
    )
    _atomic_write_csv(
        Path(output_dir) / MANIFEST_NAME, manifest_rows, fields
    )


def write_batch_comparison(output_dir, summaries):
    if not summaries:
        return None
    fields = list(summaries[0])
    path = Path(output_dir) / COMPARISON_NAME
    _atomic_write_csv(path, summaries, fields)
    return path


def run_batch(
    experiments=None,
    home=None,
    rerun_completed=False,
    input_loader=None,
    experiment_runner=None,
):
    """Run experiments sequentially, checkpointing each completed result.

    Shared market data, funding data, and candidates are loaded once. Existing
    experiments are skipped only when all eleven expected output files and a
    matching one-row summary are present. A failed experiment stops the batch;
    earlier results remain saved and the next invocation can resume.
    """
    experiments = tuple(
        experiments if experiments is not None else build_experiment_matrix()
    )
    validate_experiment_matrix(experiments)

    home = Path(home) if home is not None else Path.home()
    output_dir = home / OUTPUT_RELATIVE
    output_dir.mkdir(parents=True, exist_ok=True)

    input_loader = input_loader or load_inputs
    experiment_runner = experiment_runner or run_one_experiment_with_inputs

    summaries = []
    manifest = []
    pending = []

    for experiment in experiments:
        saved = None if rerun_completed else read_completed_summary(
            output_dir, experiment.experiment_id
        )
        if saved is not None:
            summaries.append(saved)
            status = "completed"
        else:
            status = "pending"
            pending.append(experiment)

        manifest.append({
            "experiment_id": experiment.experiment_id,
            "group": _group_name(experiment),
            "status": status,
            "started_utc": "",
            "completed_utc": "",
            "error": "",
        })

    write_batch_manifest(output_dir, manifest)
    write_batch_comparison(output_dir, summaries)

    print(f"Experiment matrix: {len(experiments)}")
    print(f"Already complete and verified: {len(summaries)}")
    print(f"Remaining to run: {len(pending)}")
    print(f"Output directory: {output_dir}")

    if not pending:
        print("All 66 experiments already have complete, verified outputs.")
        return summaries

    print("\nLoading shared market, funding, and signal inputs once...")
    shared_inputs = input_loader()
    print(f"Shared inputs loaded. Running {len(pending)} experiments sequentially.")

    by_id = {item["experiment_id"]: item for item in manifest}

    for index, experiment in enumerate(pending, start=1):
        row = by_id[experiment.experiment_id]
        row["status"] = "running"
        row["started_utc"] = _utc_now()
        row["completed_utc"] = ""
        row["error"] = ""
        write_batch_manifest(output_dir, manifest)

        print(
            f"\n===== BATCH {index}/{len(pending)}: "
            f"{experiment.experiment_id} ====="
        )
        try:
            summary = experiment_runner(
                experiment, shared_inputs, home=home
            )
            if not isinstance(summary, dict):
                raise RuntimeError("Experiment runner did not return a summary")
            if summary.get("experiment_id") != experiment.experiment_id:
                raise RuntimeError("Returned summary has the wrong experiment_id")

            saved = read_completed_summary(output_dir, experiment.experiment_id)
            if saved is None:
                raise RuntimeError(
                    "Experiment returned, but one or more expected report "
                    "files are missing or the saved summary is invalid"
                )

            summaries = [
                item for item in summaries
                if item.get("experiment_id") != experiment.experiment_id
            ]
            summaries.append(saved)
            write_batch_comparison(output_dir, summaries)

            row["status"] = "completed"
            row["completed_utc"] = _utc_now()
            write_batch_manifest(output_dir, manifest)
            print(
                f"CHECKPOINT SAVED: {experiment.experiment_id} "
                f"({len(summaries)}/{len(experiments)} total complete)"
            )
        except Exception as exc:
            row["status"] = "failed"
            row["completed_utc"] = _utc_now()
            row["error"] = f"{type(exc).__name__}: {exc}"[:500]
            write_batch_manifest(output_dir, manifest)
            write_batch_comparison(output_dir, summaries)
            print(f"\nBATCH STOPPED at {experiment.experiment_id}")
            print(row["error"])
            print("Completed experiments are preserved. Run again to resume.")
            del shared_inputs
            gc.collect()
            return summaries

        gc.collect()

    del shared_inputs
    gc.collect()
    write_batch_comparison(output_dir, summaries)
    write_batch_manifest(output_dir, manifest)

    print("\n===== 66-EXPERIMENT BATCH COMPLETE =====")
    print(f"Completed summaries: {len(summaries)}")
    print(f"Comparison: {output_dir / COMPARISON_NAME}")
    print(f"Manifest: {output_dir / MANIFEST_NAME}")
    return summaries


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Run the 66 exit experiments sequentially with checkpoints."
    )
    parser.add_argument(
        "--list-experiments", action="store_true",
        help="List all 66 experiment IDs without loading data.",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Validate and summarize the matrix without running experiments.",
    )
    parser.add_argument(
        "--rerun-completed", action="store_true",
        help="Re-run even experiments whose complete outputs already exist.",
    )
    args = parser.parse_args(argv)

    experiments = build_experiment_matrix()
    validate_experiment_matrix(experiments)

    if args.list_experiments:
        for experiment in experiments:
            print(f"{_group_name(experiment)}\t{experiment.experiment_id}")
        return 0

    if args.dry_run:
        counts = {
            name: sum(_group_name(item) == name for item in experiments)
            for name in ("baseline", "trailing_stop_loss", "trailing_take_profit")
        }
        print(f"Total experiments: {len(experiments)}")
        for name, count in counts.items():
            print(f"{name}: {count}")
        print("Execution: sequential; shared inputs loaded once.")
        print("Checkpointing: after every completed experiment.")
        print("Resume: complete outputs are verified and skipped by default.")
        return 0

    summaries = run_batch(
        experiments=experiments,
        rerun_completed=args.rerun_completed,
    )
    return 0 if len(summaries) == len(experiments) else 1


if __name__ == "__main__":
    raise SystemExit(main())
