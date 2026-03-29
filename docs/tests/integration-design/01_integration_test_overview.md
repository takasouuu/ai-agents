# Integration Test Overview

## 対象シナリオ
| シナリオID | 内容 | 対応要件 |
|------------|------|----------|
| IT-001 | 投稿一覧表示→編集遷移 | REQ-008, REQ-009, REQ-010, REQ-011 |
| IT-002 | 編集→確認→予約確定 | REQ-004, REQ-005, REQ-012 |
| IT-003 | 編集→確認→即時投稿 | REQ-006, REQ-012 |
| IT-004 | 一覧から予約キャンセル | REQ-007, REQ-010 |
| IT-005 | バッチによる予約投稿実行 | REQ-013 |
| IT-006 | 操作履歴/投稿履歴追跡 | REQ-014, REQ-015 |

## 実施方式
- API連携: tests/integration/PostFlowIntegrationTest.php
- バッチ連携: src/php-app/app/Batch/RunReservedPostsBatch.php
