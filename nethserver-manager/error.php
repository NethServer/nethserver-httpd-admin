<?php
    header('Content-type:text/html; charset: utf-8');
    $url = htmlspecialchars(sprintf("https://%s:980", $_SERVER['SERVER_ADDR']));
    $url2 = htmlspecialchars(sprintf("https://%s:980", $_SERVER['SERVER_NAME']));
?><!DOCTYPE html>
<html lang="en">
<head>
<title>Bad request</title>
<noscript>
<meta http-equiv="refresh" content="2; URL='<?php echo $url ?>'">
</noscript>
<script type="text/javascript">
var url = window.location.href.replace("http://", "https://");
document.write('<meta http-equiv="refresh" content="2; URL=\'' + url + '\'">');
</script>
</head>
<body>
<h1>Bad request</h1>
<p>Use the HTTPS scheme to access this URL!<p>
<p>Please try with
<noscript>
<a href="<?php echo $url2 ?>"><?php echo $url2 ?></a>
</noscript>
<script type="text/javascript">
var url = window.location.href.replace("http://", "https://");
document.write('<a href="' + url + '">' + url + '</a>');
</script>
</p>
</body>
</html>

