%define nethgui_commit f9aa109c38d9d7ff1895c647135c24a0c4adf522
%define uideps_commit  4c6534c9089197bfadeba0cc4569a20b994a4b31
%define pimple_commit  2.1.0
%define fontawesome_commit 4.1.0

Summary: apache/mod_php stack for nethserver-manager
Name: nethserver-httpd-admin
Version: 1.2.3
Release: 1%{?dist}
License: GPL
Source0: %{name}-%{version}.tar.gz
Source1: https://github.com/nethesis/nethserver-nethgui/archive/%{nethgui_commit}/nethserver-nethgui-%{nethgui_commit}.tar.gz
Source2: https://github.com/fabpot/Pimple/archive/v%{pimple_commit}/Pimple-%{pimple_commit}.tar.gz
Source3: https://github.com/nethesis/ui-deps-bundle/archive/%{uideps_commit}/ui-deps-bundle-%{uideps_commit}.tar.gz
Source4: https://github.com/FortAwesome/Font-Awesome/archive/v%{fontawesome_commit}/Font-Awesome-%{fontawesome_commit}.tar.gz

URL: %{url_prefix}/%{name} 

BuildRequires: nethserver-devtools > 1.0.1, git
BuildArch: noarch

Requires: httpd, php, mod_ssl, sudo
Obsoletes: nethserver-nethgui
Requires: nethserver-php
Requires: nethserver-base
Requires: perl(IO::Multiplex), perl(Net::Server::Multiplex)

AutoReq: no

%description 
Runs an Apache instance on port 980 with SSL that serves
the nethserver-manager web application

%prep
%setup    
%setup -D -T -b 1 
%setup -D -T -b 2 
%setup -D -T -b 3 
%setup -D -T -b 4 

%build
perl createlinks

mkdir -p root/usr/share/nethesis/nethserver-manager
cp -av $RPM_BUILD_DIR/ui-deps-bundle-%{uideps_commit}/{css,js} root/usr/share/nethesis/nethserver-manager/
cp -av $RPM_BUILD_DIR/nethserver-nethgui-%{nethgui_commit}/Nethgui    root/usr/share/nethesis/Nethgui
cp -av $RPM_BUILD_DIR/Pimple-%{pimple_commit}/src/Pimple  root/usr/share/nethesis/Pimple
cp -av $RPM_BUILD_DIR/FontAwesome-%{pimple_commit}/{css,fonts}  root/usr/share/nethesis/nethserver-manager/

%install
(cd root ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-%{release}-filelist
%{genfilelist} $RPM_BUILD_ROOT \
    --dir /var/cache/nethserver-httpd-admin 'attr(0750,srvmgr,srvmgr)' \
    --dir /var/log/httpd-admin 'attr(0700,root,root)' \
    > %{name}-%{version}-%{release}-filelist
echo "%doc COPYING" >> %{name}-%{version}-%{release}-filelist

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)

%pre
# ensure srvmgr user exists:
if ! id srvmgr >/dev/null 2>&1 ; then
   useradd -r -U -G adm srvmgr
fi


%changelog
* Thu Apr 17 2014 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.2.3-1.ns6
- Fix visualization problems with accented letters - Bug #2701

* Mon Mar 24 2014 Davide Principi <davide.principi@nethesis.it> - 1.2.2-1.ns6
- YUM categories in PackageManager - Feature #2694 [NethServer]

* Wed Feb 26 2014 Davide Principi <davide.principi@nethesis.it> - 1.2.1-1.ns6
- Revamp web UI style - Enhancement #2656 [NethServer]
- Emphasized visual style for mandatory text input fields - Feature #1753 [NethServer]

* Wed Feb 05 2014 Davide Principi <davide.principi@nethesis.it> - 1.2.0-1.ns6
- No feedback from Shutdown UI module - Bug #2629 [NethServer]
- RST format for help files - Enhancement #2627 [NethServer]
- Move httpd-admin web server logs - Feature #2551 [NethServer]
- Default remote access from public networks - Enhancement #2548 [NethServer]
- Restore httpd-admin symlink - Enhancement #2536 [NethServer]
- Move admin user in LDAP DB - Feature #2492 [NethServer]
- Give wings to server-manager - Enhancement #2460 [NethServer]

* Thu Oct 17 2013 Davide Principi <davide.principi@nethesis.it> - 1.0.6-1.ns6
- Add language code to URLs - Enhancement #2113 [Nethgui]

* Wed Aug 28 2013 Davide Principi <davide.principi@nethesis.it> - 1.0.5-1.ns6
- Import nethserver-manager code from nethserver-base - Enhancement #2110 [NethServer]
- RemoteAccess/HttpdAdmin UI module does not expand httpd-admin configuration - Bug #2094 [NethServer]
- Single and double quotes characters escaped - Bug #2068 [NethServer]

* Tue May  7 2013 Davide Principi <davide.principi@nethesis.it> - 1.0.4-1.ns6
- db defaults: added access prop with public default
- httpd/vhost-default template: use Redirect directive, in place of RewriteRule #1838 

* Tue Apr 30 2013 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.3-1.ns6
- Rebuild for automatic package handling. #1870
- Redirect /server-manager to port 980 #1838
- Web UI: show local networks as read-only elements #1021

* Tue Mar 19 2013 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.2-1.ns6
- Add migration code
- Use default SSL configuration

* Thu Jan 31 2013 Davide Principi <davide.principi@nethesis.it> - 1.0.1-1.ns6
- Implemented nethserver-base certificate management

