#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Library and CLI for the Storj protocol
Summary(pl.UTF-8):	Biblioteka i narzędzie linii poleceń do protokołu Storj
Name:		libstorj
Version:	1.0.3
Release:	3
License:	LGPL v2.1
Group:		Libraries
#Source0Download: https://github.com/storj/libstorj/releases
Source0:	https://github.com/storj/libstorj/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e00b4938b375e935b19161ece3d10d56
URL:		https://github.com/storj/libstorj
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	curl-devel >= 7.35.0
BuildRequires:	json-c-devel >= 0.11
BuildRequires:	libtool >= 2:2
# only checked, finally not used
BuildRequires:	libmicrohttpd-devel >= 0.9
BuildRequires:	libuv-devel >= 1.8.0
BuildRequires:	nettle-devel >= 3.1
BuildRequires:	pkgconfig
# hexdump for tests
BuildRequires:	util-linux
Requires:	curl-libs >= 7.35.0
Requires:	json-c >= 0.11
Requires:	libuv >= 1.8.0
Requires:	nettle >= 3.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Asynchronous multi-platform C library and CLI for encrypted file
transfer on the Storj network.

%description -l pl.UTF-8
Asynchroniczna, wieloplatformowa biblioteka C oraz interfejs linii
poleceń do przesyłania zaszyfrowanych plików po sieci Storj.

%package devel
Summary:	Header files for Storj library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Storj
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	curl-devel >= 7.35.0
Requires:	json-c-devel >= 0.11
Requires:	libuv-devel >= 1.8.0
Requires:	nettle-devel >= 3.1

%description devel
Header files for Storj library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Storj.

%package static
Summary:	Static Storj library
Summary(pl.UTF-8):	Statyczna biblioteka Storj
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Storj library.

%description static -l pl.UTF-8
Statyczna biblioteka Storj.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I build-aux/m4
%{__autoconf}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libstorj.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/storj
%attr(755,root,root) %{_libdir}/libstorj.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libstorj.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libstorj.so
%{_includedir}/storj.h
%{_pkgconfigdir}/libstorj.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libstorj.a
%endif
