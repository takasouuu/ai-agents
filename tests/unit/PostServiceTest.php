<?php

declare(strict_types=1);

require_once __DIR__ . '/../../src/php-app/bootstrap.php';

use App\Application\PostService;
use App\Infrastructure\InMemoryPostRepository;

$service = new PostService(new InMemoryPostRepository());

$updated = $service->update(1, '更新後本文', '2026-03-30T09:00:00+09:00', 'メモ');
assert($updated['content'] === '更新後本文');

$reserved = $service->reserve(1, '2026-03-30T09:00:00+09:00');
assert($reserved['status'] === 'reserved');

$published = $service->publish(1);
assert($published['status'] === 'published');

echo "PostServiceTest passed" . PHP_EOL;
