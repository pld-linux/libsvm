#
# Conditional build:
%bcond_without	java	# Java library
%bcond_without	octave	# Octave (MATLAB) module
%bcond_without	python	# Python (any) interface
%bcond_without	python2	# Python 2.x interface
%bcond_without	python3	# Python 3.x interface
#
%if %{without python}
%undefine	with_python2
%undefine	with_python3
%endif
Summary:	LIBSVM - simple, easy-to-use and efficient software for SVM classification and regression
Summary(pl.UTF-8):	LIBSVM - proste, łatwe w użyciu i wydajne oprogramowanie do klasyfikacji i regresji SVM
Name:		libsvm
Version:	3.24
Release:	5
License:	BSD
Group:		Libraries
Source0:	https://www.csie.ntu.edu.tw/~cjlin/libsvm/%{name}-%{version}.tar.gz
# Source0-md5:	818aa0201dc9d938846a6394653915f4
Patch0:		%{name}-python.patch
Patch1:		%{name}-make.patch
URL:		https://www.csie.ntu.edu.tw/~cjlin/libsvm/
%{?with_java:BuildRequires:	jdk >= 1.7}
BuildRequires:	libstdc++-devel
%{?with_java:BuildRequires:	m4}
%{?with_octave:BuildRequires:	octave-devel}
%{?with_python2:BuildRequires:	python-devel >= 1:2.6}
%{?with_python3:BuildRequires:	python3-devel >= 1:3.2}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.507
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

%package -n java-libsvm
Summary:	Java interface for LIBSVM library
Summary(pl.UTF-8):	Interfejs Javy do biblioteki LIBSVM
Group:		Libraries/Python
Requires:	jre >= 1.7

%description -n java-libsvm
Java interface for LIBSVM library.

%description -n java-libsvm -l pl.UTF-8
Interfejs Javy do biblioteki LIBSVM.

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
Summary:	Python 2 interface for LIBSVM library
Summary(pl.UTF-8):	Interfejs Pythona 2 do biblioteki LIBSVM
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-libs >= 1:2.6

%description -n python-libsvm
Python 2 interface for LIBSVM library.

%description -n python-libsvm -l pl.UTF-8
Interfejs Pythona 2 do biblioteki LIBSVM.

%package -n python3-libsvm
Summary:	Python 3 interface for LIBSVM library
Summary(pl.UTF-8):	Interfejs Pythona 3 do biblioteki LIBSVM
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-libs >= 1:3.2

%description -n python3-libsvm
Python 3 interface for LIBSVM library.

%description -n python3-libsvm -l pl.UTF-8
Interfejs Pythona 3 do biblioteki LIBSVM.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# probably it was meant to be shared between liblinear and libsvm interfaces,
# but it's impossible to keep in sync at distro level between different
# versions of both packages (see python patch for changes in sources)
%{__mv} python/{commonutil,svmcommonutil}.py

%build
%{__make} \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} -fPIC -Wall"

%if %{with java}
%{__make} -C java
%endif

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
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir}}

install libsvm.so.* $RPM_BUILD_ROOT%{_libdir}
ln -sf $(basename $RPM_BUILD_ROOT%{_libdir}/libsvm.so.*) $RPM_BUILD_ROOT%{_libdir}/libsvm.so
cp -p svm.h $RPM_BUILD_ROOT%{_includedir}
install svm-predict svm-scale svm-train $RPM_BUILD_ROOT%{_bindir}

%if %{with java}
install -D java/libsvm.jar $RPM_BUILD_ROOT%{_javadir}/libsvm.jar
%endif

%if %{with octave}
install -d $RPM_BUILD_ROOT%{octave_oct_dir}/libsvm
install matlab/*.mex $RPM_BUILD_ROOT%{octave_oct_dir}/libsvm
%endif

%if %{with python2}
install -d $RPM_BUILD_ROOT%{py_sitescriptdir}
cp -p python/*.py $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean
%endif

%if %{with python3}
install -d $RPM_BUILD_ROOT%{py3_sitescriptdir}
cp -p python/*.py $RPM_BUILD_ROOT%{py3_sitescriptdir}
%py3_comp $RPM_BUILD_ROOT%{py3_sitescriptdir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitescriptdir}
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

%if %{with java}
%files -n java-libsvm
%defattr(644,root,root,755)
%{_javadir}/libsvm.jar
%endif

%if %{with octave}
%files -n octave-libsvm
%defattr(644,root,root,755)
%dir %{octave_oct_dir}/libsvm
%attr(755,root,root) %{octave_oct_dir}/libsvm/libsvmread.mex
%attr(755,root,root) %{octave_oct_dir}/libsvm/libsvmwrite.mex
%attr(755,root,root) %{octave_oct_dir}/libsvm/svmpredict.mex
%attr(755,root,root) %{octave_oct_dir}/libsvm/svmtrain.mex
%endif

%if %{with python2}
%files -n python-libsvm
%defattr(644,root,root,755)
%doc python/README
%{py_sitescriptdir}/svm.py[co]
%{py_sitescriptdir}/svmcommonutil.py[co]
%{py_sitescriptdir}/svmutil.py[co]
%endif

%if %{with python3}
%files -n python3-libsvm
%defattr(644,root,root,755)
%doc python/README
%{py3_sitescriptdir}/svm.py
%{py3_sitescriptdir}/svmcommonutil.py
%{py3_sitescriptdir}/svmutil.py
%{py3_sitescriptdir}/__pycache__/svm.cpython-*.py[co]
%{py3_sitescriptdir}/__pycache__/svmcommonutil.cpython-*.py[co]
%{py3_sitescriptdir}/__pycache__/svmutil.cpython-*.py[co]
%endif
