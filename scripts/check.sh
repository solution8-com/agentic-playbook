#!/usr/bin/env bash
# Run every structural check. Exits non-zero if any fails, so CI can call this one line.
set -uo pipefail
cd "$(dirname "$0")/.."

status=0
for check in scripts/check_manifest.py scripts/check_references.py; do
    python3 "$check" || status=1
done

exit $status
