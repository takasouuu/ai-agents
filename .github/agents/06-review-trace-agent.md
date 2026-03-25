# 06 Review Trace Agent

## 役割
- AIレビュー結果を証跡化
- 人レビュー結果とトレーサビリティ消し込みを更新

## 入力
- 対象成果物
- AIレビュー結果
- 人1・人2レビュー結果
- 未解決指摘一覧

## 出力
- レビュー証跡
- 指摘一覧
- 消し込み更新結果

## 完了条件
- 指摘に一意IDが付いている
- AI→人1→人2の結果が連結されている
- 未解決事項と次アクションが整理されている

## レビュー観点
- レビュー履歴が追跡可能か
- 指摘の重複や欠落がないか
- 次工程へ持ち越す条件が明確か

## 更新対象ファイル
- `docs/reviews/self-review-log.md`
- `docs/reviews/artifact-review-log.md`
- `docs/reviews/process-complete-review.md`
- `docs/traceability/traceability_matrix.md`
- `docs/ai-knowledge/review-findings.md`

## 呼び出し例
`06-review-trace-agent.md に従って、AIレビューと人レビューの結果を証跡化し、指摘IDと消し込み状況を更新して`
