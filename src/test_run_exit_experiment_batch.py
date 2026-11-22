"""Tests for the resumable 66-experiment batch runner."""

import csv
from contextlib import redirect_stdout
import io
from pathlib import Path
import tempfile
import unittest

from exit_experiment_config import build_experiment_matrix
from run_exit_experiment_batch import (
    COMPARISON_NAME,
    MANIFEST_NAME,
    expected_artifact_names,
    read_completed_summary,
    run_batch,
)


def write_fake_experiment_outputs(home, experiment, summary):
    output_dir = (
        Path(home) / "okxtester/reports/exit_experiments_telemetry_v1"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    summary_path = output_dir / f"{experiment.experiment_id}_summary.csv"
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary))
        writer.writeheader()
        writer.writerow(summary)

    for filename in expected_artifact_names(experiment.experiment_id):
        path = output_dir / filename
        if path != summary_path:
            path.write_text("test output\n", encoding="utf-8")


class ExitExperimentBatchTests(unittest.TestCase):
    def test_matrix_contains_three_groups_of_22(self):
        matrix = build_experiment_matrix()
        self.assertEqual(len(matrix), 66)
        self.assertEqual(
            sum(item.trailing_mode == "none" for item in matrix), 22
        )
        self.assertEqual(
            sum(item.trailing_mode == "trailing_stop_loss" for item in matrix),
            22,
        )
        self.assertEqual(
            sum(item.trailing_mode == "trailing_take_profit" for item in matrix),
            22,
        )

    def test_expected_artifacts_include_all_eleven_files(self):
        names = expected_artifact_names("example")
        self.assertEqual(len(names), 11)
        self.assertIn("example_summary.csv", names)
        self.assertIn("example_trades.csv", names)
        self.assertIn("example_performance_report.md", names)
        self.assertIn("example_report.md", names)

    def test_resume_requires_every_artifact_and_matching_summary(self):
        experiment = build_experiment_matrix()[0]
        with tempfile.TemporaryDirectory() as folder:
            output_dir = Path(folder)
            summary = {
                "experiment_id": experiment.experiment_id,
                "final_equity": 123.0,
            }
            # Build outputs in the exact directory passed to the reader.
            for filename in expected_artifact_names(experiment.experiment_id):
                path = output_dir / filename
                if filename.endswith("_summary.csv"):
                    with path.open("w", newline="", encoding="utf-8") as handle:
                        writer = csv.DictWriter(handle, fieldnames=list(summary))
                        writer.writeheader()
                        writer.writerow(summary)
                else:
                    path.write_text("complete\n", encoding="utf-8")

            self.assertEqual(
                read_completed_summary(output_dir, experiment.experiment_id)[
                    "experiment_id"
                ],
                experiment.experiment_id,
            )
            (output_dir / expected_artifact_names(experiment.experiment_id)[3]).unlink()
            self.assertIsNone(
                read_completed_summary(output_dir, experiment.experiment_id)
            )

    def test_batch_loads_inputs_once_and_resumes_without_reloading(self):
        matrix = build_experiment_matrix()
        with tempfile.TemporaryDirectory() as folder:
            load_calls = []
            run_calls = []

            def loader():
                load_calls.append("loaded")
                return {"shared": "inputs"}

            def runner(experiment, shared_inputs, home=None):
                self.assertEqual(shared_inputs, {"shared": "inputs"})
                run_calls.append(experiment.experiment_id)
                summary = {
                    "experiment_id": experiment.experiment_id,
                    "final_equity": 1000.0,
                }
                write_fake_experiment_outputs(home, experiment, summary)
                return summary

            with redirect_stdout(io.StringIO()):
                first = run_batch(
                    experiments=matrix,
                    home=folder,
                    input_loader=loader,
                    experiment_runner=runner,
                )

            self.assertEqual(len(first), 66)
            self.assertEqual(len(load_calls), 1)
            self.assertEqual(len(run_calls), 66)

            run_calls.clear()
            with redirect_stdout(io.StringIO()):
                second = run_batch(
                    experiments=matrix,
                    home=folder,
                    input_loader=loader,
                    experiment_runner=runner,
                )

            self.assertEqual(len(second), 66)
            self.assertEqual(len(load_calls), 1)
            self.assertEqual(run_calls, [])

            output_dir = Path(folder) / "okxtester/reports/exit_experiments_telemetry_v1"
            self.assertTrue((output_dir / MANIFEST_NAME).is_file())
            self.assertTrue((output_dir / COMPARISON_NAME).is_file())
            with (output_dir / COMPARISON_NAME).open(
                newline="", encoding="utf-8"
            ) as handle:
                self.assertEqual(len(list(csv.DictReader(handle))), 66)

    def test_batch_stops_on_failure_and_preserves_prior_checkpoint(self):
        matrix = build_experiment_matrix()
        with tempfile.TemporaryDirectory() as folder:
            calls = []

            def runner(experiment, shared_inputs, home=None):
                calls.append(experiment.experiment_id)
                if len(calls) == 2:
                    raise RuntimeError("deliberate test failure")
                summary = {
                    "experiment_id": experiment.experiment_id,
                    "final_equity": 999.0,
                }
                write_fake_experiment_outputs(home, experiment, summary)
                return summary

            with redirect_stdout(io.StringIO()):
                first = run_batch(
                    experiments=matrix,
                    home=folder,
                    input_loader=lambda: object(),
                    experiment_runner=runner,
                )

            self.assertEqual(len(first), 1)
            self.assertEqual(len(calls), 2)

            resumed_calls = []

            def resume_runner(experiment, shared_inputs, home=None):
                resumed_calls.append(experiment.experiment_id)
                summary = {
                    "experiment_id": experiment.experiment_id,
                    "final_equity": 1000.0,
                }
                write_fake_experiment_outputs(home, experiment, summary)
                return summary

            with redirect_stdout(io.StringIO()):
                completed = run_batch(
                    experiments=matrix,
                    home=folder,
                    input_loader=lambda: object(),
                    experiment_runner=resume_runner,
                )

            self.assertEqual(len(completed), 66)
            self.assertEqual(len(resumed_calls), 65)
            self.assertNotIn(matrix[0].experiment_id, resumed_calls)


if __name__ == "__main__":
    unittest.main()
