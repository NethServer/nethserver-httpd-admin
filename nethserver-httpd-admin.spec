%define nethgui_commit 194707c92bcbc7522f31268ba1500135bcb5ea52
%define uideps_commit c8d156dfdabee8bc870fac9423d8d159250e3c41
%define pimple_commit 2.1.0
%define fontawesome_commit 4.5.0
%define mustachejs_commit 0.8.2
%define mustachephp_commit 2.6.1
%define symfonyprocess_commit 2.8.8
%define datatables_commit 1.10.12
%define datatablesplugins_commit ba06cf106a2aff79f751027fbce2032525ce69da
%define timepicker_commit 1.11.5
%define extradocs %{_docdir}/%{name}-%{version}

Summary: apache/mod_php stack for nethserver-manager
Name: nethserver-httpd-admin
Version: 2.1.1
Release: 1%{?dist}
License: GPL
URL: %{url_prefix}/%{name}
BuildArch: noarch

Source0: %{name}-%{version}.tar.gz
Source1: https://github.com/NethServer/nethgui/archive/%{nethgui_commit}/nethgui-%{nethgui_commit}.tar.gz
Source2: https://github.com/fabpot/Pimple/archive/v%{pimple_commit}/Pimple-%{pimple_commit}.tar.gz
Source3: https://github.com/NethServer/ui-deps-bundle/archive/%{uideps_commit}/ui-deps-bundle-%{uideps_commit}.tar.gz
Source4: https://github.com/FortAwesome/Font-Awesome/archive/v%{fontawesome_commit}/Font-Awesome-%{fontawesome_commit}.tar.gz
Source5: https://github.com/bobthecow/mustache.php/archive/v%{mustachephp_commit}/mustache.php-%{mustachephp_commit}.tar.gz
Source6: https://github.com/janl/mustache.js/archive/%{mustachejs_commit}/mustache.js-%{mustachejs_commit}.tar.gz
Source7: https://github.com/symfony/Process/archive/v%{symfonyprocess_commit}/Process-%{symfonyprocess_commit}.tar.gz
Source8: https://github.com/DataTables/DataTables/archive/%{datatables_commit}/DataTables-%{datatables_commit}.tar.gz
Source9: https://github.com/DataTables/Plugins/archive/%{datatablesplugins_commit}/Plugins-%{datatablesplugins_commit}.tar.gz
Source10: https://github.com/jonthornton/jquery-timepicker/archive/%{timepicker_commit}/jquery-timepicker-%{timepicker_commit}.tar.gz

BuildRequires: nethserver-devtools

BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Requires: httpd, php, mod_ssl, sudo, php-xml, php-intl
Requires: nethserver-base, nethserver-php
Requires: nethserver-lang-en

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
%setup -D -T -b 10

# Nethgui:
cd %{_builddir}/nethgui-%{nethgui_commit}

%build
perl createlinks
mkdir -p root/%{_nseventsdir}/%{name}-update

%install
(cd root ; find . -depth -print | cpio -dump %{buildroot})
rm -f %{name}-%{version}-%{release}-filelist
%{genfilelist} %{buildroot} | sed '
\|^%{_sysconfdir}/sudoers.d/| d
' > %{name}-%{version}-%{release}-filelist
mkdir -p %{buildroot}/%{_localstatedir}/log/httpd-admin
mkdir -p %{buildroot}/%{_localstatedir}/cache/nethserver-httpd-admin
mkdir -p %{buildroot}/run/ptrack

# Copy package documentation
mkdir -p %{buildroot}/%{extradocs}
cp COPYING %{buildroot}/%{extradocs}

# Copy the server-manager dir
mkdir -p %{buildroot}%{_nsuidir}
cp -av nethserver-manager %{buildroot}%{_nsuidir}/nethserver-manager

