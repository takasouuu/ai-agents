#!/usr/bin/env bash
# ログユーティリティ関数
# チーム開発対応：ホスト名・ユーザー名で分類、プロンプト・AI出力記録

set -euo pipefail

# ディレクトリ構造: .runtime/logs/{hostname}/{username}/{YYYY-MM-DD}/
# ファイル構成:
#   - workflow-{stage}-{HHMMSS}.log         : 通常実行ログ
#   - workflow-{stage}-{HHMMSS}.metadata.json  : メタデータ（ホスト、ユーザー、実行時刻）
#   - workflow-{stage}-{HHMMSS}.prompts.txt    : プロンプト・AI入出力ログ

# 初期化（run_workflow.sh 開始時に呼ぶ）
init_logging() {
  local stage="$1"
  local root_dir="$2"
  
  # ホスト名とユーザー名を検出
  export HOSTNAME_LOG="$(hostname)"
  export USERNAME_LOG="${USER:-$(whoami)}"
  export DATE_LOG="$(date +%Y-%m-%d)"
  export TIMESTAMP_LOG="$(date +%Y%m%d-%H%M%S)"
  export START_TIME_LOG=$(date +%s)
  
  # ログディレクトリ作成（ホスト名フォルダは削除、ユーザー名フォルダ直下）
  export LOG_BASE="$root_dir/.runtime/logs/$USERNAME_LOG/$DATE_LOG"
  export LOG_FILE="$LOG_BASE/workflow-${stage}-${TIMESTAMP_LOG}.log"
  export METADATA_FILE="$LOG_BASE/workflow-${stage}-${TIMESTAMP_LOG}.metadata.json"
  export PROMPT_LOG="$LOG_BASE/workflow-${stage}-${TIMESTAMP_LOG}.prompts.txt"
  
  mkdir -p "$LOG_BASE"
  
  # メタデータファイルを作成
  cat > "$METADATA_FILE" <<EOF
{
  "stage": "$stage",
  "hostname": "$HOSTNAME_LOG",
  "username": "$USERNAME_LOG",
  "timestamp_start": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "start_time": $START_TIME_LOG,
  "log_file": "$LOG_FILE",
  "prompt_log": "$PROMPT_LOG",
  "working_directory": "$root_dir"
}
EOF

  # プロンプトログファイルのヘッダーを作成
  cat > "$PROMPT_LOG" <<EOF
================================================================================
Workflow Execution Log - Prompt & AI Output Record
================================================================================
Hostname: $HOSTNAME_LOG
Username: $USERNAME_LOG
Stage: $stage
Started: $(date '+%Y-%m-%d %H:%M:%S')
================================================================================

EOF
}

# ログ出力（通常ログ + タイムスタンプ）
log_message() {
  local message="$1"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $message" | tee -a "$LOG_FILE" 2>/dev/null || echo "[$(date '+%Y-%m-%d %H:%M:%S')] $message"
}

# プロンプト記録（Agent呼び出し時）
log_prompt() {
  local agent_name="$1"
  local prompt_text="$2"
  
  cat >> "$PROMPT_LOG" <<EOF
================================================================================
Agent: $agent_name
Time: $(date '+%Y-%m-%d %H:%M:%S')
================================================================================
PROMPT:
$prompt_text

EOF
}

# AI出力記録
log_ai_output() {
  local agent_name="$1"
  local output_text="$2"
  
  cat >> "$PROMPT_LOG" <<EOF
OUTPUT:
$output_text

EOF
}

# 完了時のメタデータ更新とサマリ表示
finalize_logging() {
  local end_time=$(date +%s)
  local duration=$((end_time - START_TIME_LOG))
  
  # メタデータを更新（終了時刻・所要時間）
  cat > "$METADATA_FILE" <<EOF
{
  "stage": "$1",
  "hostname": "$HOSTNAME_LOG",
  "username": "$USERNAME_LOG",
  "timestamp_start": "$(date -u -d @$START_TIME_LOG +%Y-%m-%dT%H:%M:%SZ)",
  "timestamp_end": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "start_time": $START_TIME_LOG,
  "end_time": $end_time,
  "duration_seconds": $duration,
  "log_file": "$LOG_FILE",
  "prompt_log": "$PROMPT_LOG",
  "working_directory": "${2:-.}"
}
EOF

  # サマリーを表示
  echo ""
  echo "╔════════════════════════════════════════════════════════════════╗"
  echo "║                      [Workflow Log Summary]                    ║"
  echo "╠════════════════════════════════════════════════════════════════╣"
  echo "║  Hostname:  $HOSTNAME_LOG"
  echo "║  Username:  $USERNAME_LOG"
  echo "║  Date:      $DATE_LOG"
  echo "║  Stage:     $1"
  echo "║  Duration:  ${duration}s"
  echo "║"
  echo "║  Log Files:"
  echo "║    - $LOG_FILE"
  echo "║    - $PROMPT_LOG"
  echo "║    - $METADATA_FILE"
  echo "╚════════════════════════════════════════════════════════════════╝"
  echo ""
}

# チーム向けログレポート生成（過去N日間のログを集計）
generate_team_report() {
  local root_dir="${1:-.}"
  local days="${2:-7}"
  local log_base="$root_dir/.runtime/logs"
  
  echo "Team Workflow Execution Report (Last $days days)"
  echo "=================================================================="
  echo ""
  
  # 全ユーザー・全ホストのログを検索
  find "$log_base" -name "workflow-*.metadata.json" -type f -mtime -$days 2>/dev/null | while read metadata_file; do
    if [ -f "$metadata_file" ]; then
      # JSON パースで情報取得
      local hostname=$(grep '"hostname"' "$metadata_file" | cut -d'"' -f4)
      local username=$(grep '"username"' "$metadata_file" | cut -d'"' -f4)
      local stage=$(grep '"stage"' "$metadata_file" | cut -d'"' -f4)
      local duration=$(grep '"duration_seconds"' "$metadata_file" | cut -d':' -f2 | cut -d',' -f1)
      
      echo "  [$hostname] $username - $stage (${duration:-N/A}s)"
    fi
  done
  
  echo ""
  echo "Total log entries: $(find "$log_base" -name "workflow-*.log" -type f -mtime -$days 2>/dev/null | wc -l)"
}

# エクスポート関数
export -f log_message
export -f log_prompt
export -f log_ai_output
export -f init_logging
export -f finalize_logging
export -f generate_team_report
