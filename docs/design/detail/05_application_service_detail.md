# 05 Application Service Detail

## サービス一覧
| サービス | 入力 | 出力 | 対応要件 |
|----------|------|------|----------|
| ListPostService | status, dateRange | posts[] | REQ-008, REQ-009 |
| UpdatePostService | id, content, scheduledAt, note | post | REQ-005 |
| ReservePostService | id, scheduledAt | reservedPost | REQ-004 |
| PublishPostService | id | publishedResult | REQ-006 |
| CancelPostService | id, reason | canceledPost | REQ-007 |

## 共通処理
- 権限チェック
- 操作履歴記録
- 例外標準化
