<?php

declare(strict_types=1);

namespace App\Controller;

use App\Application\PostService;
use RuntimeException;

final class PostController
{
    public function __construct(private PostService $service)
    {
    }

    public function handle(string $method, string $path, array $body = []): array
    {
        try {
            if ($method === 'GET' && $path === '/api/posts') {
                return ['status' => 200, 'body' => ['posts' => $this->service->listPosts()]];
            }

            if ($method === 'PUT' && preg_match('#^/api/posts/(\d+)$#', $path, $m)) {
                return ['status' => 200, 'body' => $this->service->update((int) $m[1], (string) ($body['content'] ?? ''), $body['scheduled_at'] ?? null, $body['note'] ?? null)];
            }

            if ($method === 'POST' && preg_match('#^/api/posts/(\d+)/reserve$#', $path, $m)) {
                return ['status' => 200, 'body' => $this->service->reserve((int) $m[1], (string) ($body['scheduled_at'] ?? ''))];
            }

            if ($method === 'POST' && preg_match('#^/api/posts/(\d+)/publish$#', $path, $m)) {
                return ['status' => 200, 'body' => $this->service->publish((int) $m[1])];
            }

            if ($method === 'POST' && preg_match('#^/api/posts/(\d+)/cancel$#', $path, $m)) {
                return ['status' => 200, 'body' => $this->service->cancel((int) $m[1], (string) ($body['reason'] ?? ''))];
            }

            return ['status' => 404, 'body' => ['message' => 'not found']];
        } catch (RuntimeException $e) {
            return ['status' => 422, 'body' => ['message' => $e->getMessage()]];
        }
    }
}
