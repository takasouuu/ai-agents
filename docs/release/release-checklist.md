# Release Checklist

## 工程完了時点（内部結合テスト完了）
| 項目 | 判定 | 備考 |
|------|------|------|
| 要件IDトレース可能 | OK | docs/traceability/traceability_matrix.md 参照 |
| レビュー証跡更新 | OK | AI→人1→人2 記録済み |
| SonarQube結果反映 | 条件付き | 実測未連携 |
| CxSAST結果反映 | 条件付き | 実測未連携 |
| AppScan結果反映 | 条件付き | 実測未連携 |
| BlackDuck結果反映 | 条件付き | 実測未連携 |
| 社内Webセキュリティチェックシート | OK | 設計レビューで確認 |

## 総合判定
- Conditional Pass
- 次工程開始前に上記「条件付き」項目の実測結果反映が必要
