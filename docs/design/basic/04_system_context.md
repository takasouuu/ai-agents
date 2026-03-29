# 04 System Context

## システム境界

```
┌──────────────────────────────────────────────┐
│ AI Driven Development Workflow Platform      │
│ (このプロジェクト)                           │
├──────────────────────────────────────────────┤
│ ・エージェント実行エンジン                    │
│ ・ワークフローオーケストレーション           │
│ ・ログ・トレーサビリティ管理                 │
│ ・レビュー・品質ゲート判定                   │
└──────────────────────────────────────────────┘
       ↑                        ↓
     入力                      出力
┌──────────────────────────────────────────────┐
│ 外部システム・ツール                         │
├──────────────────────────────────────────────┤
│ • Redmine (WBS・課題管理) -- 双方向同期    │
│ • SonarQube (品質スキャン) -- 読取          │
│ • CxSAST/AppScan (セキュリティ) -- 読取    │
│ • BlackDuck (ライセンス) -- 読取            │
│ • GitHub/GitLab (リポジトリ) -- Push/Pull│
│ • ChatGPT/Claude (AI API) -- Call          │
│ • Docker (実行環境) -- Compose            │
└──────────────────────────────────────────────┘
```

## 外部インターフェース

| IF ID | 相手先 | 方向 | 内容 | 頻度 | フォーマット |
|-------|--------|------|------|------|-------------|
| IF-001 | Redmine | 双方向 | WBS進捗・質問票・Triage | 毎工程 | REST API |
| IF-002 | SonarQube | 入力 | 品質メトリクス | 毎回実装後 | REST API/JSON |
| IF-003 | GitHub | 双方向 | ソース管理・PR・マージ | 毎ステップ | Git/REST API |
| IF-004 | Chat GPT/Claude | 出力 | プロンプト実行 | 毎ステップ | REST API |
| IF-005 | Docker Registry | 入力 | イメージ取得・実行 | 初回建立 | Docker API |
| IF-006 | CxSAST/AppScan | 入力 | セキュリティ診断結果 | 品質ゲート時 | REST API/XML |

## 関連システム

### 入力
- **要件定義書**: users・外部から提供
- **Redmine**: 課題・WBS情報
- **HTML受領物**: `assets/html-received/`
- **既存ライブラリ**: 社内標準実装

### 出力
- **docs/design/basic**, **docs/design/detail**: テンプレート生成ドキュメント
- **src/**: PHP実装成果物
- **tests/**: テスト設計・実行結果
- **docs/reviews/**: レビュー証跡
- **docs/pm/weekly-report/**: 週次報告
