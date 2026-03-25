#!/usr/bin/env bash
set -euo pipefail

STAGE="${1:-all}"
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
LOG_DIR="$ROOT_DIR/.runtime/logs"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
LOG_FILE="$LOG_DIR/workflow-${STAGE}-${TIMESTAMP}.log"

mkdir -p "$LOG_DIR"

log() {
  local message="$1"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $message" | tee -a "$LOG_FILE"
}

run_stage() {
  local script="$1"
  log "START: $script"
  bash "$ROOT_DIR/$script" 2>&1 | tee -a "$LOG_FILE"
  log "DONE : $script"
}

log "workflow stage=$STAGE"

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
