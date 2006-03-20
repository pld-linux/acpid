# TODO:
# - better event handling in power.sh
# - better default configuration of events in /etc/acpi
# - processor and fan module support (?)
Summary:	ACPI Event Daemon
Summary(pl):	Demon zdarzeñ ACPI
Name:		acpid
Version:	1.0.4
Release:	3
License:	GPL v2
Group:		Daemons
Source0:	http://dl.sourceforge.net/acpid/%{name}-%{version}.tar.gz
# Source0-md5:	3aff94e92186e99ed5fd6dcee2db7c74
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Source4:	%{name}.halt_on_power_button.conf
Patch0:		%{name}-powersh_fix.patch
Patch1:		%{name}-gcc4.patch
URL:		http://acpid.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Obsoletes:	apmd
Obsoletes:	poweracpid
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
acpid is a daemon that dispatches ACPI events to user-space programs.

%description -l pl
acpid to demon przekazuj±cy zdarzenia ACPI do programów w user-space.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{logrotate.d,rc.d/init.d,sysconfig},/var/log} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/acpi/{events,actions},%{_sbindir},%{_mandir}/man8}

install acpid $RPM_BUILD_ROOT%{_sbindir}
install acpid.8 $RPM_BUILD_ROOT%{_mandir}/man8
install samples/sample.conf $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/acpid
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/acpid
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/acpid
install samples/acpi_handler.sh $RPM_BUILD_ROOT%{_sbindir}/power.sh
# Or create halt_on_power_button subpackage
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events

> $RPM_BUILD_ROOT/var/log/acpid

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add acpid
%service acpid restart "ACPI daemon"

%preun
if [ "$1" = "0" ]; then
	%service acpid stop
	/sbin/chkconfig --del acpid
fi

# %%post halt_on_power_button
# %%service -q acpid reload

# %%postun halt_on_power_button
# %%service -q acpid reload

%files
%defattr(644,root,root,755)
%doc Changelog README TODO
%dir %{_sysconfdir}/acpi
%dir %{_sysconfdir}/acpi/events
%dir %{_sysconfdir}/acpi/actions
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/acpid
%attr(754,root,root) /etc/rc.d/init.d/acpid
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/acpid
%config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/acpi/events/*.conf
%attr(755,root,root) %{_sbindir}/acpid
%attr(755,root,root) %{_sbindir}/power.sh
%attr(640,root,root) %ghost /var/log/acpid
%{_mandir}/man8/acpid.8*
