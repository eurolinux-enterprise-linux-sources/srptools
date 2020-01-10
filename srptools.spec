Name: srptools
Version: 1.0.2
Release: 1%{?dist}
Summary: Tools for using the InfiniBand SRP protocol devices
Group: System Environment/Base
License: GPLv2 or BSD
Url: http://www.openfabrics.org/
Source0: http://www.openfabrics.org/downloads/%{name}/%{name}-%{version}.tar.gz
Source1: srptools.init
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libibumad-devel, libibverbs-devel > 1.1.3
Requires(post): chkconfig
Requires(preun): chkconfig
ExcludeArch: s390 s390x
Obsoletes: openib-srptools <= 0.0.6

%description
In conjunction with the kernel ib_srp driver, srptools allows you to
discover and use SCSI devices via the SCSI RDMA Protocol over InfiniBand.

%prep
%setup -q

%build
%configure
make CFLAGS="$CFLAGS -fno-strict-aliasing" %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
# Remove the installed srpd script before installing our own
rm -f %{buildroot}%{_sysconfdir}/init.d/srpd
install -p -m 755 -D %{SOURCE1} %{buildroot}%{_initrddir}/srpd

%clean
rm -rf %{buildroot}

%post
if [ $1 = 1 ]; then
    /sbin/chkconfig --add srpd
fi

%preun
if [ $1 = 0 ]; then
    /sbin/chkconfig --del srpd
fi

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/srp_daemon.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/srp_daemon
%config(noreplace) %{_sysconfdir}/rsyslog.d/srp_daemon.conf
%{_initrddir}/srpd
%{_sbindir}/ibsrpdm
%{_sbindir}/srp_daemon
%{_sbindir}/srp_daemon.sh
%{_sbindir}/run_srp_daemon
%{_mandir}/man1/ibsrpdm.1*
%{_mandir}/man1/srp_daemon.1*
%doc README NEWS ChangeLog COPYING

%changelog
* Wed Jun 18 2014 Doug Ledford <dledford@redhat.com> - 1.0.2-1
- Update to latest upstream release
- Resolves: bz1055654

* Tue May 01 2012 Doug Ledford <dledford@redhat.com> - 0.0.4-15.el6
- Another fix to init script
- Resolves: bz817194

* Fri Apr 27 2012 Doug Ledford <dledford@redhat.com> - 0.0.4-14.el6
- Fix for fix to init script
- Related: bz816087

* Thu Apr 26 2012 Doug Ledford <dledford@redhat.com> - 0.0.4-13.el6
- Need to background the srp_daemon.sh script in our init script, as
  srp_daemon.sh doesn't return until killed
- Resolves: bz816087

* Tue Apr 24 2012 Doug Ledford <dledford@redhat.com> - 0.0.4-12.el6
- Can't use %%{name} macro in the %%post and %%preun as the service
  name is srpd while the package name is srptools
- Related: bz815215

* Mon Apr 23 2012 Doug Ledford <dledford@redhat.com> - 0.0.4-11.el6
- Add the init script even though it isn't enabled by default
- Fix the init script's usage of srp_daemon.conf
- Resolves: bz815215, bz815234

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

