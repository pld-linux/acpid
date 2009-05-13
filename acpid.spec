Summary:	ACPI Event Daemon
Summary(pl.UTF-8):	Demon zdarzeń ACPI
Name:		acpid
Version:	1.0.6
Release:	7
License:	GPL v2+
Group:		Daemons
Source0:	http://dl.sourceforge.net/acpid/%{name}-%{version}.tar.gz
# Source0-md5:	5c9b705700df51d232be223b6ab6414d
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Source4:	%{name}.button.conf
Source5:	%{name}.battery.conf
Source6:	%{name}.button.sh
Source7:	%{name}.battery.sh
URL:		http://acpid.sourceforge.net/
# fix: upgrade to 1.0.10
BuildRequires:	security(CVE-2009-0798)
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Provides:	acpi-daemon
Obsoletes:	acpi-daemon
Obsoletes:	apm-daemon
ExclusiveArch:	%{ix86} %{x8664} ia64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
acpid is a daemon that dispatches ACPI events to user-space programs.

%description -l pl.UTF-8
acpid to demon przekazujący zdarzenia ACPI do programów w user-space.

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
demonowi ACPI wykonywanie operacji na podstawie przychodzących
zdarzeń ACPI (np. uruchomienie skryptu usypiającego system, gdy
użytkownik naciśnie przycisk zasilania).

Uwaga: na większości obecnych systemów NIE NALEŻY instalować tego
pakietu, gdyż za reagowanie na zdarzenia ACPI są w nich odpowiedzialne
inne programy (np. gnome-power-manager), więc ACPID by tylko
przeszkadzał. W takich przypadkach demon ACPI powinien działać
wyłącznie jako dyspozytor wiadomości.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS='-Wall -Werror %{rpmcflags} -D_GNU_SOURCE $(DEFS)'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{logrotate.d,rc.d/init.d,sysconfig},/var/log} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/acpi/{events,actions},%{_sbindir},%{_mandir}/man8}

install acpid $RPM_BUILD_ROOT%{_sbindir}
install acpid.8 $RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/acpid
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/acpid
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/acpid
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events/button.conf
install %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events/battery.conf
install %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/actions/button.sh
install %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/acpi/actions/battery.sh

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

%triggerpostun -- %{name} < 1.0.4-4
%banner -e %{name} << 'EOF'
Default configuration files have changed.
You might want to review your configuration in /etc/acpi
EOF

%files
%defattr(644,root,root,755)
%doc Changelog README TODO
%attr(755,root,root) %{_sbindir}/acpid
%dir %{_sysconfdir}/acpi
%dir %{_sysconfdir}/acpi/events
%dir %{_sysconfdir}/acpi/actions
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/acpid
%attr(754,root,root) /etc/rc.d/init.d/acpid
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/acpid
%attr(640,root,root) %ghost /var/log/acpid
%{_mandir}/man8/acpid.8*

%files policy
%defattr(644,root,root,755)
%config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/acpi/events/*.conf
%attr(754,root,root) %config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/acpi/actions/*.sh
