#!/usr/bin/env bash
set -euo pipefail

STAGE="${1:-all}"
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

source "$ROOT_DIR/tools/workflow/log-util.sh"
init_logging "$STAGE" "$ROOT_DIR"

log_message "workflow stage=$STAGE user=$USERNAME_LOG"

if [[ -n "${COPILOT_AGENT:-}" || -n "${COPILOT_MODEL:-}" || -n "${COPILOT_PROMPT:-}" ]]; then
  log_chat_context "${COPILOT_AGENT:-unknown-agent}" "${COPILOT_MODEL:-unknown-model}" "${COPILOT_PROMPT:-}"
fi

if [[ -n "${COPILOT_OUTPUT:-}" ]]; then
  log_ai_output "${COPILOT_AGENT:-unknown-agent}" "${COPILOT_OUTPUT}"
fi

run_stage() {
  local script="$1"
  log_message "START: $script"
  bash "$ROOT_DIR/$script" 2>&1 | tee -a "$LOG_FILE"
  log_message "DONE : $script"
}

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

log_message "workflow completed"
finalize_logging "$STAGE" "$ROOT_DIR"
