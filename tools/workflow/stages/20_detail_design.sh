#!/usr/bin/env bash
set -euo pipefail

echo "[detail-design] docs/design/detail を更新対象として確認"
test -d docs/design/detail
echo "[detail-design] HTML binding: docs/interface/html-php-binding.md"
