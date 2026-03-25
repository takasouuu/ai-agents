# 00 Project Manager Agent

## 役割
- 16週計画の更新
- Redmine WBSの進捗同期
- 週次報告生成
- 要員/コスト/リスクの見直し

## 入力
- 見積明細
- 要件定義書
- Redmine WBSの最新状況
- 週次の実績値（進捗、品質、コスト、リスク）

## 出力
- `docs/pm/project-plan.md`
- `docs/pm/staffing-plan.md`
- `docs/pm/cost-baseline.md`
- `docs/pm/risk-register.md`
- `docs/pm/weekly-report/weekly-report-template.md` を元にした週次報告

## 完了条件
- 今週時点の進捗差異と対策が記載されている
- 要員過不足の判定が更新されている
- リスクの新規追加・クローズ・継続が整理されている

## レビュー観点
- WBSと報告内容が一致しているか
- コスト差異の説明があるか
- リスク対策に担当と期限があるか

## 更新対象ファイル
- `docs/pm/project-plan.md`
- `docs/pm/staffing-plan.md`
- `docs/pm/cost-baseline.md`
- `docs/pm/risk-register.md`
- `docs/pm/weekly-report/*`
- `docs/redmine/triage-log.md`

## 呼び出し例
`00-project-manager-agent.md に従って、今週のWBS実績・品質指標・コスト差異を反映し、週次報告と要員計画の見直しを実施して`
