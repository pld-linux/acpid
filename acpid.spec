Summary: ACPI Event Daemon
Name: acpid
Version: 1.0.0
Release: 1
Copyright: GPL
Group: Daemons
Source: acpid-1.0.0.tar.gz
BuildRoot: /var/tmp/acpid
URL: http://acpid.sourceforge.net


%description
acpid is a daemon that dispatches ACPI events to user-space programs.


%changelog
* Thu Aug 16 2001  Tim Hockin <thockin@sun.com>
  - Added commandline options to actions

* Wed Aug 15 2001  Tim Hockin <thockin@sun.com>
  - Added UNIX domain socket support
  - Changed /etc/acpid.d to /etc/acpid/events

* Mon Aug 13 2001  Tim Hockin <thockin@sun.com>
  - added changelog
  - 0.99.1-1

%prep
%setup


%build
make


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make install INSTPREFIX=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/acpi/events
mkdir -p $RPM_BUILD_ROOT/etc/acpi/actions
chmod 755 $RPM_BUILD_ROOT/etc/acpi/events
install -o root -g root -m 644 samples/sample.conf \
	$RPM_BUILD_ROOT/etc/acpi/events

mkdir -p $RPM_BUILD_ROOT/var/log
touch $RPM_BUILD_ROOT/var/log/acpid
chmod 640 $RPM_BUILD_ROOT/var/log/acpid

mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -o root -g root redhat/acpid.init $RPM_BUILD_ROOT/etc/rc.d/init.d/acpid
chmod 755 $RPM_BUILD_ROOT/etc/rc.d/init.d/acpid


%files
%defattr(-,root,root)
%dir /etc/acpi
%dir /etc/acpi/events
%dir /etc/acpi/actions
/etc/acpi/events/sample.conf
/var/log/acpid
/usr/sbin/acpid
/etc/rc.d/init.d/acpid
/usr/share/man/man8/acpid.8.gz


%post
# only run on install, not upgrade 
if [ "$1" = "1" ]; then
	/sbin/chkconfig --add acpid
fi


%preun
# only run if this is the last instance to be removed
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del acpid
fi
