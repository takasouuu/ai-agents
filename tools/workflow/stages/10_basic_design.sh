#!/usr/bin/env bash
set -euo pipefail

echo "[basic-design] docs/design/basic を更新対象として確認"
test -d docs/design/basic
echo "[basic-design] question backlog: docs/redmine/question-backlog.md"

echo ""
echo "[template list] 基本設計テンプレート："
ls -1 templates/design/basic-md/*.template.md 2>/dev/null | sed 's|.*/||' | sort
