<?php

declare(strict_types=1);

namespace InternalLib;

final class AuditLogger
{
    public static function info(string $message, array $context = []): void
    {
        $line = '[AUDIT] ' . $message . ' ' . json_encode($context, JSON_UNESCAPED_UNICODE) . PHP_EOL;
        file_put_contents(__DIR__ . '/../../../.runtime/internal-lib-audit.log', $line, FILE_APPEND);
    }
}
