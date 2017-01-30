#
# Conditional build:
%bcond_without	octave	# Octave (MATLAB) module
#
Summary:	LIBSVM - simple, easy-to-use and efficient software for SVM classification and regression
Summary(pl.UTF-8):	LIBSVM - proste, łatwe w użyciu i wydajne oprogramowanie do klasyfikacji i regresji SVM
Name:		libsvm
Version:	3.22
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://www.csie.ntu.edu.tw/~cjlin/libsvm/%{name}-%{version}.tar.gz
# Source0-md5:	7c5c521a6a68c0f879c82f376e3557b6
Patch0:		%{name}-python.patch
Patch1:		%{name}-make.patch
URL:		http://www.csie.ntu.edu.tw/~cjlin/libsvm/
BuildRequires:	libstdc++-devel
%{?with_octave:BuildRequires:	octave-devel}
BuildRequires:	rpm-pythonprov
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		octave_oct_dir	%(octave-config --oct-site-dir)

%description
Libsvm is a simple, easy-to-use, and efficient software for SVM
classification and regression. It solves C-SVM classification, nu-SVM
classification, one-class-SVM, epsilon-SVM regression, and nu-SVM
regression. It also provides an automatic model selection tool for
C-SVM classification.

%description -l pl.UTF-8
Libsvm tio proste, łatwe w użyciu i wydajne oprogramowanie do
klasyfikacji i regresji SVM. Rozwiązuje problemy klasyfikacji C-SVM,
klasyfikacji nu-SVM, jednoklasowe SVM, regresji epsilon-SVM oraz
regresji nu-SVM. Udostępnia także narzędzie do automatycznego wyboru
modelu dla klasyfikacji C-SVM.

%package devel
Summary:	Header files for LIBSVM library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki LIBSVM
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for LIBSVM library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki LIBSVM.

%package -n octave-libsvm
Summary:	MATLAB/Octave interface for LIBSVM library
Summary(pl.UTF-8):	Interfejs MATLAB-a/Octave do biblioteki LIBSVM
Group:		Libraries
Requires:	octave

%description -n octave-libsvm
MATLAB/Octave interface for LIBSVM library.

%description -n octave-libsvm -l pl.UTF-8
Interfejs MATLAB-a/Octave do biblioteki LIBSVM.

%package -n python-libsvm
Summary:	Python interface for LIBSVM library
Summary(pl.UTF-8):	Interfejs Pythona do biblioteki LIBSVM
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-libsvm
Python interface for LIBSVM library.

%description -n python-libsvm -l pl.UTF-8
Interfejs Pythona do biblioteki LIBSVM.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} -fPIC -Wall"

%if %{with octave}
%{__make} -C matlab \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} -fPIC -I.. -I/usr/include/octave -Wall" \
	MEX=mkoctfile \
	MEX_OPTION=--mex \
	MEX_EXT=mex
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir},%{py_sitescriptdir}}

install libsvm.so.* $RPM_BUILD_ROOT%{_libdir}
ln -sf $(basename $RPM_BUILD_ROOT%{_libdir}/libsvm.so.*) $RPM_BUILD_ROOT%{_libdir}/libsvm.so
cp -p svm.h $RPM_BUILD_ROOT%{_includedir}
install svm-predict svm-scale svm-train $RPM_BUILD_ROOT%{_bindir}
cp -p python/*.py $RPM_BUILD_ROOT%{py_sitescriptdir}

%if %{with octave}
install -d $RPM_BUILD_ROOT%{octave_oct_dir}/libsvm
install matlab/*.mex $RPM_BUILD_ROOT%{octave_oct_dir}/libsvm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYRIGHT FAQ.html README
%attr(755,root,root) %{_bindir}/svm-predict
%attr(755,root,root) %{_bindir}/svm-scale
%attr(755,root,root) %{_bindir}/svm-train
%attr(755,root,root) %{_libdir}/libsvm.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsvm.so
%{_includedir}/svm.h

%if %{with octave}
%files -n octave-libsvm
%defattr(644,root,root,755)
%dir %{octave_oct_dir}/libsvm
%attr(755,root,root) %{octave_oct_dir}/libsvm/libsvmread.mex
%attr(755,root,root) %{octave_oct_dir}/libsvm/libsvmwrite.mex
%attr(755,root,root) %{octave_oct_dir}/libsvm/svmpredict.mex
%attr(755,root,root) %{octave_oct_dir}/libsvm/svmtrain.mex
%endif

%files -n python-libsvm
%defattr(644,root,root,755)
%{py_sitescriptdir}/svm.py
%{py_sitescriptdir}/svmutil.py
