# 12 Validation Detail

## 入力検証
- content: 必須、空白のみ不可
- scheduled_at: ISO8601、未来時刻
- reason: キャンセル時必須

## 業務検証
- published状態は更新不可
- canceled状態は再キャンセル不可
- 予約時刻は営業日/運用制約に従う
