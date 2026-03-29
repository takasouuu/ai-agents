# 01 Architecture Layers

## レイヤ構成
- Presentation: 画面/HTTP入出力（REQ-010〜REQ-012）
- Application: ユースケース実行（REQ-004〜REQ-009）
- Domain: 投稿候補、履歴、状態遷移（REQ-002〜REQ-015）
- Infrastructure: DB/外部IF/投稿アダプタ

## 依存方向
- Presentation → Application → Domain
- Infrastructure は Domain/Application のIFを実装

## 禁止事項
- Presentation から Infrastructure 直接参照を禁止
- Domain から外部IF実装を直接参照しない
