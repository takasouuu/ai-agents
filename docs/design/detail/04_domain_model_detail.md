# 04 Domain Model Detail

## エンティティ
- PostCandidate: 投稿候補本体
- OperationLog: 操作履歴
- PublicationHistory: 投稿履歴

## 値オブジェクト
- PostStatus(draft/reserved/published/canceled/failed)
- SourceType(news/event/anomaly)

## 状態遷移
- draft → reserved → published
- draft/reserved → canceled
- reserved/published 失敗時 → failed
