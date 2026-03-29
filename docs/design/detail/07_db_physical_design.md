# 07 DB Physical Design

## テーブル
- post_candidates
- source_items
- anomaly_rules
- operation_logs
- publication_histories

## インデックス
- post_candidates(status, scheduled_at)
- publication_histories(candidate_id, published_at)

## 制約
- post_candidates.status は定義済み値のみ
- publication_histories は candidate_id 外部キー
