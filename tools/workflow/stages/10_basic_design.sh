#!/usr/bin/env bash
set -euo pipefail

echo "[basic-design] docs/design/basic を更新対象として確認"
test -d docs/design/basic
echo "[basic-design] question backlog: docs/redmine/question-backlog.md"
