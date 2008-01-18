# $Id$
# Authority: dag

%define logmsg logger -t %{name}/rpm

%define real_name davfs2

Summary: FUSE-Filesystem to access WebDAV servers
Name: fuse-davfs2
Version: 1.2.2
Release: 2
License: GPL
Group: System Environment/Kernel
URL: http://dav.sourceforge.net/

Source: http://dl.sf.net/dav/davfs2-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: fuse-devel >= 2.2, neon-devel
Requires: fuse >= 2.2

Obsoletes: davfs2 <= %{name}-%{version}
Provides: davfs2 = %{name}-%{version}

%description
davfs2 is a FUSE file system driver that allows you to mount a WebDAV server
as a local file system, like a disk drive. This way applications can access
resources on a Web server without knowing anything about HTTP or WebDAV.

davfs2 runs as a daemon in userspace. It uses the kernel file system coda or
fuse. Most propably your Linux kernel includes at least one of this file
systems. To connect to the WebDAV server it makes use of the neon library.
Neon supports TLS/SSL (using OpenSSL or GnuTLS) and access via proxy server.

%prep
%setup -n %{real_name}-%{version}

%build
%configure --disable-static
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"
%find_lang %{real_name}

%{__install} -Dp -m0770 %{buildroot}%{_localstatedir}/cache/davfs2/
%{__mv} -vf %{buildroot}%{_sbindir}/mount.davfs %{buildroot}/sbin/mount.davfs
%{__mv} -vf %{buildroot}%{_sbindir}/umount.davfs %{buildroot}/sbin/umount.davfs

### Clean up buildroot
%{__rm} -rf %{buildroot}%{_docdir}

%pre
if ! /usr/bin/getent passwd davfs2 &>/dev/null; then
    %{_sbindir}/useradd -r -d %{_localstatedir}/cache/davfs2 -s %{_sbindir}/nologin -c "davfs2" davfs2 || \
        %logmsg "Unexpected error adding user \"davfs2\". Aborting installation."
fi

if ! /usr/bin/getent group davfs2 &>/dev/null; then
    %{_sbindir}/groupadd -r davfs2 &>/dev/null || \
        %logmsg "Unexpected error adding group \"davfs2\". Aborting installation."
fi

%clean
%{__rm} -rf %{buildroot}

%files -f %{real_name}.lang
%defattr(-, root, root, 0755)
%doc AUTHORS BUGS COPYING FAQ INSTALL NEWS README* THANKS TODO etc/davfs2.conf etc/secrets
%doc %{_mandir}/man5/davfs2.conf.5*
%doc %{_mandir}/man8/mount.davfs.8*
%doc %{_mandir}/man8/umount.davfs.8*
%doc %{_mandir}/*/man5/davfs2.conf.5*
%doc %{_mandir}/*/man8/mount.davfs.8*
%doc %{_mandir}/*/man8/umount.davfs.8*
%config(noreplace) %{_sysconfdir}/davfs2/davfs2.conf
%config %{_sysconfdir}/davfs2/secrets
%config %{_sysconfdir}/davfs2/certs/
/sbin/mount.davfs
/sbin/umount.davfs
%{_datadir}/davfs2/

%defattr(-, davfs2, davfs2, 0770)
%dir %{_localstatedir}/cache/davfs2/

%changelog
* Fri Jan 18 2008 Ralph Angenendt <ra@br-online.de> - 1.2.2-2
- Updated to release 1.2.2.

* Sat Nov 10 2007 Dag Wieers <dag@wieers.com> - 1.2.2-1
- Updated to release 1.2.2.

* Sat May 12 2007 Dag Wieers <dag@wieers.com> - 1.2.1-1
- Initial package. (using DAR)
