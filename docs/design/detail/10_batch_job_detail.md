# 10 Batch Job Detail

## ジョブ一覧
- CollectSourceJob（REQ-002）
- BuildAnomalyPostsJob（REQ-003）
- ExecuteReservedPostsJob（REQ-004, REQ-013）

## 処理手順
1. 対象取得
2. 業務検証
3. 投稿/保存処理
4. 履歴記録

## リトライ
- 外部連携失敗時は3回まで再試行
- 失敗継続時はfailed化して通知
