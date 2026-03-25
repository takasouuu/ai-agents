# Local Docker Workflow Operations

## 方針
- GitLab Runner 未使用のため、ローカル Docker で工程ワークフローを実行する。
- 実行証跡は `.runtime/logs/` に保存し、レビュー時に参照する。

## 事前準備
1. Docker Desktop を起動する。
2. ワークスペースルートで以下を実行する。

```bash
docker compose -f docker/compose.workflow.yml build
```

## 実行方法

### 単工程実行
```bash
docker compose -f docker/compose.workflow.yml run --rm workflow-runner \
  bash tools/workflow/run_workflow.sh basic-design
```

### 全工程実行
```bash
docker compose -f docker/compose.workflow.yml run --rm workflow-runner \
  bash tools/workflow/run_workflow.sh all
```

## 監視方法
- 別ターミナルでログ追尾:

```bash
tail -f .runtime/logs/workflow-*.log
```

- Docker 実行状況確認:

```bash
docker ps -a | grep ai-dev-workflow-runner
```

## レビュー連携
- 実行後、`docs/reviews/` と `docs/pm/weekly-report/` に結果を転記する。
- 成果物レビュー・工程完了レビューは `AI -> 人1 -> 人2` で判定する。
