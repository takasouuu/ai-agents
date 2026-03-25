#!/usr/bin/env bash
set -euo pipefail

echo "[integration-test] integration design: docs/tests/integration-design"
test -d docs/tests/integration-design
echo "[integration-test] traceability: docs/traceability"
test -d docs/traceability
