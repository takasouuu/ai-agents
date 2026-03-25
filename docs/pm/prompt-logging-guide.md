# プロンプト記録ガイド

## 概要

Agent呼び出し時のプロンプトと出力を `.runtime/logs/{username}/{YYYY-MM-DD}/workflow-{stage}-{timestamp}.prompts.txt` に自動的に記録する方法を説明します。

## クイックスタート

### 1. VS Code での使用（推奨）

Agent呼び出し前に、VS Code 側で以下をコピーして実行：

```bash
# ターミナルで実行（ワークフロー開始時）
cd /Users/takafumi/projects/ai-agents
source tools/workflow/log-util.sh
init_logging "basic-design" "$(pwd)"

# このコマンドで以下の環境変数が設定される：
# - LOG_FILE: 実行ログファイル
# - PROMPT_LOG: プロンプト記録ファイル
# - METADATA_FILE: メタデータ
```

### 2. Agent呼び出し前にプロンプトを記録

VS Code Chat で Copilot に指示する前に、プロンプトをログに記録：

```bash
log_prompt "01-basic-design-agent" "要件定義を元に基本設計15ファイルを作成してください"
```

### 3. Agent実行後に出力を記録

```bash
log_ai_output "01-basic-design-agent" "基本設計15ファイルを docs/design/basic に作成しました"
```

## 実例

### 完全なワークフロー記録例

```bash
# ターミナル（Terminal 1: Logging）
cd /Users/takafumi/projects/ai-agents
source tools/workflow/log-util.sh
init_logging "basic-design" "$(pwd)"

# プロンプトを記録
log_prompt "01-basic-design-agent" "要件定義書を入力に、基本設計15ファイルを docs/design/basic に作成してください。
完了条件：
- 01_project_overview.md ～ 15_acceptance_criteria.md
- 要件IDとの対応が追跡可能
- 疑義は docs/redmine/question-backlog.md に集約"

echo "✓ Prompt logged to: $PROMPT_LOG"

# VS Code Chat (Terminal 2 or Copilot Panel)
# ユーザー: 01-basic-design-agent.md に従って、上記プロンプトでAgent実行

# ターミナルに戻る（Terminal 1）
log_ai_output "01-basic-design-agent" "基本設計15ファイルを以下に作成しました：
- docs/design/basic/01_project_overview.md
- docs/design/basic/02_scope_and_goals.md
- ...
- docs/design/basic/15_acceptance_criteria.md

全ファイルで要件IDを記載し、docs/traceability/traceability_matrix.md で対応付けしました。
疑義24件を docs/redmine/question-backlog.md に集約しました。"

echo "✓ Output logged"
```

## ログ確認

```bash
# プロンプトログの確認
cat .runtime/logs/takafumi/2026-03-26/workflow-basic-design-*.prompts.txt

# 出力例：
# ================================================================================
# Workflow Execution Log - Prompt & AI Output Record
# ================================================================================
# Hostname: TakafuminoMacBook-Air.local
# Username: takafumi
# Stage: basic-design
# Started: 2026-03-26 06:10:25
# ================================================================================
#
# ================================================================================
# Agent: 01-basic-design-agent
# Time: 2026-03-26 10:30:45
# ================================================================================
# PROMPT:
# 要件定義書を入力に...
#
# OUTPUT:
# 基本設計15ファイルを以下に作成しました：
# ...
```

## 関数リファレンス

### `log_prompt(agent_name, prompt_text)`

Agent呼び出し時のプロンプトをログに記録

**パラメータ**:
- `agent_name`: Agent定義ファイル名（例：`01-basic-design-agent`）
- `prompt_text`: 実際に入力するプロンプト

**例**:
```bash
log_prompt "01-basic-design-agent" "基本設計を作成..."
```

### `log_ai_output(agent_name, output_text)`

AI出力結果をログに記録

**パラメータ**:
- `agent_name`: Agent名（log_promptと同じ）
- `output_text`: Copilot からの出力結果（画面表示をコピペ）

**例**:
```bash
log_ai_output "01-basic-design-agent" "基本設計ファイルを作成しました..."
```

## チーム開発での活用

### 複数メンバーでプロンプト実績を追跡

各メンバーのプロンプトと出力は自動的に分離保存されます：

```
.runtime/logs/
├── takafumi/2026-03-26/
│   └── workflow-basic-design-20260326-*.prompts.txt
├── hanako/2026-03-26/
│   └── workflow-unit-test-20260326-*.prompts.txt
└── jiro/2026-03-26/
    └── workflow-detail-design-20260326-*.prompts.txt
```

### 実績集計（将来機能）

```bash
# 過去7日間の全プロンプト記録を確認
find .runtime/logs -name "*.prompts.txt" -mtime -7 -exec cat {} \;

# ユーザー別プロンプト統計
for user in $(ls .runtime/logs); do
  count=$(find .runtime/logs/$user -name "*.prompts.txt" -type f | wc -l)
  echo "$user: $count executions"
done
```

## トラブルシューティング

### プロンプトが記録されない場合

```bash
# 1. init_logging が実行されているか確認
echo "PROMPT_LOG=$PROMPT_LOG"

# 空の場合は以下をすぐに実行
source tools/workflow/log-util.sh
init_logging "basic-design" "$(pwd)"

# 2. ファイルが作成されているか確認
ls -la .runtime/logs/*/2026-03-26/*.prompts.txt

# 3. プロンプトを記録してみる
log_prompt "test" "テストプロンプト"

# 4. 内容確認
cat $PROMPT_LOG
```

## ベストプラクティス

1. **ワークフロー開始時に `init_logging` を必ず実行**
   ```bash
   source tools/workflow/log-util.sh
   init_logging "$(basename $0)" "$(pwd)"
   ```

2. **Agent呼び出し前に log_prompt を記録**
   - ユーザーが実際に入力したプロンプトをコピペ

3. **Agent実行後に log_ai_output を記録**
   - Copilot の出力結果を記録

4. **複数Agentを連続実行する際は各々記録**
   - 順序と依存関係が追跡不可になるため

5. **秘密情報は記録しない**
   - API キーやパスワード含まない
   - 個人情報も除外推奨
