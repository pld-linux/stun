Summary:	Simple Traversal of UDP through NATs
Summary(pl):	STUN - Proste Przepuszczanie UDP przez NAT-a
Name:		stun
Version:	0.94
Release:	1
Group:		Networking/Daemons
License:	Vovida Software License
Source0:	http://dl.sourceforge.net/stun/stund_%{version}_Oct29.tgz
# Source0-md5:	5c5b1b206c9f9d8fdbb826a83da1fb0e
Source1:	%{name}.sysconfig
Source2:	%{name}.init
URL:		http://www.vovida.org/applications/downloads/stun/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The STUN (Simple Traversal of UDP through NATs (Network Address
Translation)) server is an implementation of the STUN protocol that
enables STUN functionality in SIP-based systems.

%description -l pl
Serwer STUN (prostego przepuszczania UDP przez NAT-a) jest
implementacj± protoko³u STUN, który umo¿liwia wykorzystanie systemów
opartych na protokole SIP w sieciach za NAT-em.

%package server
Summary:	Simple Traversal of UDP through NATs server
Summary(pl):	Serwer STUN (prostego przepuszczania UDP przez NAT-a)
Group:		Networking/Daemons

%description server
The STUN (Simple Traversal of UDP through NATs (Network Address
Translation)) server is an implementation of the STUN protocol that
enables STUN functionality in SIP-based systems.

%description server -l pl
Serwer STUN (prostego przepuszczania UDP przez NAT-a) jest
implementacj± protoko³u STUN, który umo¿liwia wykorzystanie systemów
opartych na protokole SIP w sieciach za NAT-em.

%package client
Summary:	Simple Traversal of UDP through NATs client
Summary(pl):	Klient STUN (prostego przepuszczania UDP przez NAT-a)
Group:		Networking/Utilities

%description client
A simple client for testing a STUN server.

%description client -l pl
Prosty klient do testowania serwerów STUN.

%prep
%setup -q -n stund

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},/etc/{rc.d/init.d,sysconfig}}

install server $RPM_BUILD_ROOT%{_sbindir}/stund
install client $RPM_BUILD_ROOT%{_bindir}/stunc
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/stund
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/stund

%clean
rm -rf $RPM_BUILD_ROOT

%post server
/sbin/chkconfig --add stund
if [ -f /var/lock/subsys/stund ]; then
        /etc/rc.d/init.d/stund restart >&2
else
        echo "Run \"/etc/rc.d/init.d/stund start\" to start STUN server daemon."
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/stund ]; then
                /etc/rc.d/init.d/stund stop >&2
        fi
        /sbin/chkconfig --del stund
fi


%files server
%defattr(644,root,root,755)
%doc rfc3489.txt
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/stund
%attr(640,root,root) %config(noreplace) %verify(not size md5 mtime) /etc/sysconfig/stund

%files client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
