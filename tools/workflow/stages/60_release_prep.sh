#!/usr/bin/env bash
set -euo pipefail

echo "[release-prep] release docs を確認"
test -d docs/release
echo "[release-prep] doc-gen 実行"
python tools/doc-gen/run.py --mode preview
