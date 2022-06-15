#
# Conditional build
%bcond_without	gssapi		# GSSAPI support
%bcond_without	musl		# minimal tirpc for musl usage

%if %{with musl}
%undefine	gssapi
%endif

Summary:	Transport Independent RPC Library
Summary(pl.UTF-8):	Biblioteka RPC niezależnego od transportu
Name:		libtirpc
Version:	1.3.2
Release:	4
Epoch:		1
License:	BSD
Group:		Libraries
Source0:	https://downloads.sourceforge.net/libtirpc/%{name}-%{version}.tar.bz2
# Source0-md5:	cf4ca51f3fc401bea61c702c69171ab0
Patch0:		%{name}-link.patch
URL:		http://sourceforge.net/projects/libtirpc/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.11
BuildRequires:	glibc >= 6:2.14-9.1
%{?with_gssapi:BuildRequires:	heimdal-devel}
BuildRequires:	libtool
BuildRequires:	pkgconfig
%{?with_gssapi:Requires:	heimdal-libs}
%if %{with musl}
BuildRequires:	musl
BuildRequires:	linux-musl-headers
%endif
Requires:	glibc >= 6:2.14-9.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains SunLib's implementation of transport-independent
RPC (TI-RPC) documentation. This library forms a piece of the base of
Open Network Computing (ONC), and is derived directly from the Solaris
2.3 source.

TI-RPC is an enhanced version of TS-RPC that requires the UNIX System
V Transport Layer Interface (TLI) or an equivalent X/Open Transport
Interface (XTI). TI-RPC is on-the-wire compatible with the TS-RPC,
which is supported by almost 70 vendors on all major operating
systems. TS-RPC source code (RPCSRC 4.0) remains available from
several Internet sites.

%description -l pl.UTF-8
Ten pakiet zawiera implementację SunLib RPC niezależnego od transportu
(TI-RPC). Ta biblioteka tworzy element podstawy dla ONC (Open Network
Computing) i wywodzi się bezpośrednio ze źródeł Solarisa 2.3.

TI-RPC to rozszerzona wersja TS-RPC wymagająca TLI (UNIX System V
Transport Layer Interface). Jest kompatybilna w locie z TS-RPC,
obsługiwanym przez prawie 70 producentów dla wszystkich znaczących
systemów operacyjnych. Kod źródłowy TS-RPC (RPCSRC 4.0) pozostaje
dostępny z różnych stron internetowych.

%package devel
Summary:	Development files for the TI-RPC library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki TI-RPC
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	glibc-devel >= 6:2.14-9.1
%{?with_gssapi:Requires:	heimdal-devel}

%description devel
This package includes header files necessary for developing programs
which use the TI-RPC library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia programów
wykorzystujących bibliotekę TI-RPC.

%package static
Summary:	Static TI-RPC library
Summary(pl.UTF-8):	Statyczna biblioteka TI-RPC
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
%{?with_gssapi:Requires:	heimdal-static}

%description static
This package includes static TI-RPC library.

%description static -l pl.UTF-8
Ten pakiet zawiera statyczną bibliotekę TI-RPC.

%package musl-devel
Summary:	Static TI-RPC library for musl usage
Summary(pl.UTF-8):	Statyczna biblioteka TI-RPC do użycia z musl
Group:		Development/Libraries

%description musl-devel
This package includes static TI-RPC library for musl usage.

%description musl-devel -l pl.UTF-8
Ten pakiet zawiera statyczną bibliotekę TI-RPC do użycia z musl.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
install -d build
cd build
../%configure \
	--disable-silent-rules \
	--enable-authdes \
        %{!?with_gssapi:--disable-gssapi}

%{__make}
cd ..

%if %{with musl}
install -d musl
cd musl
../%configure \
	CC="musl-gcc" \
	CFLAGS="%{rpmcflags} -I%{_includedir}/musl -fno-stack-protector" \
	LDFLAGS="%{rpmldflags} -L%{_libdir}/musl" \
	--disable-silent-rules \
	--enable-authdes \
	--disable-gssapi
%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/%{_lib},%{_mandir}/man{3,5}}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with musl}
%{__make} -C musl install \
	DESTDIR=$(pwd)/musl/destdir

install -d $RPM_BUILD_ROOT{%{_includedir}/musl,%{_libdir}/musl}
mv musl/destdir/%{_includedir}/tirpc $RPM_BUILD_ROOT%{_includedir}/musl
mv musl/destdir/%{_libdir}/libtirpc.a $RPM_BUILD_ROOT%{_libdir}/musl

%endif

%{__make} -C build/doc install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_libdir}/libtirpc.so.* $RPM_BUILD_ROOT/%{_lib}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libtirpc.so
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libtirpc.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libtirpc.so

# obsoleted by pkgconfig
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libtirpc.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README THANKS TODO
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/bindresvport.blacklist
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/netconfig
%attr(755,root,root) /%{_lib}/libtirpc.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libtirpc.so.3
%{_mandir}/man5/netconfig.5*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtirpc.so
%{_includedir}/tirpc
%{_pkgconfigdir}/libtirpc.pc
%{_mandir}/man3/bindresvport.3t*
%{_mandir}/man3/des_crypt.3t*
%{_mandir}/man3/getnet*.3t*
%{_mandir}/man3/getrpc*.3t*
%{_mandir}/man3/rpc*.3t*
%{_mandir}/man3/rtime.3t*

%files static
%defattr(644,root,root,755)
%{_libdir}/libtirpc.a

%files musl-devel
%defattr(644,root,root,755)
%{_includedir}/musl/tirpc
%{_libdir}/musl/libtirpc.a
