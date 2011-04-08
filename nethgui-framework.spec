Name:		nethgui-framework		
Version:	0.0.1
Release:	1%{?dist}
Summary:	NethGui Framework package	

Group:		Networking	
License:	GPL	
Source0:	%{name}-%{version}.tar.gz	
BuildRoot:	/var/tmp/%{name}-%{version}-%{release}-buildroot

Requires:	codeigniter

BuildArch:	noarch
BuildRequires: 	e-smith-devtools


%description
NethGui Framework package including Apache and sudoers configuration

%prep
%setup -q


%build
perl createlinks


%install
rm -rf $RPM_BUILD_ROOT
(cd root ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-%{release}-filelist
/sbin/e-smith/genfilelist $RPM_BUILD_ROOT   > %{name}-%{version}-%{release}-filelist


%post
/sbin/e-smith/signal-event %{name}-update

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)

%changelog
* Thu Apr 07 2011 Giacomo Sanchietti <giacomo@nethesis.i> 0.0.1-1nh
- First NethGui Framework release


