# 単体テストケース設計書

## テストケース一覧

### [機能名] テストケース群

#### TC-001: 正常系 - Xxxを入力して Yyy が返される
| 項目 | 内容 |
|------|------|
| テスト対象 | `src/Application/UserRegistration/RegisterUserService.php` |
| メソッド | `register(string $email): UserRegistrationResult` |
| 前提条件 | データベース初期化済み、外部API Mock 設定済み |
| 入力 | `email = "user@example.com"` |
| 期待結果 | 戻り値: `UserRegistrationResult` （ID 採番、status=PENDING） |
| テストコード | `testRegisterWithValidEmailShouldReturnPendingResult` |

#### TC-002: 異常系 - 重複メールアドレスでエラーが発生
| 項目 | 内容 |
|------|------|
| テスト対象 | `src/Application/UserRegistration/RegisterUserService.php` |
| メソッド | `register(string $email): UserRegistrationResult` |
| 前提条件 | 同じメールアドレスがDB に存在、外部API Mock 設定済み |
| 入力 | `email = "existing@example.com"` |
| 期待結果 | 例外発生: `DuplicateEmailException` |
| テストコード | `testRegisterWithDuplicateEmailShouldThrowException` |

#### TC-003: 境界値 - メールアドレスが最大長
| 項目 | 内容 |
|------|------|
| テスト対象 | `src/Application/UserRegistration/RegisterUserService.php` |
| メソッド | `register(string $email): UserRegistrationResult` |
| 前提条件 | 入力値バリデーション有効 |
| 入力 | `email = "a" * 244 + "@example.com"` （RFC5321: max 255） |
| 期待結果 | 正常に処理され、登録完了 |
| テストコード | `testRegisterWithMaxLengthEmailShouldSucceed` |

---

## テストコード実装例

```php
// tests/Unit/Application/UserRegistration/RegisterUserServiceTest.php

public function testRegisterWithValidEmailShouldReturnPendingResult()
{
    // Arrange
    $email = "user@example.com";
    $repositoryMock = $this->createMock(UserRepositoryInterface::class);
    $repositoryMock->expects($this->once())
        ->method('save')
        ->willReturn(true);
    
    $service = new RegisterUserService($repositoryMock);
    
    // Act
    $result = $service->register($email);
    
    // Assert
    $this->assertInstanceOf(UserRegistrationResult::class, $result);
    $this->assertEquals(UserRegistrationResult::STATUS_PENDING, $result->status());
    $this->assertNotNull($result->userId());
}
```

## テスト結果記録

| テストケースID | テスト名 | ステータス | 実行日 | 備考 |
|---------------|---------|-----------|-------|------|
| TC-001 | testRegister...ShouldReturnPendingResult | PASS | --年--月--日 | |
| TC-002 | testRegister...ShouldThrowException | PASS | --年--月--日 | |
| TC-003 | testRegisterWithMaxLengthEmail... | PASS | --年--月--日 | |

## サマリ
- テスト総数: 3
- PASS: 3
- FAIL: 0
- スキップ: 0
- カバレッジ: 85%
