# Copilot Instructions (Sample)

## プロジェクト境界
- 対象工程: 立ち上げ〜内部結合テスト完了（16週）
- 外部結合テスト・システムテスト: 別部隊が担当

## 必須ルール
- 言語は PHP、社内ライブラリ利用を必須化
- HTML は `assets/html-received/` を原本として扱い、編集は `assets/html-working/` のみ
- 設計書は Markdown を正本とし、Word/Excel は `tools/doc-gen` で生成

## レビュー体制
- セルフレビュー: AI
- 成果物レビュー: AI → 人(1人目) → 人(2人目)
- 工程完了レビュー: AI → 人(1人目) → 人(2人目)

## 品質ゲート
- MR前: SonarQube, CxSAST, BlackDuck, UIスモーク
- 内部結合前: 社内Webセキュリティチェックシート
- 結合環境: AppScan
