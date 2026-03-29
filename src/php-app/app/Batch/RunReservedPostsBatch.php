<?php

declare(strict_types=1);

require_once __DIR__ . '/../../bootstrap.php';

use App\Application\PostService;
use App\Infrastructure\InMemoryPostRepository;

$service = new PostService(new InMemoryPostRepository());
$posts = $service->listPosts();

foreach ($posts as $post) {
    if ($post->status === 'reserved') {
        $service->publish($post->id);
    }
}

echo "reserved posts processed" . PHP_EOL;
