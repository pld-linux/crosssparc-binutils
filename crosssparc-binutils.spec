Summary:	Cross SPARC GNU binary utility development utilities - binutils
Summary(es.UTF-8):	Utilitarios para desarrollo de binarios de la GNU - SPARC binutils
Summary(fr.UTF-8):	Utilitaires de développement binaire de GNU - SPARC binutils
Summary(pl.UTF-8):	Skrośne narzędzia programistyczne GNU dla SPARC - binutils
Summary(pt_BR.UTF-8):	Utilitários para desenvolvimento de binários da GNU - SPARC binutils
Summary(tr.UTF-8):	GNU geliştirme araçları - SPARC binutils
Name:		crosssparc-binutils
Version:	2.46
Release:	1
License:	GPL v3+
Group:		Development/Tools
Source0:	https://ftp.gnu.org/gnu/binutils/binutils-with-gold-%{version}.tar.lz
# Source0-md5:	e221b6201b7234e3e7733e878ff476c4
URL:		http://sources.redhat.com/binutils/
BuildRequires:	automake
BuildRequires:	bash
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	lzip
BuildRequires:	tar >= 1:1.22
BuildRequires:	xxHash-devel
BuildRequires:	zlib-devel
ExcludeArch:	sparc sparcv9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		sparc-pld-linux
%define		arch		%{_prefix}/%{target}

%description
Binutils is a collection of binary utilities, including:
- ar - create, modify and extract from archives,
- nm - lists symbols from object files,
- objcopy - copy and translate object files,
- objdump - display information from object files,
- ranlib - generate an index for the contents of an archive,
- size - list the section sizes of an object or archive file,
- strings - list printable strings from files,
- strip - discard symbols,
- c++filt - a filter for demangling encoded C++ symbols,
- addr2line - convert addresses to file and line,
- nlmconv - convert object code into an NLM.

This package contains the cross version for SPARC.

%description -l pl.UTF-8
Pakiet binutils zawiera zestaw narzędzi umożliwiających kompilację
programów. Znajdują się tutaj między innymi assembler, konsolidator
(linker), a także inne narzędzia do manipulowania binarnymi plikami
programów i bibliotek.

Ten pakiet zawiera wersję skrośną generującą kod dla SPARC.

%prep
%setup -q -n binutils-with-gold-%{version}

%build
# ldscripts won't be generated properly if SHELL is not bash...
export CFLAGS="%{rpmcflags} -fno-strict-aliasing"
export CONFIG_SHELL="/bin/bash"
%configure \
	--disable-shared \
	--disable-silent-rules \
	--disable-nls \
	--enable-64-bit-bfd \
	--target=%{target} \
	--with-sysroot=%{_libdir}/%{target} \
	--with-debuginfod=no \
	--with-msgpack=no \
	--with-system-zlib \
	--with-zstd=no \
	--disable-jansson

%{__make} all \
	tooldir=%{_prefix} \
	EXEEXT=""

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# remove these man pages unless we cross-build for win*/netware platforms.
# however, this should be done in Makefiles.
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/{*dlltool,*nlmconv,*windres}.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/%{target}-*
%dir %{arch}
%dir %{arch}/bin
%attr(755,root,root) %{arch}/bin/*
%dir %{arch}/lib
%dir %{arch}/lib/*
%{arch}/lib/ldscripts/*
%{_mandir}/man?/%{target}-*
