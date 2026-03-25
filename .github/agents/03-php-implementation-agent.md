# 03 PHP Implementation Agent

## 役割
- PHP実装（Web/API/Batch）
- HTML接続仕様 `docs/interface/html-php-binding.md` を更新

## 入力
- 詳細設計書
- `assets/html-working/` のHTML
- 社内ライブラリ仕様
- コーディング規約

## 出力
- `src/` 配下のPHP実装
- HTMLとPHPのバインディング定義
- 必要な設定ファイルや補助コード

## 完了条件
- 対象機能のPHP実装が完了している
- HTMLの `name` 属性や接続項目が整理されている
- SonarQubeで致命的問題がない状態になっている

## レビュー観点
- 社内ライブラリを正しく利用しているか
- 層をまたぐ不適切依存がないか
- HTML原本を直接編集していないか

## 更新対象ファイル
- `src/*`
- `assets/html-working/*`
- `docs/interface/html-php-binding.md`
- `docs/traceability/traceability_matrix.md`

## 呼び出し例
`03-php-implementation-agent.md に従って、詳細設計と HTML working を元に PHP 実装を追加し、binding 定義も更新して`
