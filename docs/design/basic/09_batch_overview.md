# 09 Batch Overview

## バッチ処理一覧（REQ-005, REQ-006, REQ-007, REQ-008, REQ-010）

| BATCH | 名称 | 実行タイミング | 入力 | 出力 |
|-------|------|----------------|------|------|
| BATCH-01 | ログアーカイブ | 日次 23:00 | `.runtime/logs/` | 圧縮ログ |
| BATCH-02 | Redmine WBS同期 | 各工程完了後 | Redmine API | `docs/redmine/triage-log.md` |
| BATCH-03 | トレーサビリティ更新 | 各ステップ完了後 | 成果物群 | `docs/traceability/traceability_matrix.md` |

## 失敗時ポリシー
- 最大3回までリトライ（5分→15分→30分）
- 失敗時は question backlog へ起票
