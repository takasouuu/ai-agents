# 09 Request Response Schema

## 更新APIリクエスト
```json
{
	"content": "投稿本文",
	"scheduled_at": "2026-03-30T09:00:00+09:00",
	"note": "補足"
}
```

## 一覧APIレスポンス
```json
{
	"posts": [
		{
			"id": 101,
			"status": "reserved",
			"scheduled_at": "2026-03-30T09:00:00+09:00",
			"content_summary": "..."
		}
	]
}
```
