#!/usr/bin/env bash
set -euo pipefail

STAGE="${1:-all}"
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

# ホスト名とユーザー名を検出
HOSTNAME="$(hostname)"
USERNAME="${USER:-$(whoami)}"
DATE="$(date +%Y-%m-%d)"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"

# ログディレクトリ階層: .runtime/logs/{hostname}/{username}/{date}/
LOG_BASE="$ROOT_DIR/.runtime/logs/$HOSTNAME/$USERNAME/$DATE"
LOG_FILE="$LOG_BASE/workflow-${STAGE}-${TIMESTAMP}.log"
METADATA_FILE="$LOG_BASE/workflow-${STAGE}-${TIMESTAMP}.metadata.json"
PROMPT_LOG="$LOG_BASE/workflow-${STAGE}-${TIMESTAMP}.prompts.txt"

mkdir -p "$LOG_BASE"

# メタデータファイルを作成
cat > "$METADATA_FILE" <<EOF
{
  "stage": "$STAGE",
  "hostname": "$HOSTNAME",
  "username": "$USERNAME",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "start_time": $(date +%s),
  "log_file": "$LOG_FILE",
  "prompt_log": "$PROMPT_LOG",
  "working_directory": "$ROOT_DIR"
}
EOF

log() {
  local message="$1"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $message" | tee -a "$LOG_FILE"
}

# プロンプトをログに記録する関数
log_prompt() {
  local agent="$1"
  local prompt="$2"
  cat >> "$PROMPT_LOG" <<EOF
================================================================================
$(date '+%Y-%m-%d %H:%M:%S') - Agent: $agent
================================================================================
$prompt

EOF
}

run_stage() {
  local script="$1"
  log "START: $script"
  bash "$ROOT_DIR/$script" 2>&1 | tee -a "$LOG_FILE"
  log "DONE : $script"
}

START_TIME=$(date +%s)
log "workflow stage=$STAGE user=$USERNAME host=$HOSTNAME"

case "$STAGE" in
  basic-design)
    run_stage "tools/workflow/stages/10_basic_design.sh"
    ;;
  detail-design)
    run_stage "tools/workflow/stages/20_detail_design.sh"
    ;;
  implement)
    run_stage "tools/workflow/stages/30_implement.sh"
    ;;
  unit-test)
    run_stage "tools/workflow/stages/40_unit_test.sh"
    ;;
  integration-test)
    run_stage "tools/workflow/stages/50_integration_test.sh"
    ;;
  release-prep)
    run_stage "tools/workflow/stages/60_release_prep.sh"
    ;;
  all)
    run_stage "tools/workflow/stages/10_basic_design.sh"
    run_stage "tools/workflow/stages/20_detail_design.sh"
    run_stage "tools/workflow/stages/30_implement.sh"
    run_stage "tools/workflow/stages/40_unit_test.sh"
    run_stage "tools/workflow/stages/50_integration_test.sh"
    run_stage "tools/workflow/stages/60_release_prep.sh"
    ;;
  *)
    echo "Unknown stage: $STAGE"
    echo "Use: basic-design | detail-design | implement | unit-test | integration-test | release-prep | all"
    exit 1
    ;;
esac

log "workflow completed"
