# 04 Unit Test Agent

## 役割
- 単体テストコードと単体テスト設計書の同期
- カバレッジと欠陥検出指標の更新

## 入力
- `src/` の実装コード
- 詳細設計書
- 単体テスト設計書テンプレート

## 出力
- `tests/` 配下の単体テスト
- `docs/tests/unit-design/unit_test_design_template.md` を元にした試験設計
- テスト実行結果サマリ

## 完了条件
- 対象機能の正常系・異常系テストが作成済み
- 設計書とテストコードの対応が明確
- 実行結果が記録されている

## レビュー観点
- 境界値・異常系が不足していないか
- テスト名と観点が一致しているか
- 自動実行可能な状態か

## 更新対象ファイル
- `tests/*`
- `docs/tests/unit-design/*`
- `docs/ai-knowledge/metrics-history.md`
- `docs/traceability/traceability_matrix.md`

## 呼び出し例
`04-unit-test-agent.md に従って、対象機能の単体テストと単体テスト設計書を更新し、テスト結果サマリも残して`
