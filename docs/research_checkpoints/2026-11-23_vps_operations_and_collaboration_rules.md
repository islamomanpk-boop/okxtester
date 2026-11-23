# VPS Operations and Collaboration Rules — 2026-11-23

**Repository:** `islamomanpk-boop/okxtester`  
**Branch:** `price-action-v1`  
**Purpose:** Record the agreed division of work between ChatGPT, the user's Android/Termux environment, the VPS, and GitHub. These rules govern operations; they do not change the research roadmap or authorize new experiments.

## 1. Agreed division of work

- ChatGPT takes responsibility for planning, research prioritization, code writing/review, analysis, GitHub inspection and updates, documentation, and deciding the next safe step wherever the available tools allow it.
- The user does not need to manage routine planning, research organization, or code design. ChatGPT should do that work rather than repeatedly asking the user to make technical decisions.
- The user will use Android Termux to run computationally heavy jobs when needed. This includes large multi-asset pandas/numpy workloads, bootstrap/resampling, and memory-intensive statistical analysis.
- Keep the small 1 GB VPS for suitable lightweight tasks only when they are actually needed. Do not default to running heavy research on it.
- ChatGPT cannot directly operate the user's interactive Termux/SSH session from this chat. When a VPS command is necessary, ChatGPT must prepare one copy-paste-ready command at a time; the user runs it and shares the output.
- GitHub is the durable record for source code, methods, reports, decisions, and checkpoints.

## 2. Execution and communication

- Prefer ChatGPT-side GitHub/tool actions for work that can be completed safely through available integrations. Do not ask the user to perform actions that ChatGPT can complete and verify itself.
- Ask the user to run a command only when it requires access to their local Termux/phone or VPS shell, or when the needed capability is unavailable to ChatGPT.
- Give one copy-paste-ready command at a time, with a short explanation of purpose, expected resource use, and whether it changes anything.
- Before any computationally heavy task, estimate memory, CPU, disk, runtime, and output size, then direct it to Termux rather than the 1 GB VPS when appropriate.
- Never claim a command or GitHub update succeeded until its result has been returned or independently verified.
- Do not ask the user to share passwords, private SSH keys, exchange API secrets, or other credentials.
- If output indicates an error, stop and diagnose before proceeding.

## 3. Safety and change control

- Do not delete, truncate, overwrite, reset, clean, or move files unless the exact targets have been identified and the user has explicitly approved the operation.
- Preserve existing research data, reports, logs, archives, and untracked files. Never use broad destructive commands such as `git clean`, `rm -rf`, `git reset --hard`, or `git add .` as routine shortcuts.
- Do not uninstall or disable normal Ubuntu/DigitalOcean services as a cleanup shortcut.
- Do not change SSH authentication, firewall rules, swap, package versions, system services, or reboot the VPS without first explaining the reason, risk, rollback/safety checks, and obtaining user approval.
- Keep a recoverable backup before any approved destructive cleanup.
- Keep credentials out of GitHub, logs, screenshots, and chat.

## 4. Current VPS baseline (observed 2026-11-23)

- Ubuntu 24.04.5 LTS, x86_64; 1 vCPU; approximately 961 MiB RAM; 25 GB disk.
- At the latest memory check: 316 MiB RAM used, 644 MiB available, and no swap configured.
- Python 3.12 virtual environment at `/root/venv` (approximately 293 MB); preserve pending project review.
- Old bot archive at `/root/old_bots_archive/` (approximately 88 KB); preserve pending review and backup decision.
- Research archive at `/root/okx_research_project.zip` (approximately 62 MB); preserve.
- `/var/log` was reported at approximately 732 MB and needs read-only inspection before any cleanup.
- No active trading bot process, bot-specific systemd service, or root crontab was found in the inspections recorded before this document. Re-check before making any operational assumption.

This is a dated snapshot, not a guarantee of current system state.

## 5. Workload placement

**ChatGPT should handle directly where supported:**
- Research planning, roadmap/checklist review, source-code drafting and review, GitHub repository inspection, GitHub file creation/updates, documentation, and result interpretation.
- Small calculations and reasoning that do not require the user's machine or external execution.

**Use the user's Termux environment for heavy computation:**
- Large pandas/numpy workloads over multiple assets and timeframes.
- Large bootstrap/resampling jobs and memory-intensive statistical analyses.
- Any job likely to exceed the VPS's available RAM or cause swapping/OOM termination.

**Use the VPS only for suitable lightweight tasks when necessary:**
- Small Git operations, lightweight scripts, modest downloads, and basic server checks.
- Do not run heavy research on this 1 vCPU / 1 GB VPS by default.

Do not assume the phone has unlimited capacity either: estimate available phone resources and split/chunk computations if needed. If neither environment is suitable, redesign the computation in chunks or use a larger approved compute environment.

## 6. Research governance remains controlling

- Before any research task or experiment, inspect the current GitHub master checklist and detailed roadmap and confirm its priority.
- The research roadmap, not convenience or compute availability, determines what work is authorized.
- No new strategy backtests, exit sweeps, parameter optimization, or live-trading activity without explicit user approval and satisfaction of the relevant research gates.
- Preserve existing untracked reports and historical results; inspect before changing anything.
- Record material methods, decisions, results, failures, and next steps in dated GitHub checkpoints.
- After creating or updating a GitHub checkpoint, fetch it again and verify its content and commit before reporting it as saved.
- The immediate research gate recorded in the master checklist remains the corrected matched-breakout-controls implementation and exact 20/20 event-count reproduction. This operations document does not reorder or authorize research.

## 7. Immediate VPS housekeeping status

The next proposed action is read-only inspection of the largest files under `/var/log` and journal disk usage. No log cleanup has been authorized or performed. Review the output first, then propose any specific safe action separately.

---

**Status:** Updated operating rules; informational and procedural only. No VPS configuration or research data was changed by recording this document.
