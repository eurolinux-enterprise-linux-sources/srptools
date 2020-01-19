
Name: srptools
Version: 0.0.4
Release: 0.1.gce1f64c
Summary: Tools for SRP/IB

Group: Applications/System
License: GPL/BSD
Url: http://www.openfabrics.org/
Source: http://www.openfabrics.org/downloads/srptools-0.0.4-0.1.gce1f64c.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%{!?IB_CONF_DIR: %define IB_CONF_DIR /etc/infiniband}

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
    if [ -e %{IB_CONF_DIR}/openib.conf ]; then
       echo >> %{IB_CONF_DIR}/openib.conf
       echo "# Enable SRP High Availability daemon" >> %{IB_CONF_DIR}/openib.conf
       echo "SRPHA_ENABLE=no" >> %{IB_CONF_DIR}/openib.conf
       echo "SRP_DAEMON_ENABLE=no" >> %{IB_CONF_DIR}/openib.conf
    fi
fi

%files
%defattr(-,root,root)
%config(noreplace) /etc/srp_daemon.conf
%{_sbindir}/ibsrpdm
%{_sbindir}/srp_daemon
%{_sbindir}/srp_daemon.sh
%{_sbindir}/run_srp_daemon
%{_mandir}/man1/ibsrpdm.1*
%{_mandir}/man1/srp_daemon.1*
%doc README NEWS ChangeLog COPYING

%changelog
* Wed Aug 22 2007 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Added srp_daemon.conf
* Tue Sep  5 2006 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Added srp_daemon and scripts to execute this daemon
* Tue Mar 21 2006 Roland Dreier <rdreier@cisco.com> - 0.0.4-1
- Initial attempt at a working spec file
