Summary:	ACPI Event Daemon
Summary(pl):	Demon zdarzeñ ACPI
Name:		acpid
Version:	1.0.0
Release:	1
License:	GPL
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/acpid/%{name}-%{version}.tar.gz
URL:		http://acpid.sourceforge.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
acpid is a daemon that dispatches ACPI events to user-space programs.

%description -l pl
acpid to demon przekazuj±cy zdarzenia ACPI do programów w user-space.

%prep
%setup -q

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT
%{__make} install INSTPREFIX=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/acpi/{events,actions},/var/log,/etc/rc.d/init.d}

install samples/sample.conf $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events
install redhat/acpid.init $RPM_BUILD_ROOT/etc/rc.d/init.d/acpid

touch $RPM_BUILD_ROOT/var/log/acpid

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add acpid

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del acpid
fi

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/acpi
%dir %{_sysconfdir}/acpi/events
%dir %{_sysconfdir}/acpi/actions
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/acpi/events/sample.conf
%attr(640,root,root) %ghost /var/log/acpid
%attr(755,root,root) %{_sbindir}/acpid
%attr(754,root,root) /etc/rc.d/init.d/acpid
%{_mandir}/man8/acpid.8.gz
