<?php
/* @var $view \Nethgui\Renderer\Xhtml */
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
});
EOJS;

$globalUseFile = new \ArrayObject();

/*
 * jQuery & jQueryUI libraries:
 */
if (defined('NETHGUI_DEBUG') && NETHGUI_DEBUG === TRUE) {
    $globalUseFile->append('js/jquery-1.9.1.js');
    $globalUseFile->append('js/jquery-migrate-1.2.1.js');
    $globalUseFile->append('js/jquery-ui-1.8.23.js');
} else {
    // require global javascript resources:
    $globalUseFile->append('js/jquery-1.9.1.min.js');
    $globalUseFile->append('js/jquery-migrate-1.2.1.min.js');
    $globalUseFile->append('js/jquery-ui-1.8.23.min.js');
}

/*
 * jQuery plugins
 */
$globalUseFile->append('js/jquery.dataTables.min.js');
$globalUseFile->append('js/jquery.qtip.min.js');

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
    ->useFile('css/jquery.qtip.min.css')
    ->useFile('css/font-awesome.css')
    ->useFile('css/base.css')
;
// Custom colors
if (isset($view['headerBackground'])) {
    $view->includeCss("
        #pageHeader-background {
            background-image: url(/images/{$view['headerBackground']}) !important;
        }
    ");
}
if (isset($view['menuBackground'])) {
    $view->includeCss("
    .secondaryContent .contentWrapper { background-image: url(/images/{$view['menuBackground']}); background-repeat:no-repeat;}
    ");
}

if (isset($view['colors']) && count($view['colors']) == 3) {
    if (!isset($view['headerBackground'])) {
        $view->includeCss("
            #pageHeader {
                background-color: {$view['colors'][0]} !important;
            }
        ");
    }
    if (!isset($view['menuBackground'])) {
        $view->includeCss("
            .secondaryContent .contentWrapper {
                background: {$view['colors'][1]} !important;
            }
        ");
    }

    $view->includeCss("
        #subMenu {
            background-color: {$view['colors'][0]} !important;
        }
        .DataTable th.ui-state-default, .Navigation.Flat a.currentMenuItem, .Navigation.Flat a:hover, .header {
            color: {$view['colors'][2]} !important;
        }
        .Navigation li a:hover { background: white !important }
        #Login .ui-widget-header {
             background: {$view['colors'][1]} !important;
        }
        #Login {
            border: 1px solid {$view['colors'][1]} !important;
        }

    ");
}
?><!DOCTYPE html>
<html lang="<?php echo $view['lang'] ?>">
    <head>
        <title><?php echo htmlspecialchars($view['company'] . " - " . $view['moduleTitle']) ?></title>
        <link rel="icon"  type="image/png"  href="<?php echo $view['favicon'] ?>" />
        <meta name="viewport" content="width=device-width" />  
        <script>document.write('<style id="hiddenAllWrapperCss" type="text/css">#allWrapper {display:none}</style>')</script><?php echo $view->literal($view['Resource']['css']) ?>
    </head>
    <body>
        <div id="allWrapper">
            <div id="pageHeader-background"></div>
            <div id="pageHeader" style="background-image: url(<?php echo htmlspecialchars($view['logo']); ?>)">
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
            <?php if ( ! $view['disableFooter']): ?><div id="footer"><p><?php echo htmlspecialchars($view['company'] . ' - ' . $view['address']) ?></p></div><?php endif; ?>
        </div><?php
        array_map(function ($f) use ($view) {
            printf("<script src='%s%s'></script>", $view->getPathUrl(), $f);
        }, iterator_to_array($globalUseFile));
        echo $view->literal($view['Resource']['js'])
        ?>
    </body>
</html>
