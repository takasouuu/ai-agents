# 11 External Integration Detail

## 外部連携
- SourceProviderAdapter: ニュース/イベント/指標取得
- SnsPublisherAdapter: 投稿送信

## タイムアウト/再試行
- タイムアウト: 10秒
- 再試行: 3回（指数バックオフ）

## エラー時挙動
- 連携失敗は運用通知
- failed状態で再実行候補へ登録
