Name:           paho-mqtt-c
Version:        1.3.4
Release:        1%{?dist}
Summary:        Eclipse Paho MQTT C client library for Intel DL Streamer

License:        EPL-2.0 OR BSD-3-Clause
Source0:        paho.mqtt.c-%{version}.tar.gz
URL:            https://github.com/eclipse/paho.mqtt.c
Packager:       DL Streamer Team <dlstreamer@intel.com>
ExclusiveArch:  x86_64
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  cmake gcc gcc-c++ make
BuildRequires:  openssl-devel
BuildRequires:  doxygen

Requires:       openssl

%description
Eclipse Paho MQTT C client library configured for Intel DL Streamer.
Provides MQTT connectivity for edge AI applications.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       openssl-devel

%description devel
Development files and headers for Intel Paho MQTT C client.

%prep
%setup -q -n paho.mqtt.c-%{version}

%build
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/opt/intel/paho-mqtt-c \
      -DCMAKE_BUILD_TYPE=Release \
      ..
make -j "$(nproc)"

%install
rm -rf %{buildroot}
cd build
make install DESTDIR=%{buildroot}

# Create pkgconfig file
mkdir -p %{buildroot}/opt/intel/paho-mqtt-c/lib64/pkgconfig
cat > %{buildroot}/opt/intel/paho-mqtt-c/lib64/pkgconfig/paho-mqtt-c.pc << 'EOF'
prefix=/opt/intel/paho-mqtt-c
exec_prefix=${prefix}
libdir=${exec_prefix}/lib64
includedir=${prefix}/include

Name: paho-mqtt-c
Description: Eclipse Paho MQTT C Client Library
Version: %{version}
Libs: -L${libdir} -lpaho-mqtt3c -lpaho-mqtt3cs
Cflags: -I${includedir}
EOF

# Create system pkgconfig symlink
mkdir -p %{buildroot}/usr/lib64/pkgconfig
ln -sf /opt/intel/paho-mqtt-c/lib64/pkgconfig/paho-mqtt-c.pc \
       %{buildroot}/usr/lib64/pkgconfig/intel-paho-mqtt-c.pc

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
/opt/intel/paho-mqtt-c/lib64/*.so.*
/usr/lib64/pkgconfig/intel-paho-mqtt-c.pc

%files devel
%defattr(-,root,root,-)
/opt/intel/paho-mqtt-c/include/
/opt/intel/paho-mqtt-c/lib64/*.so
/opt/intel/paho-mqtt-c/lib64/*.a
/opt/intel/paho-mqtt-c/lib64/pkgconfig/

%changelog
* Thu Aug 07 2025 DL Streamer Team <dlstreamer@intel.com> - 1.3.4-1
- Initial Intel optimized Paho MQTT C build
