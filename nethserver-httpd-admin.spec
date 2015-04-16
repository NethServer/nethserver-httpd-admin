%define nethgui_commit ab277fe5accdc2cf932c1a63b06029157586f2d0
%define uideps_commit d97a4dbf6d8b68cd9dbe9a0a633dd25ea4ca8d3f
%define pimple_commit 2.1.0
%define fontawesome_commit 4.1.0
%define mustachejs_commit 0.8.2
%define mustachephp_commit 2.6.1
%define symfonyprocess_commit 2.5.2
%define datatables_commit 1.10.2
%define datatablesplugins_commit fa5734b2908382f771047e1486a67405ee4d9b42
%define extradocs %{_docdir}/%{name}-%{version}

Summary: apache/mod_php stack for nethserver-manager
Name: nethserver-httpd-admin
Version: 1.3.8
Release: 1%{?dist}
License: GPL
Source0: %{name}-%{version}.tar.gz
Source1: https://github.com/nethesis/nethserver-nethgui/archive/%{nethgui_commit}/nethserver-nethgui-%{nethgui_commit}.tar.gz
Source2: https://github.com/fabpot/Pimple/archive/v%{pimple_commit}/Pimple-%{pimple_commit}.tar.gz
Source3: https://github.com/nethesis/ui-deps-bundle/archive/%{uideps_commit}/ui-deps-bundle-%{uideps_commit}.tar.gz
Source4: https://github.com/FortAwesome/Font-Awesome/archive/v%{fontawesome_commit}/Font-Awesome-%{fontawesome_commit}.tar.gz
Source5: https://github.com/bobthecow/mustache.php/archive/v%{mustachephp_commit}/mustache.php-%{mustachephp_commit}.tar.gz
Source6: https://github.com/janl/mustache.js/archive/%{mustachejs_commit}/mustache.js-%{mustachejs_commit}.tar.gz
Source7: https://github.com/symfony/Process/archive/v%{symfonyprocess_commit}/Process-%{symfonyprocess_commit}.tar.gz
Source8: https://github.com/DataTables/DataTables/archive/%{datatables_commit}/DataTables-%{datatables_commit}.tar.gz
Source9: https://github.com/DataTables/Plugins/archive/%{datatablesplugins_commit}/Plugins-%{datatablesplugins_commit}.tar.gz

URL: %{url_prefix}/%{name} 

BuildRequires: nethserver-devtools > 1.0.1, git
BuildArch: noarch

Requires: httpd, php, mod_ssl, sudo, php-xml, php-intl
Obsoletes: nethserver-nethgui
Requires: nethserver-lib > 2.1.1-1
Requires: nethserver-php
Requires: nethserver-base > 2.5.4-1
Requires: upstart
Requires: perl(IO::Multiplex), perl(Net::Server::Multiplex)
Requires: nethserver-lang-it, nethserver-lang-en

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
%setup -D -T -b 5
%setup -D -T -b 6
%setup -D -T -b 7
%setup -D -T -b 8
%setup -D -T -b 9

# Nethgui:
cd %{_builddir}/nethserver-nethgui-%{nethgui_commit}

%build
perl createlinks

%install
(cd root ; find . -depth -print | cpio -dump %{buildroot})
rm -f %{name}-%{version}-%{release}-filelist
%{genfilelist} %{buildroot} \
    > %{name}-%{version}-%{release}-filelist
mkdir -p %{buildroot}/%{_localstatedir}/log/httpd-admin
mkdir -p %{buildroot}/%{_localstatedir}/cache/nethserver-httpd-admin

# Copy package documentation
mkdir -p %{buildroot}/%{extradocs}
cp COPYING %{buildroot}/%{extradocs}

# Copy the server-manager dir
mkdir -p %{buildroot}/usr/share/nethesis
cp -av nethserver-manager %{buildroot}/usr/share/nethesis/nethserver-manager

