# Research Workflow and Results Archiving Rule

**Project rule — apply to every research study and every phase of OKX Price Action V1.**

## Required sequence

1. **Save the research code and workflow first.** Commit the analysis script, tests, and GitHub Actions workflow to the active project branch.
2. **Run the GitHub Actions workflow after saving.** Do not treat a committed workflow file as proof that the study ran. Confirm the run completed and inspect its job steps.
3. **Validate the outputs.** Check tests, row counts, data integrity, metadata, and any warnings or failures before accepting the results.
4. **Permanently archive important outputs in Git.** Commit final CSVs, summaries, diagnostics, and run metadata into the appropriate versioned directory under `reports/`. Update that directory's README with the study purpose, files, run/commit reference, interpretation, and limitations.
5. **Use Actions artifacts as a secondary convenience copy only.** Artifacts can expire; they must never be the only copy of important research results.
6. **Verify the archive commit.** Confirm the files are present on the project branch and can be fetched from GitHub. If a run fails, diagnose and rerun it; do not mark the study complete until the required checks pass.

## Research integrity

- Preserve scripts, tests, workflow definitions, and final outputs so a study can be reproduced.
- Record parameters, sample/cohort definitions, timestamps, data sources, software assumptions, and known limitations in metadata or the README.
- Do not overwrite earlier study versions; create a new versioned archive when methodology changes.
- Distinguish exploratory, observational evidence from causal conclusions or proof of a profitable trading strategy.
- Keep phase order and agreed research scope; do not advance to strategy selection before the current research phase is complete.

## Completion standard

A study is considered archived only when its code/workflow is committed, its workflow has been run and checked, and its important outputs and documentation are permanently committed to the repository. A temporary workflow artifact alone does not satisfy this rule.
