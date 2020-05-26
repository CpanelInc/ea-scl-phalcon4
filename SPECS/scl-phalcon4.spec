%define debug_package %{nil}

%{?scl:%global _scl_prefix /opt/cpanel}
%{!?scl:%global pkg_name %{name}}

%scl_package %scl

# This makes the ea-php<ver>-build macro stuff work
%scl_package_override

# must redefine this in the spec file because OBS doesn't know how
# to handle macros in BuildRequires statements
%{?scl:%global scl_prefix %{scl}-}

# Package namespaces
%global ns_name ea
%global ns_dir /opt/cpanel
%global _scl_prefix %ns_dir

# OBS builds the 32-bit targets as arch 'i586', and more typical
# 32-bit architecture is 'i386', but 32-bit archive is named 'x86'.
# 64-bit archive is 'x86-64', rather than 'x86_64'.
%if "%{_arch}" == "i586" || "%{_arch}" == "i386"
%global archive_arch x86
%else
%if "%{_arch}" == "x86_64"
%global archive_arch x86-64
%else
%global archive_arch %{_arch}
%endif
%endif

Name:    %{?scl_prefix}php-phalcon4
Vendor:  cPanel, Inc.
Summary: A full-stack PHP framework delivered as a C-extension
Version: 4.0.6
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4572 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
License: PHP
Group:   Development/Languages
URL: https://phalconphp.com/

#### https://fedoraproject.org/wiki/Packaging:SourceURL?rd=Packaging/SourceURL#Git_Hosting_Services
#### Source: https://github.com/phalcon/cphalcon/archive/v%{version}.tar.gz
#### does not work :(
Source: phalcon-cphalcon-v4.0.6-0-ga803581.tar.gz
Source1: phalcon.ini
BuildRequires: scl-utils-build
BuildRequires: %{?scl_prefix}scldevel
BuildRequires: %{?scl_prefix}build
BuildRequires: %{?scl_prefix}php-devel
BuildRequires: automake, libtool

%if 0%{rhel} > 6
BuildRequires: autoconf
%else
BuildRequires: autotools-latest-autoconf
%endif

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
Requires:      %{scl} %{?scl_prefix}php-cli
Requires:      %{?scl_prefix}php-psr
Requires:      %{?scl_prefix}php-pdo
Conflicts:     %{?scl_prefix}php-phalcon

%description
Phalcon is an open source full stack framework for PHP, written as a C-extension. Phalcon is optimized for high performance. Its unique architecture allows the framework to always be memory resident, offering its functionality whenever its needed, without expensive file stats and file reads that traditional PHP frameworks employ.

%prep
%setup -n phalcon-cphalcon-a803581
#### ^^^ [GitHub]

%install

echo $RPM_BUILD_ROOT/%{php_extdir}
mkdir -p $RPM_BUILD_ROOT/%{php_extdir}
cd build

%if 0%{rhel} < 7
INSTALL_ROOT=%{buildroot} scl enable autotools-latest './install --phpize %{_scl_root}/usr/bin/phpize --php-config %{_scl_root}/usr/bin/php-config'
%else
INSTALL_ROOT=%{buildroot} ./install --phpize %{_scl_root}/usr/bin/phpize --php-config %{_scl_root}/usr/bin/php-config
%endif

mkdir -p $RPM_BUILD_ROOT/%{_scl_root}/etc/php.d/
install %{SOURCE1} $RPM_BUILD_ROOT/%{_scl_root}/etc/php.d/90-phalcon.ini

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{php_extdir}/phalcon.so
%dir %{_scl_root}/usr/include/php/ext/phalcon
%{_scl_root}/usr/include/php/ext/phalcon/php_phalcon.h
%config(noreplace) %attr(644,root,root) %{_scl_root}/etc/php.d/90-phalcon.ini

%changelog
* Tue May 26 2020 Cory McIntire <cory@cpanel.net> - 4.0.6-1
- EA-9081: Update scl-phalcon4 from v4.0.5 to v4.0.6

* Mon Mar 30 2020 Julian Brown <julian.brown@cpanel.net> - 4.0.5-2
- ZC-6246: Add support for ea-php74

* Mon Mar 30 2020 Cory McIntire <cory@cpanel.net> - 4.0.5-1
- EA-8949: Update scl-phalcon4 from v4.0.4 to v4.0.5

* Thu Mar 05 2020 Tim Mullin <tim@cpanel.net> - 4.0.4-1
- EA-8902: Update scl-phalcon4 from 4.0.0.beta.2 to 4.0.4

* Mon Aug 26 2019 Julian Brown <julian.brown@cpanel.net> - 4.0.0_beta.2-1
- ZC-5471 update to beta2

* Wed Aug 14 2019 Julian Brown <julian.brown@cpanel.net> - 4.0.0_beta.1-1
- ZC-5380 created from source

