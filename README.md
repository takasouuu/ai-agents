# AI Driven Development Sample (4 Months)

このサンプルは、立ち上げ〜内部結合テスト完了までを対象にした
プロジェクト運用テンプレートです。

## ポイント
- レビュー体制: AI（セルフ）/ AI→人1→人2（成果物・工程完了）
- HTML受領運用: `assets/html-received` と `assets/html-working` を分離
- 設計書正本: Markdown、提出形式: Word/Excel（`tools/doc-gen`）
- 品質/セキュリティ: SonarQube, CxSAST, BlackDuck, AppScan

## VS Code での使い方（イメージ）

### 1. モデル
- 推奨モデル: **GPT-5.3-Codex**
- 目的: 設計書生成、実装、テスト、レビュー証跡化を同一ワークスペースで進める

### 2. Agent の使い分け
- `00-project-manager-agent.md`: 計画、WBS、要員、コスト、週次報告
- `01-basic-design-agent.md`: 基本設計15ファイル作成
- `02-detail-design-agent.md`: 詳細設計15ファイル作成
- `03-php-implementation-agent.md`: PHP実装（Web/API/Batch）
- `04-unit-test-agent.md`: 単体テストと設計書同期
- `05-integration-test-agent.md`: 内部結合テスト設計・実施
- `06-review-trace-agent.md`: AI→人1→人2レビュー証跡
- `07-security-quality-agent.md`: Sonar/CxSAST/AppScan/BlackDuck統合判定

### 3. プロンプトの型
毎回、以下の5要素を入れて依頼する。

1. 対象Agent
2. 入力資料
3. 出力先
4. 完了条件
5. 更新対象ファイル

### 4. プロンプト例（コピペ用）

#### 基本設計
```text
01-basic-design-agent.md に従って、要件定義書を入力に基本設計15ファイルを docs/design/basic に作成してください。
未確定事項は docs/redmine/question-backlog.md に集約してください。
完了条件は、15ファイル作成済み・要件IDトレース可能・疑義集約済みです。
```

#### 詳細設計
```text
02-detail-design-agent.md に従って、docs/design/basic を入力に詳細設計15ファイルを docs/design/detail に作成してください。
HTML連携方針を docs/interface/html-php-binding.md に追記してください。
完了条件は、15ファイル作成済み・実装可能粒度・DDL/DML生成前提整理済みです。
```

#### 実装
```text
03-php-implementation-agent.md に従って、docs/design/detail と assets/html-working を入力に src を更新してください。
社内ライブラリ前提で実装し、binding 定義を docs/interface/html-php-binding.md に反映してください。
完了条件は、対象機能実装完了・HTML原本未編集・トレーサビリティ更新済みです。
```

#### 単体テスト
```text
04-unit-test-agent.md に従って、src の変更分に対応する単体テストを tests に追加してください。
docs/tests/unit-design も同期更新してください。
完了条件は、正常系/異常系の観点充足・実行結果記録・対応表更新済みです。
```

#### レビュー証跡
```text
06-review-trace-agent.md に従って、対象成果物のレビュー証跡を更新してください。
セルフレビューはAI、成果物レビューと工程完了レビューは AI→人1→人2 の流れで記録してください。
完了条件は、指摘ID採番済み・未解決事項整理済み・消し込み更新済みです。
```

### 5. ローカル Docker での実行
- ビルド:
```bash
docker compose -f docker/compose.workflow.yml build
```
- 全工程実行:
```bash
docker compose -f docker/compose.workflow.yml run --rm workflow-runner bash tools/workflow/run_workflow.sh all
```
- ログ監視:
```bash
tail -f .runtime/logs/workflow-*.log
```

### 6. 運用のコツ（コスト抑制）
- 1回で全工程を投げず、工程単位で依頼する
- 差分更新を明示し、再生成範囲を最小化する
- 週次で `docs/pm/premium-request-cost-plan.md` と `docs/pm/premium-request-usage-log.csv` を更新する
