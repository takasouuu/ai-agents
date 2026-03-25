# 単体テスト設計書 - テスト概要

## 概要
- **対象機能**: （例）ユーザー登録API、商品検索機能
- **対象ファイル**: `src/Domain/...`, `src/Application/...`
- **テスト方針**: 
  - 正常系・異常系・境界値テスト
  - 例外処理・ログ出力の確認
  - 外部依存は Mock/Stub でテスト隔離

## テストフレームワーク
- **使用ツール**: PHPUnit 10.x
- **実行方法**: `vendor/bin/phpunit tests/Unit/...`
- **カバレッジ目標**: 80% 以上（関数・行・条件カバレッジ）

## テスト対象範囲
| レイヤー | 対象 | テスト方法 |
|---------|------|----------|
| Domain Layer | Entity, Value Object | 状態遷移・不変条件 |
| Domain Layer | Service | ビジネスロジック |
| Application Layer | Service | Use Case 正常/異常系 |
| Infrastructure Layer | Repository | Mock での動作確認（実 DB は i-test で） |

## テストケース作成ルール
- テスト名: `testXxx*ShouldReturnYyyWhenZzzIsAaa` （Given-When-Then 形式）
- 1テストケース 1Assert 原則（複数の観点は複数ケースに分割）
- Setup/Teardown は共通化（Fixture/DataProvider 活用）

## 予定（スケジュール）
- テストケース設計: --年--月--日
- テストコード実装: --年--月--日
- テスト実行・結果確認: --年--月--日
- マージ予定日: --年--月--日

## 備考
- 社内ライブラリ利用時は内部動作を確認し、結果値検証に制限
- 外部API呼び出しは `HttpClientInterface` Mock で実施
- DB アクセスは RepositoryInterface Mock で隔離