# Copy external dependencies
cp -av %{_builddir}/ui-deps-bundle-%{uideps_commit}/{css,js} %{buildroot}/usr/share/nethesis/nethserver-manager/
cp -av %{_builddir}/nethserver-nethgui-%{nethgui_commit}/Nethgui    %{buildroot}/usr/share/nethesis/Nethgui
cp -av %{_builddir}/Pimple-%{pimple_commit}/src/Pimple              %{buildroot}/usr/share/nethesis/Pimple
cp -av %{_builddir}/Font-Awesome-%{fontawesome_commit}/{css,fonts}  %{buildroot}/usr/share/nethesis/nethserver-manager/
cp -av %{_builddir}/mustache.js-%{mustachejs_commit}/mustache.js     %{buildroot}/usr/share/nethesis/nethserver-manager/js
cp -av %{_builddir}/mustache.php-%{mustachephp_commit}/src/Mustache  %{buildroot}/usr/share/nethesis/Mustache
cp -v %{_builddir}/DataTables-%{datatables_commit}/media/js/jquery.dataTables{,.min}.js %{buildroot}/usr/share/nethesis/nethserver-manager/js
cp -v %{_builddir}/Plugins-%{datatablesplugins_commit}/sorting/*.js %{buildroot}/usr/share/nethesis/nethserver-manager/js
pushd %{_builddir}/Process-%{symfonyprocess_commit}; find . -name '*.php' | cpio -dump %{buildroot}/usr/share/nethesis/Symfony/Component/Process; popd

# Copy documentation and licenses from components:
mkdir -p %{buildroot}/%{extradocs}/Pimple-%{pimple_commit}
cp -av %{_builddir}/Pimple-%{pimple_commit}/{CHANGELOG,LICENSE,README.rst} %{buildroot}/%{extradocs}/Pimple-%{pimple_commit}/

mkdir -p %{buildroot}/%{extradocs}/Font-Awesome-%{fontawesome_commit}
cp -av %{_builddir}/Font-Awesome-%{fontawesome_commit}/README.md %{buildroot}/%{extradocs}/Font-Awesome-%{fontawesome_commit}/

mkdir -p %{buildroot}/%{extradocs}/nethserver-nethgui-%{nethgui_commit}
cp -av %{_builddir}/nethserver-nethgui-%{nethgui_commit}/{COPYING,Documentation/} %{buildroot}/%{extradocs}/nethserver-nethgui-%{nethgui_commit}/

mkdir -p %{buildroot}/%{extradocs}/mustache.js-%{mustachejs_commit}
cp -av %{_builddir}/mustache.js-%{mustachejs_commit}/{CHANGES,LICENSE,README.md}  %{buildroot}/%{extradocs}/mustache.js-%{mustachejs_commit}

mkdir -p %{buildroot}/%{extradocs}/mustache.php-%{mustachephp_commit}
cp -av %{_builddir}/mustache.php-%{mustachephp_commit}/{CONTRIBUTING.md,LICENSE,README.md}  %{buildroot}/%{extradocs}/mustache.php-%{mustachephp_commit}

mkdir -p %{buildroot}/%{extradocs}/Symfony-Process-%{symfonyprocess_commit}
cp -av %{_builddir}/Process-%{symfonyprocess_commit}/{LICENSE,README.md}  %{buildroot}/%{extradocs}/Symfony-Process-%{symfonyprocess_commit}

mkdir -p %{buildroot}/%{extradocs}/DataTables-%{datatables_commit}
cp -av %{_builddir}/DataTables-%{datatables_commit}/license.txt  %{buildroot}/%{extradocs}/DataTables-%{datatables_commit}

# Temporary home for English and Italian language packs:
mkdir -p %{buildroot}/usr/share/nethesis/Override/{Language,Help,Module}

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%doc %{extradocs}

/usr/share/nethesis/nethserver-manager
/usr/share/nethesis/Nethgui
/usr/share/nethesis/Pimple
/usr/share/nethesis/Mustache
/usr/share/nethesis/Symfony
/usr/share/nethesis/Override
/usr/share/nethesis/Override/Language
/usr/share/nethesis/Override/Help
/usr/share/nethesis/Override/Module


%attr(0750,srvmgr,srvmgr) %dir %{_localstatedir}/cache/nethserver-httpd-admin
%attr(0644,root,root) %ghost %{_sysconfdir}/init/httpd-admin.conf
%attr(0644,root,root) %ghost %{_sysconfdir}/httpd/admin-conf/httpd.conf
%attr(0600,root,root) %ghost %{_sysconfdir}/pki/tls/private/httpd-admin.key
%attr(0600,root,root) %ghost %{_sysconfdir}/pki/tls/certs/httpd-admin.crt
%attr(0700,root,root) %dir %{_localstatedir}/log/httpd-admin 
%attr(0644,root,root) %config %ghost %{_localstatedir}/log/httpd-admin/access_log
%attr(0644,root,root) %config %ghost %{_localstatedir}/log/httpd-admin/error_log

%pre
# ensure srvmgr user exists:
if ! id srvmgr >/dev/null 2>&1 ; then
   useradd -r -U -G adm srvmgr
fi
if [ $1 -eq 1 ]; then
   /sbin/stop httpd-admin >/dev/null 2>&1 || :
fi

%post
if [ $1 -eq 1 ]; then
   /sbin/start httpd-admin >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] && [ -f /var/run/httpd-admin.pid ]; then
   /sbin/stop httpd-admin >/dev/null 2>&1 || :
fi

%changelog
* Mon Mar 16 2015 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.3.8-1
- Fix: UI customization does not work Bug #3087

* Tue Mar 03 2015 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.3.7-1
- Set PHP default timezone from system timezone - Enhancement #3068 [NethServer]
- Move Logout button at top right - Enhancement #3046 [NethServer]
- Restore from backup, disaster recovery and network interfaces - Feature #3041 [NethServer]
- Differentiate root and admin users - Feature #3026 [NethServer]
- Inline help: Internal server error - Bug #3006 [NethServer]
- Show default password on server-manager login - Enhancement #2998 [NethServer]
- Refactor Organization contacts page - Feature #2969 [NethServer]
- Package Manager: new UPDATE button and optional packages selection - Feature #2963 [NethServer]
- squidGuard: support multiple profiles - Enhancement #2958 [NethServer]
- Base: first configuration wizard - Feature #2957 [NethServer]

* Tue Jan 20 2015 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.3.6-2.ns6
- Add php-xml dependency - Bug #3006 [NethServer]

* Wed Jan 14 2015 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.3.6-1.ns6
- Correctly handle history back button - Enhancement #2958 [NethServer]

* Tue Dec 09 2014 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.3.5-1.ns6
- Web interface: IP validator allows not valid addresses - Bug #2913 [NethServer]

* Wed Nov 19 2014 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.3.4-1.ns6
- Notify user if event fails - Enhancement #2927 [NethServer]
- Help/Template module error - Bug #2891 [Nethgui]
- "Language not found" error when requesting server-manager root URL - Bug #2883 [NethServer]

* Wed Oct 22 2014 Davide Principi <davide.principi@nethesis.it> - 1.3.3-1.ns6
- Protection against POODLE SSLv3 Vulnerability - Bug #2921 [NethServer]

* Wed Oct 15 2014 Davide Principi <davide.principi@nethesis.it> - 1.3.2-1.ns6
- Support DHCP on multiple interfaces - Feature #2849 [NethServer]

* Thu Oct 02 2014 Davide Principi <davide.principi@nethesis.it> - 1.3.1-1.ns6
- Selector widget: support validation tooltip  - Enhancement #2890 [Nethgui]
- Special DataTable sorting functions - Enhancement #2882 [Nethgui]
- Cannot access Server Manager after migration - Bug #2786 [NethServer]

* Wed Aug 20 2014 Davide Principi <davide.principi@nethesis.it> - 1.3.0-2.ns6
- Added 0001-NullRequest-fixed-User-object-creation.patch

* Wed Aug 20 2014 Davide Principi <davide.principi@nethesis.it> - 1.3.0-1.ns6
- Embed Nethgui 1.6.0 into httpd-admin RPM - Enhancement #2820 [NethServer]
- Build from plain .spec file enhanced - Enhancement #2812 [NethServer]
- Firewall: beautify rules page - Enhancement #2783 [NethServer]

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

