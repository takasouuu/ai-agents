# Traceability Matrix

| 要件ID | 基本設計 | 詳細設計 | 実装 | 単体テスト | 内部結合テスト | レビュー指摘 | 状態 |
|--------|----------|----------|------|------------|----------------|--------------|------|
| REQ-001 | basic/01,11 | detail/01,03 | src/php-app/public/index.php | UT-009 | IT-001 | RV-001 | 完了 |
| REQ-002 | basic/03,04,09,10 | detail/04,10,11 | src/php-app/app/Batch/RunReservedPostsBatch.php | UT-009 | IT-005 | RV-002 | 完了 |
| REQ-003 | basic/03,04,09,10 | detail/04,10,11 | src/php-app/app/Batch/RunReservedPostsBatch.php | UT-009 | IT-005 | RV-002 | 完了 |
| REQ-004 | basic/05,06,07,08,09,15 | detail/05,08,10,12 | PostService::reserve | UT-002 | IT-002 | RV-003 | 完了 |
| REQ-005 | basic/05,06,07,08,15 | detail/05,08,09,12 | PostService::update | UT-001,UT-005,UT-006 | IT-001,IT-002 | RV-003 | 完了 |
| REQ-006 | basic/05,06,07,08,15 | detail/05,08,09,12 | PostService::publish | UT-003 | IT-003 | RV-003 | 完了 |
| REQ-007 | basic/05,06,08,13,15 | detail/05,08,12 | PostService::cancel | UT-004,UT-007 | IT-004 | RV-003 | 完了 |
| REQ-008 | basic/05,06,07,08,15 | detail/05,08,09 | PostController::GET /api/posts | UT-009 | IT-001 | RV-004 | 完了 |
| REQ-009 | basic/05,06,07,08,15 | detail/05,08,09 | PostController::GET /api/posts | UT-009 | IT-001 | RV-004 | 完了 |
| REQ-010 | basic/06,07,15 | detail/01,02 | assets/html-working/post-management.html | UT-009 | IT-001,IT-004 | RV-001 | 完了 |
| REQ-011 | basic/06,07,15 | detail/01,02,12 | assets/html-working/post-management.html | UT-001 | IT-001,IT-002 | RV-001 | 完了 |
| REQ-012 | basic/06,07,15 | detail/01,02,08 | assets/html-working/post-management.html | UT-002,UT-003 | IT-002,IT-003 | RV-001 | 完了 |
| REQ-013 | basic/09,11,14,15 | detail/10,11 | RunReservedPostsBatch | UT-002 | IT-005 | RV-005 | 完了 |
| REQ-014 | basic/08,10,11,12,14,15 | detail/13 | InternalLib\\AuditLogger | UT-010 | IT-006 | RV-005 | 完了 |
| REQ-015 | basic/08,10,11,12,14,15 | detail/04,07,13 | publication履歴設計 | UT-010 | IT-006 | RV-005 | 完了 |

## 備考
- 単体/内部結合テストはコード・設計・結果記録を更新済み
- 実行証跡はPHPランタイム整備後に再取得（Conditional Pass条件）
