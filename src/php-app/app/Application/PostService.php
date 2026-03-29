<?php

declare(strict_types=1);

namespace App\Application;

use App\Infrastructure\InMemoryPostRepository;
use InternalLib\AuditLogger;
use RuntimeException;

final class PostService
{
    public function __construct(private InMemoryPostRepository $repository)
    {
    }

    public function listPosts(): array
    {
        return $this->repository->all();
    }

    public function update(int $id, string $content, ?string $scheduledAt, ?string $note): array
    {
        $post = $this->repository->find($id);
        if ($post === null) {
            throw new RuntimeException('post not found');
        }
        if ($post->status === 'published') {
            throw new RuntimeException('published post cannot be updated');
        }
        if (trim($content) === '') {
            throw new RuntimeException('content is required');
        }

        $post->content = $content;
        $post->scheduledAt = $scheduledAt;
        $post->note = $note;
        $saved = $this->repository->save($post);

        AuditLogger::info('post_updated', ['id' => $id]);
        return ['id' => $saved->id, 'status' => $saved->status, 'content' => $saved->content, 'scheduled_at' => $saved->scheduledAt];
    }

    public function reserve(int $id, string $scheduledAt): array
    {
        $post = $this->requirePost($id);
        $post->status = 'reserved';
        $post->scheduledAt = $scheduledAt;
        $this->repository->save($post);
        AuditLogger::info('post_reserved', ['id' => $id, 'scheduled_at' => $scheduledAt]);

        return ['id' => $id, 'status' => 'reserved', 'reserved_at' => $scheduledAt];
    }

    public function publish(int $id): array
    {
        $post = $this->requirePost($id);
        $post->status = 'published';
        $this->repository->save($post);
        AuditLogger::info('post_published', ['id' => $id]);

        return ['id' => $id, 'status' => 'published'];
    }

    public function cancel(int $id, string $reason): array
    {
        $post = $this->requirePost($id);
        if ($post->status === 'published') {
            throw new RuntimeException('published post cannot be canceled');
        }
        $post->status = 'canceled';
        $this->repository->save($post);
        AuditLogger::info('post_canceled', ['id' => $id, 'reason' => $reason]);

        return ['id' => $id, 'status' => 'canceled'];
    }

    private function requirePost(int $id)
    {
        $post = $this->repository->find($id);
        if ($post === null) {
            throw new RuntimeException('post not found');
        }

        return $post;
    }
}
