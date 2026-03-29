# 10 Data Model Logical

## 主要エンティティ

| エンティティ | 概要 | 主な属性 |
|--------------|------|----------|
| post_candidate | 投稿候補 | candidate_id, source_type, content, scheduled_at, status |
| source_item | 収集情報 | source_item_id, source_provider, category, occurred_at, summary |
| anomaly_rule | アノマリー定義 | rule_id, rule_name, condition_definition, enabled |
| operation_log | 操作履歴 | log_id, candidate_id, operation_type, operator, operated_at |
| publication_history | 投稿履歴 | history_id, candidate_id, platform, result_status, published_at |
| platform_setting | 投稿先設定 | platform_id, platform_type, credential_ref, enabled |

## 関連
- source_item 1:N post_candidate
- anomaly_rule 1:N post_candidate
- post_candidate 1:N operation_log
- post_candidate 1:N publication_history
- platform_setting 1:N publication_history

## 状態定義
- post_candidate.status: draft / reserved / published / canceled / failed
- publication_history.result_status: success / retry / error

## 制約
- 投稿済みの post_candidate は更新不可。
- publication_history は投稿実行のたびに追加し、上書きしない。
- operation_log は更新・予約・投稿・キャンセルの各操作を必ず記録する。