# Copy external dependencies
cp -av %{_builddir}/ui-deps-bundle-%{uideps_commit}/{css,js} %{buildroot}%{_nsuidir}/nethserver-manager/
cp -av %{_builddir}/nethgui-%{nethgui_commit}/Nethgui    %{buildroot}%{_nsuidir}/Nethgui
cp -av %{_builddir}/Pimple-%{pimple_commit}/src/Pimple              %{buildroot}%{_nsuidir}/Pimple
cp -av %{_builddir}/Font-Awesome-%{fontawesome_commit}/{css,fonts}  %{buildroot}%{_nsuidir}/nethserver-manager/
cp -av %{_builddir}/mustache.js-%{mustachejs_commit}/mustache.js     %{buildroot}%{_nsuidir}/nethserver-manager/js
cp -av %{_builddir}/mustache.php-%{mustachephp_commit}/src/Mustache  %{buildroot}%{_nsuidir}/Mustache
cp -v %{_builddir}/DataTables-%{datatables_commit}/media/js/jquery.dataTables{,.min}.js %{buildroot}%{_nsuidir}/nethserver-manager/js
cp -v %{_builddir}/Plugins-%{datatablesplugins_commit}/sorting/*.js %{buildroot}%{_nsuidir}/nethserver-manager/js
pushd %{_builddir}/process-%{symfonyprocess_commit}; find . -name '*.php' | cpio -dump %{buildroot}%{_nsuidir}/Symfony/Component/Process; popd
cp -v %{_builddir}/jquery-timepicker-%{timepicker_commit}/jquery.timepicker{,.min}.js %{buildroot}%{_nsuidir}/nethserver-manager/js
cp -v %{_builddir}/jquery-timepicker-%{timepicker_commit}/jquery.timepicker.css %{buildroot}%{_nsuidir}/nethserver-manager/css

# Copy documentation and licenses from components:
mkdir -p %{buildroot}/%{extradocs}/Pimple-%{pimple_commit}
cp -av %{_builddir}/Pimple-%{pimple_commit}/{CHANGELOG,LICENSE,README.rst} %{buildroot}/%{extradocs}/Pimple-%{pimple_commit}/

mkdir -p %{buildroot}/%{extradocs}/Font-Awesome-%{fontawesome_commit}
cp -av %{_builddir}/Font-Awesome-%{fontawesome_commit}/README.md %{buildroot}/%{extradocs}/Font-Awesome-%{fontawesome_commit}/

mkdir -p %{buildroot}/%{extradocs}/nethgui-%{nethgui_commit}
cp -av %{_builddir}/nethgui-%{nethgui_commit}/{COPYING,Documentation/} %{buildroot}/%{extradocs}/nethgui-%{nethgui_commit}/

mkdir -p %{buildroot}/%{extradocs}/mustache.js-%{mustachejs_commit}
cp -av %{_builddir}/mustache.js-%{mustachejs_commit}/{CHANGES,LICENSE,README.md}  %{buildroot}/%{extradocs}/mustache.js-%{mustachejs_commit}

mkdir -p %{buildroot}/%{extradocs}/mustache.php-%{mustachephp_commit}
cp -av %{_builddir}/mustache.php-%{mustachephp_commit}/{CONTRIBUTING.md,LICENSE,README.md}  %{buildroot}/%{extradocs}/mustache.php-%{mustachephp_commit}

mkdir -p %{buildroot}/%{extradocs}/Symfony-Process-%{symfonyprocess_commit}
cp -av %{_builddir}/process-%{symfonyprocess_commit}/{LICENSE,README.md}  %{buildroot}/%{extradocs}/Symfony-Process-%{symfonyprocess_commit}

mkdir -p %{buildroot}/%{extradocs}/DataTables-%{datatables_commit}
cp -av %{_builddir}/DataTables-%{datatables_commit}/license.txt  %{buildroot}/%{extradocs}/DataTables-%{datatables_commit}

mkdir -p %{buildroot}/%{extradocs}/jquery-timepicker-%{timepicker_commit}
cp -av %{_builddir}/jquery-timepicker-%{timepicker_commit}/README.md  %{buildroot}/%{extradocs}/jquery-timepicker-%{timepicker_commit}

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%doc %{extradocs}

%{_nsuidir}/nethserver-manager
%{_nsuidir}/Nethgui
%{_nsuidir}/Pimple
%{_nsuidir}/Mustache
%{_nsuidir}/Symfony

%dir %{_nseventsdir}/%{name}-update
%dir %{_sysconfdir}/httpd/admin-conf.d

%attr(0750,srvmgr,srvmgr) %dir %{_localstatedir}/cache/nethserver-httpd-admin
%attr(0644,root,root) %ghost %{_sysconfdir}/init/httpd-admin.conf
%attr(0644,root,root) %ghost %{_sysconfdir}/httpd/admin-conf/httpd.conf
%attr(0600,root,root) %ghost %{_sysconfdir}/pki/tls/private/httpd-admin.key
%attr(0600,root,root) %ghost %{_sysconfdir}/pki/tls/certs/httpd-admin.crt
%attr(0700,root,root) %dir %{_localstatedir}/log/httpd-admin
%attr(0644,root,root) %config %ghost %{_localstatedir}/log/httpd-admin/access_log
%attr(0644,root,root) %config %ghost %{_localstatedir}/log/httpd-admin/error_log
%config %attr(440,root,root) %{_sysconfdir}/sudoers.d/20_nethserver_httpd_admin
%dir %attr(1770,root,adm) /run/ptrack
%config(noreplace) /etc/sysconfig/httpd-admin

%pre
# ensure srvmgr user exists:
if ! id srvmgr >/dev/null 2>&1 ; then
   useradd -r -U -G adm srvmgr
fi

%post
%systemd_post httpd-admin.service smwingsd.service

%preun
%systemd_preun httpd-admin.service smwingsd.service

%postun
%systemd_postun

%changelog
* Tue Apr 17 2018 Davide Principi <davide.principi@nethesis.it> - 2.1.1-1
- Restart smwingsd on failure - NethServer/dev#5453

* Tue Apr 03 2018 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 2.1.0-1
- Hardening TLS policy 2018-03-30 - NethServer/dev#5438

* Wed Nov 08 2017 Davide Principi <davide.principi@nethesis.it> - 2.0.14-1
- logrotate: httpd-admin fails reload - Bug NethServer/dev#5371

* Sat Sep 09 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 2.0.13-1
- CSRF and XSS vulnerabilities in server manager - Bug NethServer/dev#5345
- latest nethgui changes not included in nethserver-httpd-admin 2.0.12-1 - Bug NethServer/dev#5347 !! INCOMPLETE

* Fri Sep 08 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 2.0.12-1
- CSRF and XSS vulnerabilities in server manager - Bug NethServer/dev#5345

* Tue May 30 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 2.0.11-1
- Add an example to FQDN validator - NethServer/dev#5297

* Mon May 22 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 2.0.10-1
- PKI: SSL chain file not updated after certificate-update - Bug NethServer/dev#5283

* Mon Mar 06 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 2.0.9-1
- Migration from sme8 - NethServer/dev#5196

* Wed Feb 15 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 2.0.8-1
- Persist notifications on AJAX GET calls - nethgui#4009

* Mon Jan 30 2017 Davide Principi <davide.principi@nethesis.it> - 2.0.7-1
- Small code enhancements -- NethServer/nethserver-httpd-admin#20
- Bump nethgui f2a5b751

* Wed Jan 11 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 2.0.6-1
- Logical interfaces UI tweaks - NethServer/dev#5189
- httpd-admin: use KillMode=process - NethServer/dev#5190

* Fri Dec 16 2016 Davide Principi <davide.principi@nethesis.it> - 2.0.5-1
- Nethgui notifications fix -- NethServer/dev#5165

* Wed Nov 09 2016 Davide Principi <davide.principi@nethesis.it> - 2.0.4-1
- Strong SSL ciphers for httpd-admin
- Silence WARNING messages in server output

* Wed Sep 28 2016 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 2.0.3-1
- Firewall: time rules - NethServer/dev#5107

* Thu Sep 01 2016 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 2.0.2-1
- Internationalized domain names (IDN) in UI - NethServer/dev#5093
- Missing i18n labels - Bug NethServer/dev#5094
- Apache vhost-default template expansion - NethServer/dev#5088

* Thu Aug 25 2016 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 2.0.1-1
- Handle table keys with '/' character - NethServer/dev#5079
- Upgrade of the Process component
- db default: add missing headerBackground and menuBackground props

* Thu Jul 07 2016 Davide Principi <davide.principi@nethesis.it> - 2.0.0-1
- First NS7 release

* Fri Apr 01 2016 Davide Principi <davide.principi@nethesis.it> - 1.6.4-1
- Language fallback to alternative country - Enhancement #3368 [NethServer]

* Fri Mar 04 2016 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.3-1
- Invalid TCP port range - Bug #3333 [NethServer]

* Tue Sep 29 2015 Davide Principi <davide.principi@nethesis.it> - 1.6.2-1
- Make Italian language pack optional - Enhancement #3265 [NethServer]

* Tue Sep 29 2015 Davide Principi <davide.principi@nethesis.it> - 1.6.1-1
- Make Italian language pack optional - Enhancement #3265 [NethServer]

* Thu Sep 24 2015 Davide Principi <davide.principi@nethesis.it> - 1.6.0-1
- Upgrade SSL/TLS defaults on 6.7 - Enhancement #3246 [NethServer]

* Mon Jun 22 2015 Davide Principi <davide.principi@nethesis.it> - 1.5.0-1
- Updated jQuery and jQuery-UI libraries - Enhancement #2773 [NethServer]
- Wrong Server Manager menu category order - Bug #3197 [NethServer]
- smwingsd UTF-8 decode problems - Bug #3183 [NethServer]
- Require HTTPS protocol on port 980 - Enhancement #3104 [NethServer]
- Show host name in Server Manager - Enhancement #3103 [NethServer]

* Tue May 19 2015 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.1-1
- jQuery DateTime l10n - Enhancement #3147 [NethServer]

* Thu Apr 23 2015 Davide Principi <davide.principi@nethesis.it> - 1.4.0-1
- Language packs support - Feature #3115 [NethServer]

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

