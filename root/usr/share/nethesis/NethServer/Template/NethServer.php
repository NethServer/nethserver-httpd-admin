<?php
/* @var $view \Nethgui\Renderer\Xhtml */

//read css from db
$db = $view->getModule()->getPlatform()->getDatabase('configuration');
$myView = array();

$colors = $db->getProp('httpd-admin', 'colors');
if ($colors) {
    $colors = explode(',', $colors);
    $myView['colors'] = $colors;
}
$hb = $db->getProp('httpd-admin', 'headerBackground');
$mb = $db->getProp('httpd-admin', 'menuBackground');
if ($hb) {
    $myView['headerBackground'] = $hb;
}
if ($mb) {
    $myView['menuBackground'] = $mb;
}
$logo = $db->getProp('httpd-admin', 'logo');
$myView['logo'] = $view->getPathUrl() . ($logo ? sprintf('images/%s', $logo) : 'images/logo.png');
$myView['company'] = $db->getProp('OrganizationContact', 'Company');
$myView['address'] = $db->getProp('OrganizationContact', 'Street') . ", " . $db->getProp('OrganizationContact', 'City');
$favicon = $db->getProp('httpd-admin', 'favicon');
$myView['favicon'] = $view->getPathUrl() . ($favicon ? sprintf('images/%s', $favicon) : 'images/favicon.png');
if (file_exists("/etc/e-smith/db/configuration/defaults/cockpit.socket")) {
    $myView['cockpitUrl'] = "https://". $_SERVER['SERVER_NAME'] . ":9090";
} else {
    $myView['cockpitUrl'] = '';
}


if(strstr($view['username'], '@')) {
    $username = $view['username'];
} else {
    $username = $view['username'] . '@' . gethostname();
}

$filename = basename(__FILE__);
$bootstrapJs = <<<"EOJS"
/*
 * bootstrapJs in {$filename}
 */
