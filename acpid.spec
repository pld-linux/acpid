# TODO:
# - better event handling in power.sh
# - better default configuration of events in /etc/acpi
# - processor and fan module support (?)
# - run-parts(8)-like [A-Z...] regexp from Debian for config scan is evil as it
#   is locale dependant (http://www.gentoo.org/news/en/gwn/20060522-newsletter.xml#doc_chap2)
#   also it does not allow *.conf files (missing "."), which is not backward
#   compatible (custom files can be left unprocessed)
#   but if patch is made to allow ".", must consider to ignore .rpm{new,old,save} files
Summary:	ACPI Event Daemon
Summary(pl.UTF-8):	Demon zdarzeń ACPI
Name:		acpid
Version:	2.0.34
Release:	1
License:	GPL v2+
Group:		Daemons
Source0:	http://downloads.sourceforge.net/acpid2/%{name}-%{version}.tar.xz
# Source0-md5:	988c2e3fd5ba0ea4492d3ba7273af295
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Source4:	%{name}.button.conf
Source5:	%{name}.battery.conf
Source6:	%{name}.button.sh
Source7:	%{name}.battery.sh
Source9:	%{name}.service
Source10:	%{name}.preconfig
URL:		http://sourceforge.net/projects/acpid2/
BuildRequires:	rpmbuild(macros) >= 1.647
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	rc-scripts >= 0.4.3.0
Requires:	systemd-units >= 38
Provides:	acpi-daemon
Obsoletes:	acpi-daemon
Obsoletes:	apm-daemon
ExclusiveArch:	%{ix86} %{x8664} x32 ia64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
acpid is a daemon that dispatches ACPI events to user-space programs.

%description -l pl.UTF-8
acpid to demon przekazujący zdarzenia ACPI do programów w przestrzeni
użytkownika.

%package policy
Summary:	ACPID policy files
Summary(pl.UTF-8):	Pliki z polityką dla ACPID
Group:		Daemons
Requires:	%{name} = %{version}-%{release}

%description policy
This package contains scripts and configuration files which allow
ACPID to take action on incoming ACPI events (eg. to run a script that
suspends the system when the power button is pressed).

Notice: on most current systems you DO NOT want this package
installed, since there are other software packages responsible for
handling ACPI events (one example being gnome-power-manager) and
having ACPID also respond will lead to problems. In such cases ACPID
should only act as a message broker.

%description policy -l pl.UTF-8
Ten pakiet zawiera skrypty i pliki konfiguracyjne, które umożliwiają
demonowi ACPI wykonywanie operacji na podstawie przychodzących zdarzeń
ACPI (np. uruchomienie skryptu usypiającego system, gdy użytkownik
naciśnie przycisk zasilania).

Uwaga: na większości obecnych systemów NIE NALEŻY instalować tego
pakietu, gdyż za reagowanie na zdarzenia ACPI są w nich odpowiedzialne
inne programy (np. gnome-power-manager), więc ACPID by tylko
przeszkadzał. W takich przypadkach demon ACPI powinien działać
wyłącznie jako dyspozytor wiadomości.

%prep
%setup -q

%build
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{logrotate.d,rc.d/init.d,sysconfig,init},/var/log} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/acpi/{events,actions},%{systemdunitdir}} \
	$RPM_BUILD_ROOT%{_datadir}/%{name}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/acpid
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/acpid
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/acpid
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events/button
cp -p %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events/battery
install -p %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/actions/button.sh
install -p %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/actions/battery.sh
install %{SOURCE9} $RPM_BUILD_ROOT%{systemdunitdir}
install %{SOURCE10} $RPM_BUILD_ROOT%{_datadir}/%{name}

> $RPM_BUILD_ROOT/var/log/acpid
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add acpid
%service acpid restart "ACPI daemon"
%systemd_post acpid.service

%preun
if [ "$1" = "0" ]; then
	%service acpid stop
	/sbin/chkconfig --del acpid
fi
%systemd_preun acpid.service

%postun
%systemd_reload

%triggerpostun -- %{name} < 2.0.10-12
if [ -f /etc/sysconfig/acpid ]; then
	. /etc/sysconfig/acpid
	__PROGRAM_ARGS=
	[ "$NETLINK" = "yes" ] && __PROGRAM_ARGS="-n"
	[ -n "$CLIENTMAX" ] && __PROGRAM_ARGS="$__PROGRAM_ARGS -C $CLIENTMAX"
	if [ -n "$__PROGRAM_ARGS" ]; then
		%{__cp} -f /etc/sysconfig/acpid{,.rpmsave}
		echo >>/etc/sysconfig/acpid
		echo "# Added by rpm trigger" >>/etc/sysconfig/acpid
		echo "PROGRAM_ARGS=\"$PROGRAM_ARGS $__PROGRAM_ARGS\"" >>/etc/sysconfig/acpid
	fi
fi
%systemd_trigger acpid.service

%files
%defattr(644,root,root,755)
%doc Changelog README TESTPLAN TODO
%attr(755,root,root) %{_sbindir}/acpid
%attr(755,root,root) %{_sbindir}/kacpimon
%attr(755,root,root) %{_bindir}/acpi_listen
%dir %{_sysconfdir}/acpi
%dir %{_sysconfdir}/acpi/events
%dir %{_sysconfdir}/acpi/actions
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/acpid
%attr(754,root,root) /etc/rc.d/init.d/acpid
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/acpid
%{systemdunitdir}/acpid.service
%attr(640,root,root) %ghost /var/log/acpid
%{_mandir}/man8/acpid.8*
%{_mandir}/man8/acpi_listen.8*
%{_mandir}/man8/kacpimon.8*
%dir %{_datadir}/%{name}
%attr(755,root,root) %{_datadir}/%{name}/acpid.preconfig

%files policy
%defattr(644,root,root,755)
%config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/acpi/events/button
%config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/acpi/events/battery
%attr(754,root,root) %config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/acpi/actions/*.sh
