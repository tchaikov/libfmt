Name:           fmt
Version:        5.2.1
Release:        1%{?dist}
Summary:        Small, safe and fast formatting library for C++

License:        BSD
URL:            https://github.com/fmtlib/fmt
Source0:        https://github.com/fmtlib/fmt/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
# See https://github.com/fmtlib/fmt/issues/443 and https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/message/LVKYLDLJVWAVJE4MQVKDO6PYZRD5MCP6/
Patch1:         doc-build-removed-all-pip-internet-stuff.patch
Patch3:         doc-build-do-not-create-virtual-environment.patch
Patch4:         doc-_templates-layout-stripped-Google-Analytics.patch
Patch5:         doc-_templates-layout-stripped-download-links.patch
Patch6:         doc-index-removed-GitHub-iframe.patch
Patch7:         doc-build-use-sphinx-build-3.patch
Patch8:         doc-build-use-python3.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:  cmake3
%else
BuildRequires:  cmake
%endif
# For building documentation
BuildRequires:  doxygen
BuildRequires:  nodejs-less
%if 0%{?fedora}
BuildRequires:  python3-sphinx
BuildRequires:  python3-breathe
%else
BuildRequires:  python2-sphinx
BuildRequires:  python2-breathe
%endif

# This package replaces the old name of cppformat
Provides:       cppformat = %{version}-%{release}
Obsoletes:      cppformat < %{version}-%{release}

%description
C++ Format is an open-source formatting library for C++. It can be used as a
safe alternative to printf or as a fast alternative to IOStreams.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

# This package replaces the old name of cppformat
Provides:       cppformat-devel = %{version}-%{release}
Obsoletes:      cppformat-devel < %{version}-%{release}

%description    devel
This package contains the header file for using %{name}.

%package        doc
Summary:        Documentation files for %{name}
License:        Python
BuildArch:      noarch

# This package replaces the old name of cppformat
Provides:       cppformat-doc = %{version}-%{release}
Obsoletes:      cppformat-doc < %{version}-%{release}

%description    doc
This package contains documentation for developer documentation for %{name}.

%prep
%autosetup -p1

%build
mkdir build
pushd build
%if 0%{?rhel} && 0%{?rhel} <= 7
%cmake3 ..                                    \
%else
%cmake ..                                     \
%endif
    -DCMAKE_BUILD_TYPE=RelWithDebInfo         \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON      \
    -DFMT_CMAKE_DIR=%{_datarootdir}/cmake/%{name} \
    -DFMT_LIB_DIR=%{_libdir}

# Remove --clean-css since that plugin isn't available
sed -i "s/'--clean-css',//" ../doc/build.py
%make_build all doc
# Remove temporary build products
rm -rf ../build/doc/html/{.buildinfo,.doctrees,objects.inv}

%install
%make_install -C build

%check
pushd build
ctest -VV %{?_smp_mflags}
popd

%files
%{_libdir}/libfmt.so.*
%{!?_licensedir:%global license %%doc}
%license LICENSE.rst
%doc ChangeLog.rst README.rst

%files devel
%{_includedir}/fmt/
%{_libdir}/libfmt.so
%{_datarootdir}/cmake/fmt/

%files doc
%doc %{_datadir}/doc/fmt/
%license doc/python-license.txt

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Thu Oct 11 2018 Kefu Chai <tchaikov@gmail.com> - 5.2.1-1
- Update to 5.2.1
- Build using python3 packages on fedora
- Remove links in document accessing network
- Package ChangeLog.rst and README.rst
- Drop fmt-static package

* Fri Aug 31 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.0.2-7
- Fix python2 issue for doc

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 09 2017 Dave Johansen <davejohansen@gmail.com> - 3.0.2-4
- Patch for Test 8 segfault

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 24 2017 Dave Johansen <davejohansen@gmail.com> - 3.0.2-1
- Upstream release

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Tue Dec 27 2016 Dave Johansen <davejohansen@gmail.com> - 3.0.1-2
- Build documentation

* Fri Nov 25 2016 Dave Johansen <davejohansen@gmail.com> - 3.0.1-1
- Upstream release

* Tue Nov 15 2016 Dave Johansen <davejohansen@gmail.com> - 3.0.0-2
- Fix expected unqualified-id before numeric constant error

* Wed Aug 24 2016 Dave Johansen <davejohansen@gmail.com> - 3.0.0-1
- Initial RPM release