jQuery(document).ready(function($) {
    $('script.unobstrusive').remove();
    $('#pageContent').Component();    
    $('.HelpArea').HelpArea();
    $('#hiddenAllWrapperCss').remove();

    // push initial ui state
    var target = window.location.href.split(/\#!?/, 2)[1];
    if(target) {
        $('#' + target).trigger('nethguishow');
        history.replaceState({'target': target}, '', '#!' + target);
    }

    if ( $( "#Login" ).length ) {
        $('#pageHeader-background').hide();
    } else {
        $('#pageHeader-background').show();
    }

    if( localStorage.getItem("hideCockpitTooltip") == null ) {
        $( "#cockpitTooltip" ).show();
        $( "#closeCockpitTooltip" ).click(function() {
            $( "#cockpitTooltip" ).hide();
            localStorage.setItem("hideCockpitTooltip", true);
        });
    } else {
        $( "#cockpitTooltip" ).hide();
    }
});
EOJS;

$globalUseFile = new \ArrayObject();

/*
 * jQuery & jQueryUI libraries:
 */
if (defined('NETHGUI_DEBUG') && NETHGUI_DEBUG === TRUE) {
    $globalUseFile->append('js/jquery-1.12.4.js');
    $globalUseFile->append('js/jquery-migrate-1.4.1.js');
    $globalUseFile->append('js/jquery-ui-1.8.23.js');
} else {
    // require global javascript resources:
    $globalUseFile->append('js/jquery-1.12.4.min.js');
    $globalUseFile->append('js/jquery-migrate-1.4.1.min.js');
    $globalUseFile->append('js/jquery-ui-1.8.23.min.js');
}

/*
 * jQuery plugins
 */
$globalUseFile->append('js/jquery.dataTables.min.js');
$globalUseFile->append('js/jquery.timepicker.min.js');

$lang = substr($view->getTranslator()->getLanguageCode(), 0, 2);
if ($lang !== 'en') {
    $globalUseFile->append(sprintf('js/jquery.ui.datepicker-%s.js', $lang));
}


$view
    ->includeFile('Nethgui/Js/jquery.nethgui.loading.js')
    ->includeFile('Nethgui/Js/jquery.nethgui.helparea.js')
    ->includeJavascript($bootstrapJs)
    // CSS:
    ->useFile('css/ui/jquery-ui-1.8.16.custom.css')
    ->useFile('css/font-awesome.css')
    ->useFile('css/base.css')
    ->useFile('css/jquery.timepicker.css')
;
// Custom colors
if (isset($myView['headerBackground'])) {
    $url =  "url('/images/{$myView['headerBackground']}') !important";
    $view->includeCss("
        #pageHeader-background {
        background-image: $url;
        background-image: -moz-linear-gradient(left, rgba(46,46,46,1) 0%, rgba(0,0,0,0) 50%, rgba(46,46,46,1) 100%), $url;
        background-image: -webkit-linear-gradient(left, rgba(46,46,46,1) 0%,rgba(0,0,0,0) 50%,rgba(46,46,46,1) 100%), $url; 
        background-image: linear-gradient(to right, rgba(46,46,46,1), rgba(0,0,0,0), rgba(46,46,46,1)), $url;
        }
    ");
}
if (isset($myView['menuBackground'])) {
    $view->includeCss("
    .secondaryContent .contentWrapper { background-image: url(/images/{$myView['menuBackground']}); background-repeat:no-repeat;}
    ");
}

if (isset($myView['colors']) && count($myView['colors']) == 3) {
    if (!isset($myView['headerBackground'])) {
        $view->includeCss("
            #pageHeader {
                background-color: {$myView['colors'][0]} !important;
            }
        ");
    }
    if (!isset($myView['menuBackground'])) {
        $view->includeCss("
            .secondaryContent .contentWrapper {
                background: {$myView['colors'][1]} !important;
            }
        ");
    }

    $view->includeCss("
        #subMenu {
            background-color: {$myView['colors'][0]} !important;
        }
        .DataTable th.ui-state-default, .Navigation.Flat a.currentMenuItem, .Navigation.Flat a:hover, .header {
            color: {$myView['colors'][2]} !important;
        }
        .Navigation li a:hover { background: white !important }
        #Login .ui-widget-header {
             background: {$myView['colors'][1]} !important;
        }
        #Login {
            border: 1px solid {$myView['colors'][1]} !important;
        }

    ");
}
?><!DOCTYPE html>
<html lang="<?php echo $view['lang'] ?>">
    <head>
        <title><?php echo htmlspecialchars($myView['company'] . " - " . $view['moduleTitle']) ?></title>
        <link rel="icon"  type="image/png"  href="<?php echo $myView['favicon'] ?>" />
        <meta name="viewport" content="width=device-width" />  
        <script>document.write('<style id="hiddenAllWrapperCss" type="text/css">#allWrapper {display:none}</style>')</script><?php echo $view->literal($view['Resource']['css']) ?>
    </head>
    <body>
         <?php if ($myView['cockpitUrl']): ?>
            <div id="cockpitTooltip"><?php echo htmlspecialchars($view->translate('cockpit_available')) ?><a href="<?php echo htmlspecialchars($myView['cockpitUrl']) ?>"><?php echo htmlspecialchars($myView['cockpitUrl']) ?></a>
            <a href="#" id="closeCockpitTooltip" class="fa fa-times pull-right"></a>
            </div>
        <?php endif; ?>
        <div id="allWrapper">
            <div id="pageHeader-background"></div>
            <div id="pageHeader" style="background-image: url(<?php echo htmlspecialchars($myView['logo']); ?>)">
                <a href='<?php echo \htmlspecialchars($view->getSiteUrl()); ?>'></a>
              <?php if ( ! $view['disableHeader']): ?>
		<div id="headerMenu">
            <div id="username"><i class="fa fa-user"></i> <?php echo htmlspecialchars($username) ?></div>
		    <ul id="subMenu">
			<li><a href="<?php echo htmlspecialchars($view->getModuleUrl('/UserProfile')); ?>">
			    <i class="fa fa-wrench"></i> <?php echo $T('Profile'); ?>
			</a></li>
			<li><form method="post" action="<?php echo htmlspecialchars($view->getModuleUrl('/Logout')); ?>">
			    <input type="hidden" value="<?php echo htmlspecialchars($view['Logout']['nextPath']); ?>" name="Logout[nextPath]">
			    <input type="hidden" value="logout" name="Logout[action]">			      
			    <button type="submit"><i class="fa fa-power-off"></i> <?php echo $T('Logout'); ?></button>
			    <input type="hidden" name="csrfToken" value="<?php echo htmlspecialchars($view['csrfToken']) ?>">
			</form></li>
		    </ul>
		</div>
                <h1 id="ModuleTitle"><?php echo htmlspecialchars($view['moduleTitle']) ?></h1>                
              <?php endif; ?>
            </div>
            <div id="pageContent">                
                <div class="primaryContent" role="main">
                    <?php 
                         echo $view['notificationOutput'];
                         echo $view['trackerOutput'];
                         echo $view['currentModuleOutput'];
                    ?>
                </div>
                <?php if ( ! $view['disableMenu']): ?><div class="secondaryContent" role="menu"><div class="contentWrapper"><h2><?php echo htmlspecialchars($view->translate('Other modules')) ?></h2><?php echo $view['menuOutput'] ?></div></div><?php endif; ?>
            </div><?php echo $view['helpAreaOutput'] ?>
            <?php if ( ! $view['disableFooter']): ?><div id="footer"><p><?php echo htmlspecialchars($myView['company'] . ' - ' . $myView['address']) ?></p></div><?php endif; ?>
        </div><?php
        array_map(function ($f) use ($view) {
            printf("<script src='%s%s'></script>", $view->getPathUrl(), $f);
        }, iterator_to_array($globalUseFile));
        echo $view->literal($view['Resource']['js'])
        ?>
    </body>
</html>
