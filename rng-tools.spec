Summary:        Random number generator related utilities
Name:           rng-tools
Version:	6.3.1
Release:        3%{?dist}
Group:          System Environment/Base
License:        GPLv2+
URL:            http://sourceforge.net/projects/gkernel/
# Note, need to update this next release to point to the new upstream
# https://github.com/ricardon/rng-tools
Source0:        http://downloads.sourceforge.net/project/gkernel/rng-tools/5/rng-tools-%{version}.tar.gz
Source1:        rngd.service
Source2:        jitterentropy-library-3f7b6cc.tar.gz


# Man pages
Patch0:         jitterentropy-remove-install.patch
Patch1:		rngd-quiet.patch
Patch2:		tpm-deprecate-tpm-entropy_source.patch

BuildRequires:  gettext
BuildRequires:  systemd-units
BuildRequires: libgcrypt-devel
BuildRequires: autoconf automake
BuildRequires: libsysfs-devel libcurl-devel
BuildRequires: libxml2-devel openssl-devel
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires: libgcrypt libsysfs
Requires: openssl libxml2 libcurl

%description
Hardware random number generation tools.

%prep
%setup -q
tar xvf %{SOURCE2}
%patch0 -p1 -b .rminstall
%patch1 -p1 -b .quiet
%patch2 -p1 -b .tpm

%build
./autogen.sh
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

# install systemd unit file
mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE1} %{buildroot}%{_unitdir}

%post
%systemd_post rngd.service

%preun
%systemd_preun rngd.service

%postun
%systemd_postun_with_restart rngd.service

%files
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/rngtest
%{_sbindir}/rngd
%{_mandir}/man1/rngtest.1.*
%{_mandir}/man8/rngd.8.*
%attr(0644,root,root)   %{_unitdir}/rngd.service

%changelog
* Wed Sep 12 2018 Neil Horman <nhorman@redhat.com> -6.3.1-3
- Deprecate tpm entropy source (bz 1627822)

* Mon Jul 30 2018 Neil Horman <nhorman@redhat.com> -6.3.1-2
- Fix quiet option (bz 1609888)

* Tue Jul 17 2018 Neil Horman <nhorman@redhat.com> - 6.3.1-1
- Update to latest upstream

* Mon Apr 09 2018 Neil Horman <nhorman@redhat.com> - 5.15
- Reconcile man page discrepancy properly (bz 1558616)

* Wed Mar 21 2018 Neil Horman <nhorman@redhat.com> - 5.14
- Rectify man page discrepancy (bz 1558616)
- Make quiet behave as it ought to (bz 1558616)

* Thu Nov 09 2017 Neil Horman <nhorman@redhat.com> - 5.13
- Add Power DARN support (bz 1473033)

* Tue Aug 29 2017 Neil Horman <nhorman@redhat.com> - 5.12
- Fix read error (bz 1464200)

* Wed May 31 2017 Neil Horman <nhorman@redhat.com> - 5.11
- Fix initializtion of alternate entropy sources (bz 1454731)

* Wed Apr 19 2017 Jerry Snitselaar <jsnitsel@redhat.com> - 5.10
- Check for whether there is available rng during init (bz 1421234)

* Tue Apr 11 2017 Neil Horman <nhorman@redhat.com> - 5.9
- Fixed verbose behavior (bz 1437044)

* Mon Aug 17 2015 Neil Horman <nhorman@redhat.com> - 5.8
- Fixed man page (bz 1254223)

* Mon Jun 08 2015 Neil Horman <nhorman@redhat.com> - 5.7
- Added entropy limit option (bz 1211406)

* Thu May 28 2015 Neil Horman <nhorman@redhat.com> - 5.6
- Updating spec file (bz 1225175)

* Thu May 28 2015 Neil Horman <nhorman@redhat.com> - 5.5
- Update rngtest man page (bz 1225175)

* Wed Apr 08 2015 Neil Horman <nhorman@redhat.com> - 5.4
- Use real rdrand instructions

* Tue Mar 10 2015 Neil Horman <nhorman@redhat.com> - 5.3
- Fixed man page (bz 1178871)

* Fri Aug 22 2014 Neil Horman <nhorman@redhat.com> - 5.2
- Uploaded new sources from new upstream repo (bz1087590)

* Thu Aug 21 2014 Neil Horman <nhorman@redhat.com> - 5.1
- Update to rng tools version 5 (bz1087590)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 4-5
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 4-4
- Mass rebuild 2013-12-27

* Mon Nov 4 2013 Jay Fenlason <fenlason@redhat.com> 4-3.3
- Forward port the -ignorefail patch from RHEL-6
  Resolves: rhbz1020635

* Mon Sep 30 2013 Jay Fenlason <fenlason@redhat.com> - 4-3.1
- Do not override sbindir, because it breaks selinux labelling on rngd
  Resolves: rhbz1000308

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 25 2012 Jaromir Capik <jcapik@redhat.com> - 4-2
- Migration to new systemd macros

* Mon Aug 6 2012 Jeff Garzik <jgarzik@redhat.com> - 4-1
- Update to release version 4.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Jiri Popelka <jpopelka@redhat.com> - 3-4
- 2 patches from RHEL-6
- systemd service
- man page fixes
- modernize spec file

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul  3 2010 Jeff Garzik <jgarzik@redhat.com> - 3-2
- comply with renaming guidelines, by Providing rng-utils = 1:2.0-4.2

* Sat Jul  3 2010 Jeff Garzik <jgarzik@redhat.com> - 3-1
- Update to release version 3.

* Fri Mar 26 2010 Jeff Garzik <jgarzik@redhat.com> - 2-3
- more minor updates for package review

* Thu Mar 25 2010 Jeff Garzik <jgarzik@redhat.com> - 2-2
- several minor updates for package review

* Wed Mar 24 2010 Jeff Garzik <jgarzik@redhat.com> - 2-1
- initial revision (as rng-tools)

