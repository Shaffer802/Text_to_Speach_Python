<?php
// C:\xampp\htdocs\your_project\api\index.php
header('Content-Type: application/json');

// Path to your Python script (use forward slashes)
$pythonScript = 'C:/xampp/htdocs/PHP-Python-API_Test/python/test-script.py';

// Get input data
$input = file_get_contents('php://input');
$data = json_decode($input, true) ?? ["text" => "Hello, World!"];

// Prepare command
$command = 'python ' . escapeshellarg($pythonScript) . ' ' . escapeshellarg($input);

// Execute command
$output = shell_exec($command);

// Handle errors
if ($output === null) {
    http_response_code(500);
    echo json_encode(['error' => 'Python execution failed']);
    exit;
}

// Return output
echo $output;
?>