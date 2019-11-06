Name:		bzip2
Version:	1.0.8
Release:	1
Summary:	A high-quality data compressor

License:	BSD
URL:		https://www.sourceware.org/bzip2/
Source0:	https://sourceware.org/pub/bzip2/%{name}-%{version}.tar.gz
Source1:	bzip2.pc

Patch0:		0001-add-compile-option.patch
Patch1:		0002-CVE-2019-12900.patch

BuildRequires:	gcc

Provides:       bzip2-libs
Obsoletes:      bzip2-libs

%description
bzip2 is a freely available, patent free, high-quality data compressor.
It typically compresses files to within 10% to 15% of the best available
techniques (the PPM family of statistical compressors), whilst being
around twice as fast at compression and six times faster at decompression.

%package	devel
Summary:	header files for bzip2
Requires:	%{name} = %{version}-%{release}
Provides:       bzip2-static
Obsoletes:      bzip2-static

%description	devel
header files for bzip2

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
%make_build -f Makefile-libbz2_so "CFLAGS=%{optflags} -Winline -D_FILE_OFFSET_BITS=64"
%make_build "CFLAGS=%{optflags} -fpic -fPIC -Winline -D_FILE_OFFSET_BITS=64"

%install
rm -rf %RPM_BUILD_ROOT
%make_install PREFIX=%{buildroot}%{_prefix}

# Default install path is /usr/bin lib man, change dest dirs here.
pushd %{buildroot}%{_prefix}
mkdir -p share
mv man/ share/
mv lib lib64
popd

ln -fs bzdiff %{buildroot}%{_bindir}/bzcmp
ln -fs bzgrep %{buildroot}%{_bindir}/bzegrep
ln -fs bzgrep %{buildroot}%{_bindir}/bzfgrep
ln -fs bzmore %{buildroot}%{_bindir}/bzless
install -m 0755 *.so* %{buildroot}%{_libdir}
ln -s libbz2.so.%{version} %{buildroot}%{_libdir}/libbz2.so.1
ln -s libbz2.so.%{version} %{buildroot}%{_libdir}/libbz2.so
cp %{SOURCE1} .
sed -i "s@^libdir=@libdir=%{_libdir}@" bzip2.pc
mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -m 0644 bzip2.pc %{buildroot}%{_libdir}/pkgconfig/
ln -s bzip2.1.gz %{buildroot}%{_mandir}/man1/bunzip2.1.gz
ln -s bzip2.1.gz %{buildroot}%{_mandir}/man1/bzcat.1.gz
ln -s bzip2.1.gz %{buildroot}%{_mandir}/man1/bzip2recover.1.gz

%check
make check

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%doc CHANGES LICENSE README
%license LICENSE
%{_bindir}/*
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/bzlib.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/
%{_libdir}/*.a

%files help
%doc manual.html manual.pdf
%{_mandir}/man1/b*.1.gz

%changelog
* Sat Oct 19 2019 openEuler Builteam <buildteam@openeuler.org> - 1.0.8-1
- update bzip2

* Tue Sep 24 2019 shenyangyang<shenyangyang4@huawei.com> - 1.0.6-33
- Type:enhancement
- ID:NA
- SUG:NA
- DESC:add help package and combine packages

* Mon Aug 12 2019 openEuler Builteam <buildteam@openeuler.org> - 1.0.6-32
- rewrite spec

* Thu Jul 25 2019 wangchan<wangchan9@huawei.com> - 1.0.6-31
- Modify version number

* Tue Jul 16 2019 wangchan<wangchan9@huawei.com> - 1.0.6-30
- Modify version number

* Mon Jul 15 2019 wangchan<wangchan9@huawei.com> - 1.0.6-29
- Type:security
- ID:CVE-2019-12900
- SUG:restart
- DESC: fix CVE-2019-12900

* Thu Jul 12 2018 openEuler Builteam <buildteam@openeuler.org>> - 1.0.6-28
- Package init
