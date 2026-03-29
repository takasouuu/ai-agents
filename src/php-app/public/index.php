<?php

declare(strict_types=1);

require_once __DIR__ . '/../bootstrap.php';

use App\Application\PostService;
use App\Controller\PostController;
use App\Infrastructure\InMemoryPostRepository;

$repository = new InMemoryPostRepository();
$service = new PostService($repository);
$controller = new PostController($service);

$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
$path = $_SERVER['PATH_INFO'] ?? '/';
$body = json_decode(file_get_contents('php://input') ?: '[]', true) ?: [];

$result = $controller->handle($method, $path, $body);
http_response_code($result['status']);
header('Content-Type: application/json; charset=utf-8');
echo json_encode($result['body'], JSON_UNESCAPED_UNICODE);
