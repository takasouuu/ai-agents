#!/usr/bin/env bash
set -euo pipefail

echo "[unit-test] tests 配下を確認"
test -d tests
echo "[unit-test] unit design: docs/tests/unit-design"
test -d docs/tests/unit-design

echo ""
echo "[template list] 単体テスト設計テンプレート："
ls -1 templates/tests/unit-design/*.template.* 2>/dev/null | sed 's|.*/||' | sort
