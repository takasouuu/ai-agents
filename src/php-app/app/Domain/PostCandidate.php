<?php

declare(strict_types=1);

namespace App\Domain;

final class PostCandidate
{
    public function __construct(
        public int $id,
        public string $content,
        public string $status,
        public ?string $scheduledAt = null,
        public ?string $note = null
    ) {
    }
}
