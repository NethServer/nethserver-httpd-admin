<?php
    header('Content-type:text/html; charset: utf-8');
    
    function ip_is_private ($ip) {
	    $pri_addrs = array (
	    '10.0.0.0|10.255.255.255', // single class A network
	    '172.16.0.0|172.31.255.255', // 16 contiguous class B network
	    '192.168.0.0|192.168.255.255', // 256 contiguous class C network
	    '169.254.0.0|169.254.255.255', // Link-local address also refered to as Automatic Private IP Addressing
	    '127.0.0.0|127.255.255.255' // localhost
		);
	
	    $long_ip = ip2long ($ip);
	    if ($long_ip != -1) {
	
	        foreach ($pri_addrs AS $pri_addr) {
	            list ($start, $end) = explode('|', $pri_addr);
	
	             // IF IS PRIVATE
	             if ($long_ip >= ip2long ($start) && $long_ip <= ip2long ($end)) {
	                 return true;
	             }
	        }
	    }
	
	    return false;
	}
    
    if(ip_is_private($_SERVER['REMOTE_ADDR']) || !ip_is_private($_SERVER['SERVER_ADDR'])){
	    $hostname = $_SERVER['SERVER_ADDR'];
    }else if(!ip_is_private($_SERVER['REMOTE_ADDR']) && ip_is_private($_SERVER['SERVER_ADDR'])){
	    $hostname = $_SERVER['SERVER_NAME'];
    }
    
    $url = htmlspecialchars(sprintf("https://%s:980", $hostname));
?><!DOCTYPE html>
<html lang="en">
<head>
<title>Bad request</title>
<meta http-equiv="refresh" content="2; URL='<?php echo $url ?>'">
</head>
<body>
<h1>Bad request</h1>
<p>Your browser sent a request that this server could not understand.<br>
Reason: You're speaking plain HTTP to an SSL-enabled server port.<br>
Instead use the HTTPS scheme to access this URL, please.</p>
<a href="<?php echo $url ?>"><?php echo $url ?></a>
</body>
</html>


