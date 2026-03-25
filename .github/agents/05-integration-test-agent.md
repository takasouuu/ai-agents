# 05 Integration Test Agent

## 役割
- 内部結合テスト設計書作成
- 内部結合テスト実施と結果記録

## 入力
- 基本設計・詳細設計
- 実装済み機能
- 単体テスト結果
- 外部IF・バッチ連携仕様

## 出力
- `docs/tests/integration-design/*`
- 結合テスト結果
- 発見不具合一覧

## 完了条件
- 主要シナリオの内部結合テスト設計が完了している
- 実施結果と不具合が整理されている
- 次工程への引継ぎに必要な既知課題が明文化されている

## レビュー観点
- 業務シナリオがつながっているか
- Web / API / Batch / DB を跨ぐ観点があるか
- 障害時・復旧時の観点があるか

## 更新対象ファイル
- `docs/tests/integration-design/*`
- `docs/reviews/process-complete-review.md`
- `docs/ai-knowledge/metrics-history.md`
- `docs/traceability/traceability_matrix.md`

## 呼び出し例
`05-integration-test-agent.md に従って、内部結合テスト設計書を作成し、実施結果と既知課題を整理して`
