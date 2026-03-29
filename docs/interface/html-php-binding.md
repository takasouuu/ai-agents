# HTML PHP Binding

## 原本/作業コピー方針
- 原本参照: assets/html-received/
- 編集対象: assets/html-working/
- 本工程では作業HTMLを `assets/html-working/post-management.html` に配置

## バインディング定義
| 画面 | HTML name属性 | PHPリクエスト項目 | API |
|------|---------------|-------------------|-----|
| 投稿一覧 | status_filter | status | GET /api/posts |
| 投稿一覧 | scheduled_from | scheduled_from | GET /api/posts |
| 投稿一覧 | scheduled_to | scheduled_to | GET /api/posts |
| 投稿編集 | post_id | id | GET /api/posts/{id} |
| 投稿編集 | content | content | PUT /api/posts/{id} |
| 投稿編集 | scheduled_at | scheduled_at | PUT /api/posts/{id} |
| 投稿編集 | note | note | PUT /api/posts/{id} |
| 投稿確認 | publish_mode | force_publish | POST /api/posts/{id}/publish |
| 投稿確認 | reserve_at | scheduled_at | POST /api/posts/{id}/reserve |
| 投稿一覧 | cancel_reason | reason | POST /api/posts/{id}/cancel |

## DTO対応
- `PostUpdateRequest`: content, scheduledAt, note
- `ReservePostRequest`: scheduledAt
- `PublishPostRequest`: forcePublish
- `CancelPostRequest`: reason
