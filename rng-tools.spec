
%global _sbindir /sbin

Summary:	Random number generator related utilities
Name:		rng-tools
Version:	5
Release:	1%{?dist}
Group:		System Environment/Base
License:	GPLv2+
URL:		http://sourceforge.net/projects/gkernel/
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Source0:	http://downloads.sourceforge.net/gkernel/rng-tools-%{version}.tar.gz
Source1:	rngd.init
Source2:	rngd.sysconfig

Requires:	chkconfig initscripts
BuildRequires:	automake autoconf groff gettext
Obsoletes:	rng-utils <= 1:2.0-4.1

%description
Hardware random number generation tools.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}/%{_initrddir}
install -m 755 %{SOURCE1} %{buildroot}/%{_initrddir}/rngd
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 640 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/rngd

%clean
rm -rf %{buildroot}

%post
/sbin/chkconfig --add rngd

%preun
if [ $1 -eq "0" ]; then
   /sbin/service rngd stop > /dev/null 2>&1
   /sbin/chkconfig --del rngd
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/sysconfig/rngd
%attr(0755,root,root) %{_initrddir}/rngd
%{_bindir}/rngtest
%{_sbindir}/rngd
%{_mandir}/man1/rngtest.1.*
%{_mandir}/man8/rngd.8.*

%changelog
* Thu Mar 12 2015 Neil Horman <nhorman@redhat.com> - 5.1
- Update to the latest upstream

* Fri Dec  2 2011 Jeff Garzik <jgarzik@redhat.com> - 2-13
- Resolves: bz#751374
- Add post/preun calls to chkconfig, during rpm install/removal
- Remove unused rotate, resume steps from init script

* Thu Nov 17 2011 Jeff Garzik <jgarzik@redhat.com> - 2-12
- Update RPM package changelog.

* Thu Nov 17 2011 Jeff Garzik <jgarzik@redhat.com> - 2-11
- Resolves: bz#751374
  add sysconfig and init scripts

* Thu Nov 3 2011 Don Zickus <dzickus@redhat.com> - 2-10
- Resolves: bz#749629
  add ignorefail option to manpage

* Tue Oct 25 2011 Jay Fenlason <fenlason@redhat.com> - 2-9
- Add patch from James M. Leddy <james.leddy@redhat.com> to add
  an option to ignore FIPS failures.
  Resolves: bz#733452

* Mon Aug 23 2010 Jeff Garzik <jgarzik@redhat.com> - 2-8
- Resolves: bz#624530
- Fix loop on bad RNG

* Fri May 28 2010 David Howells <dhowells@rehdat.com> - 2-7
- Resolves: bz#597221
- Fix some compiler warnings thus dealing with the SEGV
- Make do_loop() correctly interpret the result of iter->xread()

* Fri Mar 26 2010 Jeff Garzik <jgarzik@redhat.com> - 2-6
- Resolves: bz#576678
- increase version number of rng-utils that we obsolete
- use global rather than define, for sbindir (Fedora pkg review)
- improve BuildRoot (Fedora pkg review)

* Thu Mar 25 2010 Jeff Garzik <jgarzik@redhat.com> - 2-5
- Fix specfile error preventing TPM patch from being applied
- Resolves: bz#530012

* Thu Mar 25 2010 Jeff Garzik <jgarzik@redhat.com> - 2-4
- Add TPM patch from Dell
- Resolves: bz#530012

* Thu Mar 25 2010 Jeff Garzik <jgarzik@redhat.com> - 2-3
- Related: bz#576678
- bump release number due to tag confusion w/ devel branch

* Thu Mar 25 2010 Jeff Garzik <jgarzik@redhat.com> - 2-2
- Related: bz#576678
- several minor updates from Fedora package review

* Wed Mar 24 2010 Jeff Garzik <jgarzik@redhat.com> - 2-1
- initial revision (as rng-tools)

