Name:           malaga
Version:        7.12 
Release:        6%{?dist}
Summary:        A programming language for automatic language analysis

Group:          Development/Languages
License:        GPLv2+
URL:            http://home.arcor.de/bjoern-beutel/malaga/
Source0:        http://home.arcor.de/bjoern-beutel/malaga/%{name}-%{version}.tgz
# Fix map_file symbol conflict with samba. Upstream can be considered
# inactive but as libvoikko >= 2.2 doesn't use libmalaga anymore, these kind
# of problems won't probably come up. The only executables in Fedora which
# link to libmalaga currently are the malaga tools.
Patch0:         malaga-rename-map_file.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel readline-devel
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Requires: lib%{name} = %{version}-%{release}

%description
A software package for the development and application of
grammars that are used for the analysis of words and sentences of natural
languages. It is a language-independent system that offers a programming
language for the modelling of the language-dependent grammatical
information. This language is also called Malaga.

Malaga is based on the grammatical theory of the "Left Associative Grammar"
(LAG), developed by Roland Hausser, professor for Computational Linguistics at
University of Erlangen, Germany.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Languages
Requires:       lib%{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n	lib%{name}
Summary:        Library files for %{name}
Group:          Development/Libraries

%description -n	lib%{name}
Library files for %{name}.


%prep
%setup -q
%patch0 -p1
# Remove "@" marks so that the build process is more verbose
sed -i.debug -e 's|^\([ \t][ \t]*\)@|\1|' Makefile.in
# Remove "-s" so binaries won't be stripped
sed -i.strip -e 's| -s | |' Makefile.in
# Make libtool output more verbose
sed -i.silent -e 's|--silent||' Makefile.in

%build
%configure --with-readline
# Remove rpath,
# https://fedoraproject.org/wiki/Packaging/Guidelines#Removing_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL_INFO=/sbin/install-info INSTALL="install -p"
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
# Remove static archive
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'
# Change permission of libmalaga.so*
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/libmalaga.so*


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%post -n lib%{name} -p /sbin/ldconfig

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%postun -n lib%{name} -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_infodir}/%{name}*
%{_bindir}/mal*
%{_datadir}/%{name}
%{_mandir}/man1/mal*

%files -n lib%{name}
%defattr(-,root,root,-)
%doc CHANGES.txt GPL.txt README.txt
%defattr(-,root,root,-)
%{_libdir}/lib%{name}.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib%{name}*.so
%{_includedir}/malaga.h


%changelog
* Wed Sep 16 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 7.12-6
- Remove rpath which was set for the malaga binaries in 64 bit architechtures

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 14 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 7.12-4
- Add patch to change the (un)map_file functions to malaga_(un)map_file,
  there was a symbol conflict with the samba libraries causing a segfault
  if enchant-voikko and evolution-mapi were both installed when using
  Evolution. Bugs rhbz #502546 and sourceforge #2802548, patch by Harri
  Pitkänen.
- Add defattr to the libmalaga subpackage

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Apr 03 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 7.12-2
- Upstream changed the source tarball of the current release, use the current
  upstream sources

* Sun Mar 02 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 7.12-1
- New version
- Drop upstreamed linking patch
- Re-add a Makefile.in sed build verbosity trick, which was done in the
  dropped patch but not upstream

* Sat Feb 23 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 7.11-3
- Add Makefile.in patch to link the executables against libmalaga

* Sat Feb 16 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 7.11-2
- Rebuild for GCC 4.3

* Mon Oct 29 2007 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 7.11-1
- Increment release for the first Fedora build

* Sun Oct 28 2007 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 7.11-0.5
- -devel requires only libmalaga, not malaga

* Sun Oct 28 2007 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 7.11-0.4
- Add option --with-readline to configure
- Add BR readline-devel

* Sat Oct 27 2007 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 7.11-0.3
- Don't strip binaries
- Remove static archive
- Make build procedure more verbose
- Make libtool output more verbose
- Remove redundant requires gtk2
- Add INSTALL="install -p" to make install to preserve timestamps
- Change libmalaga.so* to have permissions 0755

* Wed Oct 24 2007 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 7.11-0.2
- Main package requires libmalaga version-release and gtk2 (malshow needs it)
- libmalaga requires in -devel removed, that's implicit
- install-info called in post of main package
- Unneeded postun line removed
- INSTALL.txt is not needed in this package
- All documents are now in libmalaga
- /usr/share/malaga/ now owned by the malaga package
- A shorter Summary so rpmlint won't complain
- Currently writes an empty debuginfo package, "install -s" is called in 
  Makefile, how do I remove it?

* Mon Oct 22 2007 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 7.11-0.1
- Initial package
