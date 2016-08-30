Name:           fmt
Version:        3.0.0
Release:        1%{?dist}
Summary:        Small, safe and fast formatting library for C++

License:        BSD
URL:            https://github.com/fmtlib/fmt
Source0:        https://github.com/fmtlib/fmt/releases/download/%{version}/%{name}-%{version}.zip
# See https://github.com/fmtlib/fmt/issues/325
Patch0:         fmt_gmock_crash.patch
# See https://github.com/fmtlib/fmt/issues/329
Patch1:         fmt_mock_locale.patch

%if 0%{?rhel}
BuildRequires:  cmake3
%else
BuildRequires:  cmake
%endif

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
make %{?_smp_mflags} all

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
%doc doc/html/
%license doc/python-license.txt

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Wed Aug 24 2016 Dave Johansen <davejohansen@gmail.com> - 3.0.0-1
- Initial RPM release
