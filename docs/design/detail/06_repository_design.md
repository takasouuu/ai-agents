# 06 Repository Design

## リポジトリIF
- PostCandidateRepository
- OperationLogRepository
- PublicationHistoryRepository

## 永続化方針
- 参照系はID・状態・日付条件で検索
- 更新系は楽観ロック相当（updated_at比較）
- 履歴系は追記専用
