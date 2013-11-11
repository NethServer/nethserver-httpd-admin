<?php
namespace NethServer;

/*
 * Copyright (C) 2011 Nethesis S.r.l.
 *
 * This script is part of NethServer.
 *
 * NethServer is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * NethServer is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with NethServer.  If not, see <http://www.gnu.org/licenses/>.
 */

// PHP settings (timezone, error reporting..)
date_default_timezone_set('UTC');
ini_set('log_errors', "1");
ini_set('error_log', 'syslog');
ini_set('error_reporting', E_ALL | E_STRICT);
ini_set('session.use_trans_sid', "0");
session_cache_limiter(FALSE);
ini_set('display_errors', "0");
ini_set('html_errors', "0");
ini_set('default_mimetype', 'text/plain');
ini_set('default_charset', 'UTF-8');
setlocale(LC_CTYPE, 'en_US.utf-8');
register_shutdown_function(function() {   
    $error = error_get_last();
    if (is_array($error)) {
        header('HTTP/1.1 500 Internal server error');
        printf("\n\n[%s] %s\n\nSee the system log for details.\n", $error['type'], $error['message']);
    }
});

// If xdebug is loaded, disable xdebug backtraces:
extension_loaded('xdebug') && xdebug_disable();

// Enable nethgui javascript files auto inclusion:
define('NETHGUI_ENABLE_INCLUDE_WIDGET', TRUE);

$namespaces = array();
$loader = include_once("../vendor/autoload.php");

foreach ($loader->getPrefixes() as $nsName => $paths) {
    $namespaces[trim($nsName, '\\')] = reset($paths) . DIRECTORY_SEPARATOR . trim($nsName, '\\');
}

$FW = new \Nethgui\Framework();
$FW
    ->setLogLevel(E_WARNING | E_ERROR | E_NOTICE)
    ->registerNamespace($namespaces[__NAMESPACE__])
    ->setDefaultModule('Dashboard')
    ->setDecoratorTemplate('NethServer\\Template\\Nethesis')
;

try {
    $R = $FW->createRequest();
    if ($R->getFormat() === 'xhtml') {
        $R
            ->setParameter('Menu', array())
            ->setParameter('Notification', array())
            ->setParameter('Resource', array())
            ->setParameter('Logout', array())
        ;
    } elseif ($R->getFormat() === 'json') {
        $R->setParameter('Notification', array());
    }
    $FW->dispatch($R);
} catch (\Nethgui\Exception\HttpException $ex) {
    $FW->printHttpException($ex, FALSE);
} catch (\Exception $ex) {
    $FW->printHttpException(new \Nethgui\Exception\HttpException('Internal server error', 500, 1377609334, $ex), FALSE);
}

