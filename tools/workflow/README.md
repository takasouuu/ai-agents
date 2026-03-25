# Local Workflow Runner

ローカル Docker 上で工程ワークフローを実行する。

## 目的
- GitLab Runner なしで、工程ごとの自動実行を再現する。
- 実行ログを可視化して、AIの実行状況を監視する。

## 実行例
- 全工程: `bash tools/workflow/run_workflow.sh all`
- 単工程: `bash tools/workflow/run_workflow.sh basic-design`

## 監視
- ログ保存先: `.runtime/logs/`
- 追尾表示: `tail -f .runtime/logs/workflow-*.log`
