#!/usr/bin/env bash
set -euo pipefail

echo "[detail-design] docs/design/detail を更新対象として確認"
test -d docs/design/detail
echo "[detail-design] HTML binding: docs/interface/html-php-binding.md"

echo ""
echo "[template list] 詳細設計テンプレート："
ls -1 templates/design/detail-md/*.template.md 2>/dev/null | sed 's|.*/||' | sort
