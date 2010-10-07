Name:		firewall-compiler
Version:	1
Release:	3%{?dist}
Summary:	Build an iptables firewall from modules.

Group:		SEAS
License:	BSD
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires:	python
Requires:	python-cheetah
Requires:	iptables

Buildarch:	noarch
Buildrequires:	python-setuptools

%description
Build an iptables firewall from modules.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT/etc/firewall
install -d -m 755 $RPM_BUILD_ROOT/etc/firewall/rules.d
install -d -m 755 $RPM_BUILD_ROOT%{_bindir}

python setup.py install --root=$RPM_BUILD_ROOT

install -m 644 master.tmpl $RPM_BUILD_ROOT/etc/firewall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc rules.d/*

%config(noreplace) /etc/firewall/master.tmpl

/usr/lib
%{_bindir}/fwc

%changelog

