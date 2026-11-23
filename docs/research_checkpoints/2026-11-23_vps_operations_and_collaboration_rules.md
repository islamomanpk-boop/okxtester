# VPS Operations and Collaboration Rules — 2026-11-23

**Repository:** `islamomanpk-boop/okxtester`  
**Branch:** `price-action-v1`  
**Purpose:** Record the agreed division of work between ChatGPT, the user's Android/Termux environment, the VPS, and GitHub. These rules govern operations; they do not change the research roadmap or authorize new experiments.

## 1. Roles and access

- ChatGPT plans the work, reviews the research roadmap/checklist, writes and reviews scripts, explains commands, interprets outputs, and prepares research checkpoints.
- The user runs commands from Android Termux and shares their output. ChatGPT does not have direct interactive SSH control of the user's VPS in this chat and must not imply otherwise.
- The VPS is used for suitable lightweight or long-running tasks when its resources permit.
- Termux/on-device execution is preferred for tasks that exceed the VPS's available memory or CPU capacity, provided the phone can safely handle them.
- GitHub is the durable record for source code, methods, reports, decisions, and checkpoints.

## 2. Command delivery and execution

- Give the user one copy-paste-ready command at a time, with a short explanation of what it does and whether it changes anything.
- Prefer read-only inspection before any modification.
- Before a potentially heavy job, assess expected RAM, CPU, disk, runtime, and output size; choose VPS or Termux accordingly.
- Do not ask the user to share passwords, private SSH keys, exchange API secrets, or other credentials.
- Never claim a command succeeded until the user provides its output or a tool independently verifies the result.
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

**Usually suitable for the VPS (subject to a fresh resource check):**
- Git fetch/status/commit operations and small source-code checks.
- Lightweight scripts, small metadata checks, and modest downloads.
- Long-running jobs only when their memory and disk requirements are known and monitored.

**Usually better suited to Termux/on-device execution or another adequately sized compute environment:**
- Large pandas/numpy workloads over multiple assets and timeframes.
- Large bootstrap/resampling jobs and memory-intensive statistical analyses.
- Jobs likely to exceed the VPS's available RAM or cause swapping/OOM termination.

Do not assume Termux has unlimited capacity: estimate the phone's available resources too. If neither environment is suitable, redesign the computation in chunks or use a larger approved compute environment.

## 6. Research governance remains controlling

- Before any research task or experiment, inspect the current GitHub master checklist and detailed roadmap and confirm its priority.
- The research roadmap, not convenience or VPS availability, determines what work is authorized.
- No new strategy backtests, exit sweeps, parameter optimization, or live-trading activity without explicit user approval and satisfaction of the relevant research gates.
- Preserve existing untracked reports and historical results; inspect before changing anything.
- Record material methods, decisions, results, failures, and next steps in dated GitHub checkpoints.
- After creating or updating a GitHub checkpoint, fetch it again and verify its content and commit before reporting it as saved.
- The immediate research gate recorded in the master checklist remains the corrected matched-breakout-controls implementation and exact 20/20 event-count reproduction. This operations document does not reorder or authorize research.

## 7. Immediate VPS housekeeping status

The next proposed action is read-only inspection of the largest files under `/var/log` and journal disk usage. No log cleanup has been authorized or performed. Review the output first, then propose any specific safe action separately.

---

**Status:** Agreed operating rules; informational and procedural only. No VPS configuration or research data was changed by recording this document.
