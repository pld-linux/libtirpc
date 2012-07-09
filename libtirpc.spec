#
# Conditional build:
%bcond_with	gssglue		# build with MIT Kerberos instead of Heimdal
#
Summary:	Transport Independent RPC Library
Summary(pl.UTF-8):	Biblioteka RPC niezależnego od transportu
Name:		libtirpc
Version:	0.2.2
Release:	4
Epoch:		1
License:	BSD-like
Group:		Libraries
Source0:	http://downloads.sourceforge.net/libtirpc/%{name}-%{version}.tar.bz2
# Source0-md5:	74c41c15c2909f7d11d9c7bfa7db6273
Patch0:		%{name}-link.patch
Patch1:		%{name}-heimdal.patch
# fixed in git
Patch2:		%{name}-XDR_GETPOS.patch
Patch3:		%{name}-rpc-des-prot.patch
Patch4:		%{name}-des-in-libc.patch
#Patch4:		%{name}-nis.patch
#Patch5:		%{name}-glibc-2.14.patch
URL:		http://sourceforge.net/projects/libtirpc/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	glibc >= 6:2.14-9.1
%if %{with gssglue}
BuildRequires:	libgssglue-devel >= 0.1
%else
BuildRequires:	heimdal-devel
%endif
BuildRequires:	libtool
BuildRequires:	pkgconfig
%if %{with gssglue}
Requires:	libgssglue >= 0.1
%else
Requires:	heimdal-libs
%endif
Requires:	glibc >= 6:2.14-9.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# FIXME: this allows invalid (unresolved symbols) library to be installed.
# Left until upstream fixes this properly.
%define	no_install_post_check_so	1

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
%if %{with gssglue}
Requires:	libgssglue-devel >= 0.1
%else
Requires:	heimdal-devel
%endif

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

%description static
This package includes static TI-RPC library.

%description static -l pl.UTF-8
Ten pakiet zawiera statyczną bibliotekę TI-RPC.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-gss=%{?with_gssglue:libgssglue}%{!?with_gssglue:heimdal-gssapi}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/%{_lib},%{_mandir}/man{3,5}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C doc install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_libdir}/libtirpc.so.* $RPM_BUILD_ROOT/%{_lib}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libtirpc.so
ln -sf /%{_lib}/$(cd $RPM_BUILD_ROOT/%{_lib}; echo lib*.so.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libtirpc.so

# obsoleted by pkgconfig
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libtirpc.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/netconfig
%attr(755,root,root) /%{_lib}/libtirpc.so.*.*
%attr(755,root,root) %ghost /%{_lib}/libtirpc.so.1
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
