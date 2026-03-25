# 02 Detail Design Agent

## 役割
- 詳細設計15ファイルを `docs/design/detail/` に作成
- DDL/DMLテンプレ定義の整合性を確認

## 入力
- 基本設計一式
- HTML受領物
- 社内ライブラリ利用方針
- DB設計テンプレート

## 出力
- `docs/design/detail/01_architecture_layers.md` 〜 `15_migration_release_detail.md`
- DDL/DML生成対象の整理結果

## 完了条件
- 詳細設計15ファイルがすべて更新済み
- HTMLとのバインディング方針が反映済み
- DDL/DMLマクロ実行前提の定義が整っている

## レビュー観点
- クリーンアーキテクチャの責務分離があるか
- 実装・テストへ落とせる粒度か
- DB/API/Batch の例外処理方針が明記されているか

## 更新対象ファイル
- `docs/design/detail/*`
- `docs/interface/html-php-binding.md`
- `docs/db/generated/*`
- `docs/traceability/traceability_matrix.md`

## 呼び出し例
```
02-detail-design-agent.md に従って、以下テンプレートを参照しながら詳細設計15ファイルを作成してください：
- templates/design/detail-md/01_architecture_layers.template.md
- templates/design/detail-md/02_directory_structure.template.md
- templates/design/detail-md/03_php_coding_rules.template.md
- ...
- templates/design/detail-md/15_migration_release_detail.template.md

同時に以下を整理してください：
- HTML受領物（assets/html-received/）から作業コピー（assets/html-working/）へ展開
- docs/interface/html-php-binding.md で PHP バインディング方針を記載
- DDL/DML マクロの実行前提定義
- docs/traceability/traceability_matrix.md で基本設計と対応付け
```
