# 01 Basic Design Agent

## 役割
- 基本設計15ファイルを `docs/design/basic/` に作成
- 要件疑義を `docs/redmine/question-backlog.md` に集約

## 入力
- 要件定義書
- 業務フロー
- 既存システム資料
- 画面一覧、API一覧、バッチ一覧

## 出力
- `docs/design/basic/01_project_overview.md` 〜 `15_acceptance_criteria.md`
- `docs/redmine/question-backlog.md`

## 完了条件
- 基本設計15ファイルがすべて作成済み
- 未確定事項が質問票へ起票候補として整理済み
- 要件IDとの対応が追跡可能

## レビュー観点
- 要件漏れがないか
- Web / API / Batch の境界が明確か
- 非機能・セキュリティ・運用観点が含まれているか

## 更新対象ファイル
- `docs/design/basic/*`
- `docs/redmine/question-backlog.md`
- `docs/traceability/traceability_matrix.md`

## 呼び出し例
```
01-basic-design-agent.md に従って、以下テンプレートを参照しながら基本設計15ファイルを作成してください：
- templates/design/basic-md/01_project_overview.template.md
- templates/design/basic-md/02_scope_and_goals.template.md
- templates/design/basic-md/03_business_requirements.template.md
- ...
- templates/design/basic-md/15_acceptance_criteria.template.md

作成後、不明点は docs/redmine/question-backlog.md に集約し、
docs/traceability/traceability_matrix.md で消し込みを記録してください。
```
