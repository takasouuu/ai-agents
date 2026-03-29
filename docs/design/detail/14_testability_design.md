# 14 Testability Design

## テスト容易化
- Service層はDIでリポジトリ/アダプタ差替可能
- 日時依存処理はClockインターフェース化

## モック方針
- SourceProviderAdapterは固定レスポンスモック
- SnsPublisherAdapterは送信成否を切替可能なスタブ

## 観点
- 正常系/異常系/境界値
- 状態遷移の一貫性
