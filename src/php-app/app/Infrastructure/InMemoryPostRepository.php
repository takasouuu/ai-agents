<?php

declare(strict_types=1);

namespace App\Infrastructure;

use App\Domain\PostCandidate;

final class InMemoryPostRepository
{
    /** @var array<int, PostCandidate> */
    private array $posts = [];

    public function __construct()
    {
        $this->posts[1] = new PostCandidate(1, '初期投稿候補', 'draft');
    }

    /** @return array<int, PostCandidate> */
    public function all(): array
    {
        return array_values($this->posts);
    }

    public function find(int $id): ?PostCandidate
    {
        return $this->posts[$id] ?? null;
    }

    public function save(PostCandidate $post): PostCandidate
    {
        $this->posts[$post->id] = $post;
        return $post;
    }
}
