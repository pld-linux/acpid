Summary:	ACPI Event Daemon
Summary(pl):	Demon zdarzeń ACPI
Name:		acpid
Version:	1.0.1
Release:	3
License:	GPL
Group:		Daemons
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/acpid/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
URL:		http://acpid.sourceforge.net/
Requires(post,preun):	/sbin/chkconfig
Obsoletes:	apmd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
acpid is a daemon that dispatches ACPI events to user-space programs.

%description -l pl
acpid to demon przekazujący zdarzenia ACPI do programów w user-space.

%prep
%setup -q

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{logrotate.d,rc.d/init.d,sysconfig},/var/log} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/acpi/{events,actions},%{_sbindir},%{_mandir}/man8}

install acpid $RPM_BUILD_ROOT/%{_sbindir}
install acpid.8 $RPM_BUILD_ROOT/%{_mandir}/man8
install samples/sample.conf $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/acpid
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/acpid
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/acpid
install samples/acpi_handler.sh $RPM_BUILD_ROOT%{_sbindir}/power.sh

> $RPM_BUILD_ROOT/var/log/acpid

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add acpid
if [ -f /var/lock/subsys/acpid ]; then
	/etc/rc.d/init.d/acpid restart >&2
else
	echo "Run \"/etc/rc.d/init.d/acpid start\" to start ACPI daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/acpid ]; then
		/etc/rc.d/init.d/acpid stop>&2
	fi
	/sbin/chkconfig --del acpid
fi

%files
%defattr(644,root,root,755)
%doc Changelog README
%dir %{_sysconfdir}/acpi
%dir %{_sysconfdir}/acpi/events
%dir %{_sysconfdir}/acpi/actions
%attr(640,root,root) %{_sysconfdir}/logrotate.d/acpid
%attr(754,root,root) /etc/rc.d/init.d/acpid
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/acpid
%config(noreplace,missingok) %verify(not size mtime md5) %{_sysconfdir}/acpi/events/sample.conf
%attr(755,root,root) %{_sbindir}/acpid
%attr(755,root,root) %{_sbindir}/power.sh
%attr(640,root,root) %ghost /var/log/acpid
%{_mandir}/man8/acpid.8.gz
