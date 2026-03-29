# 05 Usecase List

## Web ユースケース

| UC No | ユースケース名 | 要件ID | 完全性 | 優先度 |
|--------|---------------|--------|--------|--------|
| UC-W01 | プロジェクト基本情報をエディタで作成・更新 | REQ-004 | 〇 | M |
| UC-W02 | 基本設計15ファイルをテンプレートから展開 | REQ-004 | 〇 | M |
| UC-W03 | 実装コードをGitHubからPull・レビュー | REQ-005 | 〇 | M |
| UC-W04 | レビュー指摘を採番・追跡・マークアップ | REQ-009 | 〇 | M |
| UC-W05 | トレーサビリティマトリックスを閲覧・検索 | REQ-008 | ◎ | M |
| UC-W06 | 工程進捗・品質メトリクスをダッシュボード表示 | REQ-002 | ◎ | L |
| UC-W07 | ログ・実行履歴を検索・フィルタ | REQ-006 | 〇 | L |

## API ユースケース

| UC No | API エンドポイント | メソッド | 要件ID | 目的 |
|--------|------------------|----------|--------|------|
| UC-A01 | /api/workflow/execute | POST | REQ-005 | ワークフロー実行開始 |
| UC-A02 | /api/workflow/{id}/status | GET | REQ-006 | ワークフロー実行状態取得 |
| UC-A03 | /api/requirements/list | GET | REQ-004 | 要件一覧取得 |
| UC-A04 | /api/requirements/{id} | GET/PUT | REQ-004 | 要件詳細取得・更新 |
| UC-A05 | /api/traceability/matrix | GET | REQ-008 | トレーサビリティ参照 |
| UC-A06 | /api/reviews/create | POST | REQ-009 | レビュー指摘登録 |
| UC-A07 | /api/reviews/{id}/resolve | PUT | REQ-009 | レビュー指摘解決 |
| UC-A08 | /api/redmine/sync | POST | REQ-007 | Redmine同期 |

## バッチ処理

| Batch No | 名称 | 実行タイミング | 入力 | 出力 | 要件ID |
|----------|------|--------------|------|------|--------|
| BATCH-01 | ログアーカイブ | 日次 23:00 | .runtime/logs/ | 圧縮ファイル → S3 | REQ-006 |
| BATCH-02 | Redmine WBS同期 | 毎回工程完了時 | Redmine API | docs/redmine/triage-log.md | REQ-007 |
| BATCH-03 | トレーサビリティ更新 | 毎ステップ完了時 | 成果物ファイル群 | docs/traceability/matrix.md | REQ-008 |
| BATCH-04 | 品質ゲート判定 | テスト完了後 | SonarQube/CxSAST/AppScan | docs/reviews/process-complete-review.md | REQ-010 |
| BATCH-05 | 週次報告生成 | 毎週金曜 16:00 | metrics-history.md, risk-register.md | docs/pm/weekly-report/weekly-YYYY-WW.md | REQ-013 |
