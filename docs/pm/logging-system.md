# ログシステム（チーム開発対応）

## 概要

`.runtime/logs/` はワークフロー実行時のログを**ホスト名・ユーザー名・日付別に分類**して保存するシステムです。プロンプト・AI 入出力・実行結果を一括記録により、チーム開発での実行追跡が可能になります。

## ディレクトリ構造

```
.runtime/logs/
├── {username}/                 # ユーザー名（例：takafumi）
│   ├── 2026-03-26/            # 実行日
│   │   ├── workflow-basic-design-20260326-060611.log
│   │   ├── workflow-basic-design-20260326-060611.metadata.json
│   │   ├── workflow-basic-design-20260326-060611.prompts.txt
│   │   ├── workflow-detail-design-20260326-080530.log
│   │   ├── workflow-detail-design-20260326-080530.metadata.json
│   │   ├── workflow-detail-design-20260326-080530.prompts.txt
│   │   └── ...
```

## ログファイル種類

### 1. **workflow-{stage}-{timestamp}.log**
- **通常の実行ログ**
- ステージビル・テンプレート一覧・エラーメッセージを記録
- 例：`[2026-03-26 06:06:11] START: tools/workflow/stages/10_basic_design.sh`

### 2. **workflow-{stage}-{timestamp}.metadata.json**
- **実行メタデータ**
- ホスト名・ユーザー名・ステージ・実行時刻・ファイルパスを記録
- チーム向けレポート生成の基盤
```json
{
  "stage": "basic-design",
  "hostname": "TakafuminoMacBook-Air.local",
  "username": "takafumi",
  "timestamp_start": "2026-03-25T21:06:16Z",
  "start_time": 1774472776,
  "log_file": "/.../workflow-basic-design-20260326-060616.log",
  "prompt_log": "/.../workflow-basic-design-20260326-060616.prompts.txt"
}
```

### 3. **workflow-{stage}-{timestamp}.prompts.txt**
- **プロンプト・AI入出力ログ**（将来拡張）
- 現在：ログヘッダー（実行情報）のみ
- 将来：Agent呼び出し時にプロンプト・応答を自動記録

## 使用方法

### ワークフロー実行

```bash
# 基本設計を実行
bash tools/workflow/run_workflow.sh basic-design

# 全工程を順序実行
bash tools/workflow/run_workflow.sh all
```

実行後、ログが自動的に以下に保存されます：
```
.runtime/logs/{hostname}/{username}/{YYYY-MM-DD}/
```

### ログの確認

```bash
# 本日のログ一覧
ls -la .runtime/logs/takafumi/2026-03-26/

# 特定ステージのログを確認
cat .runtime/logs/takafumi/2026-03-26/workflow-basic-design-*.log

# メタデータの確認（実行時刻・ホストなど）
cat .runtime/logs/takafumi/2026-03-26/workflow-basic-design-*.metadata.json
```

## チーム開発での活用

### マルチユーザー対応

各自が実行すると、ユーザー名ごとに自動的に分類されます：

```
.runtime/logs/
├── takafumi/2026-03-26/*.{log,metadata.json,prompts.txt}
├── hanako/2026-03-26/*.{log,metadata.json,prompts.txt}
├── jiro/2026-03-26/*.{log,metadata.json,prompts.txt}
```

**利点**：
- ✅ 各自のログが混在しない（ユーザー単位で分離）
- ✅ ホスト名はメタデータに記録されるため、追跡可能
- ✅ Git にコミットしない（`.gitignore` で無視）→ ローカル独立運用

### チーム向けレポート生成

将来実装予定：
```bash
# 過去7日間の全ユーザー・全マシンの実行統計
bash tools/workflow/log-util.sh generate-report 7

# 出力例：
# [TakafuminoMacBook-Air.local] takafumi - basic-design (12s)
# [TakafuminoMacBook-Air.local] takafumi - detail-design (45s)
# [OtherMac.local] hanako - unit-test (120s)
```

## Git 無視設定

`.gitignore` に以下が設定されているため、ローカルログはリポジトリに含まれません：

```
.runtime/logs/
```

## 今後の拡張機能

### 1. プロンプト自動記録
Agent呼び出し時に、以下を自動記録予定：
```bash
log_prompt "01-basic-design-agent" "要件定義を基に基本設計15ファイルを作成してください..."
log_ai_output "01-basic-design-agent" "基本設計ファイルを作成しました：01_project_overview.md 〜 15_acceptance_criteria.md"
```

### 2. チーム向けダッシュボード
ログを集約し、以下を可視化：
- 工程別実行時間の推移
- ユーザー別・マシン別の実行履歴
- エラー頻出箇所の自動検出

### 3. Performance Profile
ワークフロー実行の遅い部分を自動分析：
```
[Performance] detail-design took 45s
  - 30s: テンプレート参照＆読み込み
  - 12s: テンプレート展開（docs/design/detail へ出力）
  - 3s: メタデータ更新
```

## トラブルシューティング

### ログが作成されない場合

```bash
# 1. ディレクトリ権限を確認
ls -ld .runtime/logs/

# 2. log-util.sh が正しく読み込まれているか確認
bash -c 'source tools/workflow/log-util.sh && echo "OK"'

# 3. .gitignore に .runtime/logs がある確認
cat .gitignore | grep ".runtime/logs"
```

### メタデータが不完全な場合

```bash
# finalize_logging が実行されているか確認
cat .runtime/logs/.../workflow-*.metadata.json | grep "duration_seconds"
```

## 補足

- ログはテキスト形式のため、Git Diff で変更追跡可能です
- ローカル作業専用なため、Pull Request に含まれません
- 複数マシンでの同時実行時もファイル競合なし（ホスト名で分離）
