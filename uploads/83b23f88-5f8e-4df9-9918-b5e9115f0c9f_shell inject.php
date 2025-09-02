<?php
 $output = shell_exec('uname -a' . " 2>&1"); // Jalankan perintah dan tangkap output
 echo "<pre>$output</pre>"; // Tampilkan output dalam tag <pre>
 die;
?>