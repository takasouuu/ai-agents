# 01 Project Overview

## 目的
- 株価に影響するニュース・イベント・指標情報を収集し、投稿候補として整理できるWebシステムを設計する。
- トレーダー向けの株価アノマリー情報を整理し、投稿候補として生成・予約・投稿できる仕組みを定義する。
- 投稿一覧、投稿編集、投稿確認の3画面と、API・バッチの責務分担を明確化する。

## 背景
- 要件定義では、投稿候補の自動生成と予約投稿、手動編集、即時投稿、履歴追跡が求められている。
- 投稿先プラットフォームや収集元が未確定のため、基本設計では差し替え可能な外部連携構成を採用する。
- 内部結合テスト完了までを対象とし、外部結合テストとシステムテストは別部隊で対応する。

## システム概要
- 利用者はWebブラウザから投稿候補を確認し、内容を修正し、予約または即時投稿を実行する。
- アプリケーションは外部情報収集、アノマリー生成、投稿予約実行をAPIとバッチで分担する。
- 操作履歴と投稿履歴は監査・障害調査・運用報告に利用できる形で保存する。

## 前提
- 実装言語はPHPとし、社内ライブラリを利用する。
- HTML原本は assets/html-received/ を参照し、作業用HTMLは assets/html-working/ を利用する。
- 設計書はMarkdownを正本とし、提出用のWord/Excelは別工程で生成する。

## 入力資料
- docs/requirements/requirements-definition.md

## 成果物
- docs/design/basic/01_project_overview.md 〜 15_acceptance_criteria.md
- docs/redmine/question-backlog.md
- docs/traceability/traceability_matrix.md
