# 07 Screen Definition

## 画面定義（REQ-004, REQ-009に対応）

### SCR-02: ダッシュボード（REQ-002）
- 要件ID、要件内容、優先度フィールド
- バリデーション：優先度は H/M/L に限定

### SCR-03: 設計書編集画面（REQ-004）
- ファイルパス選択（テンプレート一覧から選択可）
- テキストエリア（Markdown編集）
- [保存] ボタン → PUT /api/requirements/{id}
- [プレビュー] ボタン → Markdown render

### SCR-05: レビュー一覧（REQ-009）
- テーブル：指摘ID、内容、状態（NEW/ACCEPTING/RESOLVED/CLOSED）、重要度
- フィルタ：状態別、重要度別
- [指摘選択] → SCR-06

### SCR-06: レビュー窓口（REQ-009）
- 指摘内容表示
- コメント入力欄
- [回答送信] ボタン → POST /api/reviews/create

## 項目定義

| Item ID | 項目名 | 型 | 必須 | バリデーション |
|---------|------|------|------|---------|
| priority | 優先度 | SELECT | Y | H/M/L |
| content | 内容 | TEXTAREA | Y | 5000文字以下 |
| status | 状態 | SELECT | Y | 定義値のみ |
| severity | 重要度 | SELECT | Y | H/M/L |

