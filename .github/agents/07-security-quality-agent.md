# 07 Security Quality Agent

## 役割
- SonarQube/CxSAST/AppScan/BlackDuckの結果集約
- 工程ゲート判定資料を作成

## 入力
- SonarQube結果
- CxSAST結果
- BlackDuck結果
- AppScan結果
- 社内Webセキュリティチェックシート結果

## 出力
- 品質/セキュリティ判定資料
- 残課題一覧
- 工程ゲート判定結果

## 完了条件
- 各ツール結果が集約されている
- High/Criticalの扱いが整理されている
- ゲート判定（Pass / Conditional Pass / Fail）が明示されている

## レビュー観点
- 結果の取りこぼしがないか
- 重大課題の是正期限があるか
- 工程境界に応じた判定になっているか

## 更新対象ファイル
- `docs/reviews/process-complete-review.md`
- `docs/pm/risk-register.md`
- `docs/ai-knowledge/metrics-history.md`
- `docs/release/release-checklist.md`

## 呼び出し例
`07-security-quality-agent.md に従って、品質/セキュリティ結果を集約し、工程ゲート判定資料を更新して`

