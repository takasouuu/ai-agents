#!/usr/bin/env bash
set -euo pipefail

echo "[integration-test] integration design: docs/tests/integration-design"
test -d docs/tests/integration-design
echo "[integration-test] traceability: docs/traceability"
test -d docs/traceability

echo ""
echo "[template list] 統合テスト設計テンプレート："
ls -1 templates/tests/integration-design/*.template.* 2>/dev/null | sed 's|.*/||' | sort
