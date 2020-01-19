%define _hardened_build 1

Name: srptools
Version: 1.0.3
Release: 1%{?dist}
Summary: Tools for using the InfiniBand SRP protocol devices
Group: System Environment/Base
License: GPLv2 or BSD
Url: https://www.openfabrics.org/

Source0: https://www.openfabrics.org/downloads/%{name}/%{name}-%{version}.tar.gz
Source1: srptools.init
Source2: srptools.service
BuildRequires: libibumad-devel
BuildRequires: libibverbs-devel >= 1.2.0
BuildRequires: systemd
Requires(pre): systemd
Requires(preun): systemd
Requires(postun): systemd
ExcludeArch: s390
Obsoletes: openib-srptools <= 0.0.6

%description
In conjunction with the kernel ib_srp driver, srptools allows you to
discover and use SCSI devices via the SCSI RDMA Protocol over InfiniBand.

%package sysv
Summary: Back-compatible SysV Init script for srptools
Group: System Environment/Base
Requires(pre): chkconfig
Requires(preun): chkconfig /sbin/service

%description sysv
Backward compatible SysV Init script for srptools package

%prep
%setup -q

%build
%configure
make CFLAGS="$CXXFLAGS -fno-strict-aliasing" %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/etc/init.d/srpd
install -p -m 755 -D %{SOURCE1} %{buildroot}%{_initrddir}/srpd
install -p -m 644 -D %{SOURCE2} %{buildroot}%{_unitdir}/srpd.service

%post
%systemd_post srpd.service

%preun
%systemd_preun srpd.service

%postun
%systemd_postun_with_restart srpd.service

%post sysv
if [ $1 = 1 ]; then
    /sbin/chkconfig --add srpd
fi

%preun sysv
if [ $1 = 0 ]; then
    /sbin/service srpd stop
    /sbin/chkconfig --del srpd
fi

%files
%config(noreplace) %{_sysconfdir}/srp_daemon.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/srp_daemon
%config(noreplace) %{_sysconfdir}/rsyslog.d/srp_daemon.conf
%{_unitdir}/srpd.service
%{_sbindir}/ibsrpdm
%{_sbindir}/srp_daemon
%{_sbindir}/srp_daemon.sh
%{_sbindir}/run_srp_daemon
%{_mandir}/man1/ibsrpdm.1*
%{_mandir}/man1/srp_daemon.1*
%doc README NEWS ChangeLog
%license COPYING

%files sysv
%{_initrddir}/srpd

%changelog
* Tue Apr 12 2016 Honggang Li <honli@redhat.com> - 1.0.3-1
- Update to latest upstream version 1.0.3.
- Remove executable permission bits of srpd.service.
- Start srpd.service before remote-fs service.
- Resolves: bz1092530, bz1273181, bz1274119

* Fri Jul 17 2015 Doug Ledford <dledford@redhat.com> - 1.0.2-1
- Update to latest upstream release
- Resolves: bz1061931

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.0.4-18
- Mass rebuild 2013-12-27

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 05 2012 Doug Ledford <dledford@redhat.com> - 0.0.4-16
- Add native systemd support
- Resolves: bz884274

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul  4 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.0.4-14
- Enable building on ARM, modernise spec

* Tue Apr 24 2012 Doug Ledford <dledford@redhat.com> - 0.0.4-13
- Further tweaks to LSB init script headers
- Add a %%post and %%preun scriptlets to add/remove the init script

* Tue Feb 28 2012 Doug Ledford <dledford@redhat.com> - 0.0.4-12
- Fix minor issue in init script LSB headers

* Fri Jan 06 2012 Doug Ledford <dledford@redhat.com> - 0.0.4-11
- Initial import into Fedora

* Wed Jul 27 2011 Doug Ledford <dledford@redhat.com> - 0.0.4-10.el6
- Fix build on i686 arch
- Resolves: bz724900

* Thu Feb 03 2011 Doug Ledford <dledford@redhat.com> - 0.0.4-9.el6
- Add srpd init script
- Resolves: bz591169, bz658633, bz658674

* Mon Jan 25 2010 Doug Ledford <dledford@redhat.com> - 0.0.4-8.el6
- Update to latest upstream version so we can have an actual URL that works
- Fix ups for pkgwrangler import and also fix bug reported against rhel5
  version of package (552915)
- Related: bz543948

* Tue Dec 22 2009 Doug Ledford <dledford@redhat.com> - 0.0.4-7.el5
- Bump and rebuild against new libibumad
- Related: bz518218

* Mon Jun 22 2009 Doug Ledford <dledford@redhat.com> - 0.0.4-6.el5
- Rebuild against libibverbs that isn't missing the proper ppc wmb() macro
- Related: bz506258

* Sun Jun 21 2009 Doug Ledford <dledford@redhat.com> - 0.0.4-5.el5
- Build against non-XRC libibverbs
- Update to ofed 1.4.1 final bits
- Related: bz506258, bz506097

* Fri Apr 24 2009 Doug Ledford <dledford@redhat.com> - 0.0.4-4.el5
- Add -fno-strict-aliasing to CFLAGS

* Sat Apr 18 2009 Doug Ledford <dledford@redhat.com> - 0.0.4-3.el5
- Bump and rebuild against updated libibverbs and libibumad
- Related: bz459652

* Tue Apr 01 2008 Doug Ledford <dledford@redhat.com> - 0.0.4-2
- Update to OFED 1.3 final bits
- Related: bz428197

* Tue Jan 29 2008 Doug Ledford <dledford@redhat.com> - 0.0.4-1
- Import upstream srptools and obsolete old openib-srptools package
- Related: bz428197

