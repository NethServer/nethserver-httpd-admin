
include ../common/Makefile.common

checkout:
	git clone ssh://svn.nethesis.it/var/git/nethgui-framework.git nethgui-framework
	cd nethgui-framework; git submodule add ssh://svn.nethesis.it/var/git/neth-gui.git root/var/www/html/nethgui
