#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

cd "$HOME/okxtester"

BRANCH="price-action-v1"

if [[ "$(git branch --show-current)" != "$BRANCH" ]]; then
    echo "ERROR: Wrong branch. Expected $BRANCH"
    exit 1
fi

echo "===== STAGING PROJECT FILES ====="
git add -A -- src reports scripts README.md .gitignore

echo "===== CHECKING PATCH FORMAT ====="
git diff --cached --check

echo "===== CHECKING STAGED FILES FOR SECRETS ====="
python - <<'PY'
import subprocess
import re
import sys

files = subprocess.check_output(
    ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
    text=True
).splitlines()

patterns = [
    re.compile(r'(?i)(api[_-]?key|api[_-]?secret|access[_-]?token)\s*[:=]\s*["\'][^"\']{8,}'),
    re.compile(r'(?i)password\s*[:=]\s*["\'][^"\']{4,}'),
    re.compile(r'-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----'),
]

found = False

for filename in files:
    result = subprocess.run(
        ["git", "show", ":" + filename],
        capture_output=True
    )
    if result.returncode != 0 or b"\0" in result.stdout:
        continue

    content = result.stdout.decode("utf-8", errors="replace")

    for number, line in enumerate(content.splitlines(), 1):
        if any(pattern.search(line) for pattern in patterns):
            print(f"BLOCKED: Possible secret in {filename}, line {number}")
            found = True

if found:
    print("STOPPED: Nothing was committed or pushed.")
    sys.exit(1)

print("PASS: No obvious hardcoded credentials detected.")
PY

if git diff --cached --quiet; then
    echo "No new project changes to upload."
    exit 0
fi

echo "===== COMMITTING ====="
git commit -m "Update research code and reports"

echo "===== PUSHING TO GITHUB ====="
git push origin "$BRANCH"

echo "===== SYNC COMPLETE ====="
