Name:		firewall-compiler
Version:	2
Release:	2%{?dist}
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
install -d -m 755 $RPM_BUILD_ROOT/etc/firewall/rules.enabled
install -d -m 755 $RPM_BUILD_ROOT%{_bindir}

python setup.py install --root=$RPM_BUILD_ROOT

ln -s fwc-tool $RPM_BUILD_ROOT%{_bindir}/fwc-enable
ln -s fwc-tool $RPM_BUILD_ROOT%{_bindir}/fwc-disable

install -m 644 master.tmpl $RPM_BUILD_ROOT/etc/firewall
install -m 644 fwc.conf $RPM_BUILD_ROOT/etc/firewall

for x in rules.d/*.rules; do
	install -m 644 $x $RPM_BUILD_ROOT/etc/firewall/rules.d
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README.rst

/etc/firewall/master.tmpl
%config(noreplace) /etc/firewall/fwc.conf

%dir /etc/firewall/rules.enabled
/etc/firewall/rules.d/*.rules

/usr/lib
%{_bindir}/fwc
%{_bindir}/fwc-tool
%{_bindir}/fwc-enable
%{_bindir}/fwc-disable

%changelog

