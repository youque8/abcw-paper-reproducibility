#!/bin/sh
# Create a disposable isolated environment and run the complete verification.

set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON=${PYTHON:-python3}
TMP_BASE=${TMPDIR:-/tmp}
CLEAN_ROOT=$(mktemp -d "${TMP_BASE%/}/abcw-verify-clean-XXXXXX")
VENV="$CLEAN_ROOT/venv"

cleanup() {
    if [ "${ABCW_KEEP_CLEAN_ENV:-0}" = "1" ]; then
        printf '\nClean environment retained at: %s\n' "$CLEAN_ROOT"
    else
        rm -rf -- "$CLEAN_ROOT"
    fi
}
trap cleanup EXIT HUP INT TERM

printf 'ABCW clean-environment verification\n'
printf 'Repository: %s\n' "$ROOT"
printf 'Temporary environment: %s\n' "$CLEAN_ROOT"

"$PYTHON" -c '
import sys
if sys.version_info[:2] != (3, 12):
    raise SystemExit(
        f"CPython 3.12 is required; found {sys.version.split()[0]}. "
        "Set PYTHON=/path/to/python3.12 and retry."
    )
'

"$PYTHON" -m venv "$VENV"
VPY="$VENV/bin/python"

"$VPY" -c '
import pathlib, sys
cfg = pathlib.Path(sys.prefix) / "pyvenv.cfg"
text = cfg.read_text().lower()
assert sys.prefix != sys.base_prefix
assert "include-system-site-packages = false" in text
print("PASS isolation: new venv with system site-packages disabled")
'

"$VPY" -m pip install \
    --require-virtualenv \
    --disable-pip-version-check \
    -r "$ROOT/requirements-lock.txt"

"$VPY" -m pip check
"$VPY" "$ROOT/scripts/verify_full.py"

printf '\nPASS CLEAN ENVIRONMENT VERIFICATION\n'
