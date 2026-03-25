# note.com API リファレンス

note.comが内部で使用するWeb APIの仕様メモ。公式ドキュメントは非公開。

---

## 認証

| 方法 | ヘッダー | 値 |
|------|---------|-----|
| セッションCookie | `Cookie` | `note_session_v5=<value>` |
| APIトークン（利用可能な場合） | `Authorization` | `Bearer <token>` |

---

## ドラフト作成

### エンドポイント

```
POST https://note.com/api/v2/notes
```

### リクエストヘッダー

```
Content-Type: application/json
X-Requested-With: XMLHttpRequest
Cookie: note_session_v5=<value>
```

### リクエストボディ（JSON）

```json
{
  "title": "記事のタイトル",
  "body": "<p>本文のHTMLコンテンツ</p>",
  "type": "TextNote",
  "status": "draft",
  "hashtag_notes_attributes": [
    {"hashtag": {"name": "AI"}},
    {"hashtag": {"name": "GitHub Copilot"}}
  ]
}
```

### フィールド説明

| フィールド | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| `title` | string | ✅ | 記事タイトル（100文字以内推奨） |
| `body` | string | ✅ | HTML形式の本文 |
| `type` | string | ✅ | `"TextNote"` 固定 |
| `status` | string | ✅ | `"draft"` または `"published"` |
| `hashtag_notes_attributes` | array | ❌ | タグ（最大10個） |

### レスポンス例（成功）

```json
{
  "data": {
    "id": 12345678,
    "key": "n1a2b3c4d",
    "title": "記事タイトル",
    "status": "draft",
    "creator": {
      "urlname": "your_username"
    },
    "created_at": "2026-03-22T00:00:00.000Z"
  }
}
```

### 下書き確認URL

```
https://note.com/<urlname>/n/<key>
```

---

## 記事一覧取得（自分の下書き）

```
GET https://note.com/api/v2/creators/<urlname>/contents?kind=note&status=draft
```

---

## 注意事項

- note.comのAPIは公式には公開されていないため、仕様が変更される可能性がある
- HTMLは note.comのエディタが解釈できる形式である必要がある（TipTap互換）
- 画像のアップロードは別エンドポイントが必要（スクリプト非対応）
- 連続リクエストを短時間で多数送るとRateLimitが発生する可能性がある
