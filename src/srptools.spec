
Name: srptools
Version: 1.0.3
Release: 1%{?dist}
Summary: Tools for SRP/IB

Group: Applications/System
License: GPL/BSD
Url: http://www.openfabrics.org/
Source: http://www.openfabrics.org/downloads/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
In conjunction with the kernel ib_srp driver, srptools allows you to
discover and use SCSI devices via the SCSI RDMA Protocol over InfiniBand.

%prep
rm -rf $RPM_BUILD_ROOT
%setup -q -n %{name}-%{version}

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 = 1 ]; then # 1 : This package is being installed for the first time
    for ib_conf_file in /etc/infiniband/openib.conf /etc/rdma/rdma.conf; do
	if [ -e $ib_conf_file ] &&
	    ! grep -q '^SRPHA_ENABLE=' $ib_conf_file; then
	    cat <<EOF >>$ib_conf_file

# Enable SRP High Availability daemon
SRPHA_ENABLE=no
SRP_DAEMON_ENABLE=no
EOF
	fi
    done
    if [ -e /sbin/chkconfig ]; then
        /sbin/chkconfig --add srpd
    elif [ -e /usr/sbin/update-rc.d ]; then
        /usr/sbin/update-rc.d srpd defaults
    else
        /usr/lib/lsb/install_initd /etc/init.d/srpd
    fi
fi
if type systemctl >/dev/null 2>&1; then
    systemctl --system daemon-reload
fi
if [ $1 != 1 ]; then
    /etc/init.d/srpd condrestart
fi

%preun
if [ $1 = 0 ]; then
    pidfile=/var/run/srp_daemon.sh.pid
    if [[ -f "$pidfile" && -e "/proc/$(cat $pidfile)" ]]; then
        /etc/init.d/srpd stop
    fi
    if [ -e /sbin/chkconfig ]; then
        /sbin/chkconfig --del srpd
    elif [ -e /usr/sbin/update-rc.d ]; then
        /usr/sbin/update-rc.d -f srpd remove
    else
        /usr/lib/lsb/remove_initd /etc/init.d/srpd
    fi
fi

%files
%defattr(-,root,root)
%config(noreplace) /etc/srp_daemon.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/srp_daemon
%config(noreplace) %{_sysconfdir}/rsyslog.d/srp_daemon.conf
%{_sysconfdir}/init.d/srpd
%{_sbindir}/ibsrpdm
%{_sbindir}/run_srp_daemon
%{_sbindir}/srp_daemon
%{_sbindir}/srp_daemon.sh
%{_mandir}/man1/ibsrpdm.1*
%{_mandir}/man1/srp_daemon.1*
%doc README NEWS ChangeLog COPYING

%changelog
* Wed Feb 11 2015 Bart Van Assche <bart.vanassche@sandisk.com> - 1.0.3
- srp_daemon: Survive catastrophic HCA errors.
- srp_daemon: Fix ib_dev name and port assignments for non-default umad devices.
- srp_daemon: Add support for allow_ext_sg, cmd_sg_entries and sg_tablesize
  in /etc/srp_daemon.conf.
- srp_daemon: Reduce time needed to stop.
- srp_daemon: Log start and end of trap deregistration.
- srp_daemon: Avoid that clang complains about an invalid conversion specifier.
- srp_daemon: Fix memory leaks in error paths.
- ibsrpdm: Do not start trap threads in ibsrpdm.
- configure.ac: Add subdir-objects to AM_INIT_AUTOMAKE.
- srptools.spec: Avoid redundant stop in pre-uninstall.
- Debian: Fix build-deb.sh to read version from configure.ac.
- Debian: Fix package build.
* Thu Feb 20 2014 Bart Van Assche <bvanassche@acm.org> - 1.0.2
- Added support for specifying tl_retry_count in srp_daemon.conf. Changed
  default behavior for tl_retry_timeout parameter from setting it to 2 into
  leaving it at its default value (7). This makes srp_daemon again compatible
  with the SRP initiator driver from kernel 3.12 and before.
* Mon Feb 03 2014 Bart Van Assche <bvanassche@acm.org> - 1.0.1
- Make process uniqueness check work.
- Unsubscribe from subnet manager for traps before exiting.
- Added support for the comp_vector and queue_size configuration file options.
* Tue Dec 24 2013 Sagi Grimberg and Bart Van Assche - 1.0.0
- srp_daemon keeps working even if the LID changes of the port it is using to
  scan the fabric or if a P_Key change occurs.
- Added P_Key support to srp_daemon and ibsrpdm.
- Fixed month in srp_daemon.log (OFED bug \#2281). srp_daemon now uses syslog
  and logrotate for logging.
- srp_daemon is now only started for InfiniBand ports. It is no longer
  attempted to start srp_daemon on Ethernet ports.
- Added support for specifying the tl_retry_count parameter. By default use
  tl_retry_count=2.
- Allow srp_daemon to be started without configuration file.
- Fixed a memory leak in srp_daemon that was triggered once during every fabric
  rescan.
- Reduced memory consumption of the srp_daemon process.
- MAD transaction ID 0 is skipped after 2**32 rescans.
- Installation: SRPHA_ENABLE=no / SRP_DAEMON_ENABLE=no is only added to
  /etc/infiniband/openibd.conf if these variables did not yet exist in that
  file.
- Changed range of the srp_daemon and ibsrpdm exit codes from 0..127 into 0..1.
- Changed ibsrpdm such that it uses the new umad P_Key ABI. Running ibsrpdm
  does no longer cause a warning to be logged ("user_mad: process ibsrpdm did
  not enable P_Key index support / user_mad:
  Documentation/infiniband/user_mad.txt has info on the new ABI").
- Fixed spelling of several help texts and diagnostic messages.
* Wed Aug 22 2007 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Added srp_daemon.conf
* Tue Sep  5 2006 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Added srp_daemon and scripts to execute this daemon
* Tue Mar 21 2006 Roland Dreier <rdreier@cisco.com> - 0.0.4-1
- Initial attempt at a working spec file
