%define _localstatedir  %{_var}

Summary:        Network transaction audit tool
Name:           argus
Version:        3.0.6
Release:        %mkrel 1
Epoch:          0
License:        GPL
Group:          System/Servers
URL:            http://qosient.com/argus/
Source0:        http://qosient.com/argus/dev/argus-%{version}.tar.gz
Source1:        http://qosient.com/argus/dev/argus-%{version}.tar.gz.asc
Source2:        http://qosient.com/argus/dev/argus-%{version}.tar.gz.md5
Source3:        argus.init
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	ncurses-devel
BuildRequires:	pcap-devel
BuildRequires:	libsasl-devel
BuildRequires:	libwrap-devel
BuildRequires:	zlib-devel

%description
Argus (Audit Record Generation and Utilization System) is an IP network
transaction audit tool. The data generated by argus can be used for a
wide range of tasks such as network operations, security and performance
management.

%prep

%setup -q -n argus-%{version}

%build
export CPPFLAGS="-I%{_includedir}/sasl"

%configure2_5x \
    --with-sasl

%make

%install

%makeinstall_std

%{__mkdir_p} %{buildroot}%{_bindir}
%{__cp} -a bin/argusbug %{buildroot}%{_bindir}/argusbug

%{__mkdir_p} %{buildroot}%{_localstatedir}/lib/%{name}/archive

%{__mkdir_p} %{buildroot}%{_sysconfdir}
%{__cp} -a support/Config/argus.conf %{buildroot}%{_sysconfdir}/argus.conf

%{__perl} -pi -e 's|/var/log/argus|%{_localstatedir}/lib/%{name}|;' \
              -e 's|^#ARGUS_BIND_IP|ARGUS_BIND_IP|;' \
              -e 's|^#ARGUS_ACCESS_PORT|ARGUS_ACCESS_PORT|;' \
  %{buildroot}%{_sysconfdir}/argus.conf

%{__mkdir_p} %{buildroot}%{_initrddir}
%{__cp} -a %{SOURCE3} %{buildroot}%{_initrddir}/%{name}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files
%defattr(0644,root,root,0755)
%doc COPYING CREDITS INSTALL README VERSION doc support
%attr(0755,root,root) %{_bindir}/*
%attr(0755,root,root) %{_sbindir}/argus
%{_mandir}/man5/argus.conf.5*
%{_mandir}/man8/argus.8*
%dir %{_localstatedir}/lib/%{name}
%dir %{_localstatedir}/lib/%{name}/archive
%attr(0755,root,root) %{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/argus.conf
