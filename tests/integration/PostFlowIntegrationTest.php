<?php

declare(strict_types=1);

require_once __DIR__ . '/../../src/php-app/bootstrap.php';

use App\Application\PostService;
use App\Controller\PostController;
use App\Infrastructure\InMemoryPostRepository;

$controller = new PostController(new PostService(new InMemoryPostRepository()));

$list = $controller->handle('GET', '/api/posts');
assert($list['status'] === 200);

$update = $controller->handle('PUT', '/api/posts/1', [
    'content' => '内部結合テスト更新',
    'scheduled_at' => '2026-03-30T10:00:00+09:00',
    'note' => 'integration'
]);
assert($update['status'] === 200);

$reserve = $controller->handle('POST', '/api/posts/1/reserve', ['scheduled_at' => '2026-03-30T10:00:00+09:00']);
assert($reserve['status'] === 200);

$publish = $controller->handle('POST', '/api/posts/1/publish');
assert($publish['status'] === 200);

echo "PostFlowIntegrationTest passed" . PHP_EOL;
