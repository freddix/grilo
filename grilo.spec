Summary:	Framework for access to sources of multimedia content
Name:		grilo
Version:	0.2.8
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/grilo/0.2/%{name}-%{version}.tar.xz
# Source0-md5:	ded2f82fd2fc5291762134d0cfc70307
URL:		http://live.gnome.org/Grilo
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk+3-devel
BuildRequires:	libsoup-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	vala-vapigen
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Grilo is a framework that provides access to various sources of
multimedia content, using a pluggable system.

%package devel
Summary:	Header files for grilo library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for grilo library.

%package apidocs
Summary:	grilo API documentation
Group:		Documentation

%description apidocs
API and internal documentation for grilo library.

%prep
%setup -q

# kill gnome common deps
%{__sed} -i -e '/GNOME_COMPILE_WARNINGS.*/d'	\
    -i -e '/GNOME_MAINTAINER_MODE_DEFINES/d'	\
    -i -e '/GNOME_COMMON_INIT/d'		\
    -i -e '/GNOME_CXX_WARNINGS.*/d'		\
    -i -e '/GNOME_DEBUG_CHECK/d' configure.ac

# vala 0.22 fix
%{__sed} -i 's/\ \[0.20\]/\ \[0.20\], \[0.22\]/' configure.ac

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-debug		\
	--disable-silent-rules	\
	--disable-static	\
	--enable-vala		\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/grilo-0.2

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/grilo-simple-playlist
%attr(755,root,root) %{_bindir}/grl-inspect-0.2
%attr(755,root,root) %ghost %{_libdir}/libgrilo-0.2.so.1
%attr(755,root,root) %ghost %{_libdir}/libgrlnet-0.2.so.0
%attr(755,root,root) %ghost %{_libdir}/libgrlpls-0.2.so.0
%attr(755,root,root) %{_libdir}/libgrilo-0.2.so.*.*.*
%attr(755,root,root) %{_libdir}/libgrlnet-0.2.so.*.*.*
%attr(755,root,root) %{_libdir}/libgrlpls-0.2.so.*.*.*
%dir %{_libdir}/grilo-0.2
%{_libdir}/girepository-1.0/*.typelib
%{_mandir}/man1/grl-inspect.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/grilo-0.2
%{_pkgconfigdir}/*.pc
%{_datadir}/gir-1.0/*.gir
%{_datadir}/vala/vapi/*.deps
%{_datadir}/vala/vapi/*.vapi

%if 0
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/grilo
%endif

