# 08 API Endpoint Detail

## エンドポイント
- GET /api/posts
- GET /api/posts/{id}
- PUT /api/posts/{id}
- POST /api/posts/{id}/reserve
- POST /api/posts/{id}/publish
- POST /api/posts/{id}/cancel

## バリデーション
- content: 必須、上限文字数
- scheduled_at: 未来日時
- reason: キャンセル時必須
