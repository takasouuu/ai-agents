# 08 API External Spec

## API一覧

| API | Method | 用途 | 対応要件 |
|-----|--------|------|----------|
| /api/posts | GET | 投稿一覧取得 | REQ-008, REQ-009 |
| /api/posts/{id} | GET | 投稿候補詳細取得 | REQ-005 |
| /api/posts/{id} | PUT | 投稿候補更新 | REQ-005 |
| /api/posts/{id}/reserve | POST | 予約投稿確定 | REQ-004 |
| /api/posts/{id}/publish | POST | 即時投稿実行 | REQ-006 |
| /api/posts/{id}/cancel | POST | 予約キャンセル | REQ-007 |
| /api/histories/operations | GET | 操作履歴取得 | REQ-014 |
| /api/histories/publications | GET | 投稿履歴取得 | REQ-015 |

## 主要API仕様

### 1. 投稿一覧取得
- Method: GET
- Path: /api/posts
- Query: status, scheduled_from, scheduled_to, source_type
- Response:
  - posts[]: id, status, scheduled_at, source_type, content_summary, updated_at

### 2. 投稿候補更新
- Method: PUT
- Path: /api/posts/{id}
- Request:
  - content
  - scheduled_at
  - note
- Response:
  - id, status, content, scheduled_at, updated_at

### 3. 予約投稿確定
- Method: POST
- Path: /api/posts/{id}/reserve
- Request:
  - scheduled_at
- Response:
  - id, status=reserved, reserved_at

### 4. 即時投稿
- Method: POST
- Path: /api/posts/{id}/publish
- Request:
  - force_publish=true
- Response:
  - id, status=published, published_at, external_reference

### 5. 予約キャンセル
- Method: POST
- Path: /api/posts/{id}/cancel
- Request:
  - reason
- Response:
  - id, status=canceled, canceled_at

## 外部連携仕様
- 投稿実行時はSNS投稿アダプタを経由して送信する。
- 情報収集系IFはバッチから呼び出し、APIには候補生成済みデータのみ連携する。

## エラーコード
| Code | 意味 | 処理 |
|------|------|------|
| 400 | 入力不正 | 入力項目を再確認させる |
| 404 | 対象なし | 一覧へ戻して再検索させる |
| 409 | 状態競合 | 最新状態を再取得させる |
| 422 | 業務エラー | 予約時刻不正などを表示する |
| 500 | システムエラー | ログ採番し運用へ通知する |
| 503 | 外部連携失敗 | 再試行または手動対応へ誘導する |

