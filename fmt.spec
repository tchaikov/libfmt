Name:           fmt
Version:        3.0.1
Release:        2%{?dist}
Summary:        Small, safe and fast formatting library for C++

License:        BSD
URL:            https://github.com/fmtlib/fmt
Source0:        https://github.com/fmtlib/fmt/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

%if 0%{?rhel}
BuildRequires:  cmake3
%else
BuildRequires:  cmake
%endif
# For building documentation
BuildRequires:  doxygen
BuildRequires:  git
BuildRequires:  nodejs-less
BuildRequires:  python2-pip
BuildRequires:  python2-virtualenv

%description
C++ Format is an open-source formatting library for C++. It can be used as a
safe alternative to printf or as a fast alternative to IOStreams.

# This package replaces the old name of cppformat
Provides:       cppformat = %{version}-%{release}
Obsoletes:      cppformat < %{version}-%{release}

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

# This package replaces the old name of cppformat
Provides:       cppformat-devel = %{version}-%{release}
Obsoletes:      cppformat-devel < %{version}-%{release}

%description    devel
This package contains the header file for using %{name}.

%package        static
Summary:        Header only development files for %{name}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description    static
This package contains the files for using %{name} as a header only library.

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
cd build
cmakeopts="-DFMT_LIB_DIR=%{_lib} -DFMT_CMAKE_DIR=%{_datarootdir}/cmake/%{name}"
# NOTE: Specifying CMAKE_SKIP_RPATH=OFF is so it will link properly on RHEL 6
# See https://bugzilla.redhat.com/show_bug.cgi?id=640672
%if 0%{?rhel}%{?fedora} == 6
cmakeopts="$cmakeopts -DCMAKE_SKIP_RPATH=OFF"
%endif
%if 0%{?rhel}
%cmake3 \
%else
%cmake \
%endif
 $cmakeopts ..
# Remove --clean-css since that plugin isn't available
sed -i "s/'--clean-css',//" ../doc/build.py
make %{?_smp_mflags} all doc
# Remove temporary build products
rm -rf ../build/doc/html/{.buildinfo,.doctrees}

%install
make -C build install DESTDIR=%{buildroot}

%check
make -C build test

%files
%{_libdir}/libfmt.so.*
%{!?_licensedir:%global license %%doc}
%license LICENSE.rst

%files devel
%{_includedir}/fmt/
%{_libdir}/libfmt.so
%{_datarootdir}/cmake/fmt/

%files static
%{_includedir}/fmt/format.cc
%{_includedir}/fmt/ostream.cc
%{_includedir}/fmt/ostream.h
%{_includedir}/fmt/posix.h
%{_includedir}/fmt/time.h

%files doc
%doc %{_datadir}/doc/fmt/
%license doc/python-license.txt

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Tue Dec 27 2016 Dave Johansen <davejohansen@gmail.com> - 3.0.1-2
- Build documentation

* Fri Nov 25 2016 Dave Johansen <davejohansen@gmail.com> - 3.0.1-1
- Upstream release

* Tue Nov 15 2016 Dave Johansen <davejohansen@gmail.com> - 3.0.0-2
- Fix expected unqualified-id before numeric constant error

* Wed Aug 24 2016 Dave Johansen <davejohansen@gmail.com> - 3.0.0-1
- Initial RPM release
