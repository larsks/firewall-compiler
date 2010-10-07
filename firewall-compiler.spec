Name:		firewall-compiler
Version:	1
Release:	1%{?dist}
Summary:	Build an iptables firewall from modules.

Group:		SEAS
License:	BSD
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires:	python
Requires:	python-cheetah
Requires:	iptables

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

for rule in rules.d/*; do
	install -m 644 $rule $RPM_BUILD_ROOT/etc/firewall/rules.d/
done

install -m 644 master.tmpl $RPM_BUILD_ROOT/etc/firewall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc

%config(noreplace) /etc/firewall/master.tmpl
%config(noreplace) /etc/firewall/rules.d/*

/usr/lib
%{_bindir}/fwc

%changelog

