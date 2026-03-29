# Unit Test Overview

## 対象
- src/php-app/app/Application/PostService.php
- src/php-app/app/Controller/PostController.php（主要分岐）

## 観点
| テストID | 観点 | 対応要件 |
|----------|------|----------|
| UT-001 | 投稿更新（正常） | REQ-005 |
| UT-002 | 投稿予約（正常） | REQ-004 |
| UT-003 | 即時投稿（正常） | REQ-006 |
| UT-004 | キャンセル（正常） | REQ-007 |
| UT-005 | 空本文更新（異常） | REQ-005 |
| UT-006 | 公開済み更新（異常） | REQ-005 |
| UT-007 | 公開済みキャンセル（異常） | REQ-007 |
| UT-008 | 対象なしID（異常） | REQ-004, REQ-005 |
| UT-009 | 一覧取得 | REQ-008, REQ-009 |
| UT-010 | 監査ログ出力 | REQ-014 |
