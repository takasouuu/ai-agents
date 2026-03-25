#!/usr/bin/env bash
set -euo pipefail

echo "[implement] src 配下を確認"
test -d src
echo "[implement] HTML working 配下を確認"
test -d assets/html-working
