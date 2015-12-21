<?php
    header('Content-type:text/html; charset: utf-8');
    $url = htmlspecialchars(sprintf("https://%s:980", $_SERVER['SERVER_ADDR']));
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


