Summary:	Transport Independent RPC Library
Summary(pl.UTF-8):	Biblioteka RPC niezależnego od transportu
Name:		libtirpc
Version:	0.1.7
Release:	2
License:	BSD-like
Group:		Libraries
Source0:	http://nfsv4.bullopensource.org/tarballs/tirpc/%{name}-%{version}.tar.bz2
# Source0-md5:	6b03f1567132abf546ff44643e136621
Patch1:		%{name}-netconfig.patch
Patch2:		%{name}-gssapi.patch
Patch3:		%{name}-svcauthnone.patch
Patch4:		%{name}-ppc64.patch
Patch5:		%{name}-svcauthdestroy.patch
Patch6:		%{name}-compile.patch
Patch7:		%{name}-xdr_string.patch
Patch8:		%{name}-more-ports.patch
Patch9:		%{name}-mutex.patch
Patch10:	%{name}-clnt_sperror.patch
Patch11:	%{name}-ntohs.patch
Patch12:	%{name}-recverr.patch
Patch13:	%{name}-link.patch
URL:		http://nfsv4.bullopensource.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libgssapi-devel >= 0.11
BuildRequires:	libtool
BuildRequires:	pkgconfig
Requires:	libgssapi >= 0.11
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
Requires:	%{name} = %{version}-%{release}
Requires:	libgssapi-devel >= 0.11

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
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package includes static TI-RPC library.

%description static -l pl.UTF-8
Ten pakiet zawiera statyczną bibliotekę TI-RPC.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-gss

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/%{_lib},%{_mandir}/man{3,5}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install man/netconfig.5 $RPM_BUILD_ROOT%{_mandir}/man5
install man/publickey.5 $RPM_BUILD_ROOT%{_mandir}/man5
install man/getnetconfig.3 $RPM_BUILD_ROOT%{_mandir}/man3
install man/getnetpath.3 $RPM_BUILD_ROOT%{_mandir}/man3
install man/publickey.3 $RPM_BUILD_ROOT%{_mandir}/man3
install man/rpc_*.3 $RPM_BUILD_ROOT%{_mandir}/man3
install man/rpcbind.3 $RPM_BUILD_ROOT%{_mandir}/man3

mv -f $RPM_BUILD_ROOT%{_libdir}/lib*.so.* $RPM_BUILD_ROOT/%{_lib}
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.so
ln -sf /%{_lib}/`(cd $RPM_BUILD_ROOT/%{_lib}; echo lib*.so.*.*)` \
	$RPM_BUILD_ROOT%{_libdir}/libtirpc.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/netconfig
%attr(755,root,root) /%{_lib}/libtirpc.so.*.*
%ghost %attr(755,root,root) /%{_lib}/libtirpc.so.?
%{_mandir}/man5/*.5*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtirpc.so
%{_libdir}/libtirpc.la
%{_includedir}/tirpc
%{_mandir}/man3/*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libtirpc.a
