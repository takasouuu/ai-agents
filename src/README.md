# src

PHPソースコード（Web/API/Batch）。

## 構成
- src/php-app/public/index.php: APIエントリポイント
- src/php-app/app/Controller/PostController.php: API制御
- src/php-app/app/Application/PostService.php: ユースケース実装
- src/php-app/app/Domain/PostCandidate.php: ドメインモデル
- src/php-app/app/Infrastructure/*: リポジトリ・社内ライブラリスタブ
- src/php-app/app/Batch/RunReservedPostsBatch.php: 予約投稿実行バッチ
