# 08 API External Spec

## API 一覧（REQ-005, REQ-007, REQ-008, REQ-009, REQ-010に対応）

### Workflow 実行（REQ-005）
- POST /api/workflow/execute
  - Request: { agent_name, workflow, input }
  - Response: { workflow_id, status, created_at, eta_sec }
  - Error: 400, 401, 503

### Workflow 状態取得（REQ-006）
- GET /api/workflow/{id}/status
  - Response: { workflow_id, status, progress, logs_url, updated_at }
  - Status: QUEUED / RUNNING / SUCCESS / FAILED / CANCELED

### 要件 CRUD（REQ-004）
- GET /api/requirements/list (filter, limit, offset)
- GET /api/requirements/{id}
- PUT /api/requirements/{id} (content, priority)
- Response: { id, content, priority, status, created_at, updated_at }

### トレーサビリティ（REQ-008）
- GET /api/traceability/matrix
  - Response: [ { requirement_id, design_id, impl_id, test_id, status } ]

### レビュー API（REQ-009）
- POST /api/reviews/create
  - Request: { artifact_type, artifact_id, review_type, findings }
- PUT /api/reviews/{id}/resolve
  - Request: { finding_id, status, resolution }

### Redmine 同期（REQ-007）
- POST /api/redmine/sync
  - Trigger: 毎工程完了後
  - Action: WBS更新、Triage log記録

## エラー仕様
| Code | 説明 | クライアント処理 |
|------|------|---------|
| 400 | Bad Request | リクエスト再確認 |
| 401 | Unauthorized | トークンリフレッシュ |
| 403 | Forbidden | 管理者に連絡 |
| 409 | Conflict | Retry (exponential backoff) |
| 500 | Internal Error | ログ送信、サポート連絡 |
| 503 | Unavailable | Client-side retry |

