Name:           intel-dlstreamer
Version:        2025.2.0
Release:        1%{?dist}
Summary:        Deep Learning Streamer with bundled dependencies

License:        Proprietary
Source0:        %{name}-%{version}.tar.gz
Source1:        opencv-4.10.0.tar.gz
Source2:        paho.mqtt.c-1.3.4.tar.gz
Source3:        openvino_toolkit_ubuntu24_2025.2.0.19140.c01cd93e24d_x86_64.tgz
Source4:        gstreamer-1.26.1.tar.gz
Source5:        ffmpeg-6.1.1.tar.gz
URL:            https://github.com/open-edge-platform/edge-ai-libraries/tree/release-1.2.0/libraries/dl-streamer
Packager:       DL Streamer Team <dlstreamer@intel.com>
ExclusiveArch:  x86_64
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
AutoReqProv:    no
%define debug_package %{nil}
%define __os_install_post %{nil}

BuildRequires:  cmake ninja-build gcc gcc-c++ make git python3 python3-pip yasm nasm meson pkgconfig openssl-devel patchelf
Requires: glib2-devel
Requires: libjpeg-turbo
Requires: libdrm
Requires: wayland-devel
Requires: libX11
Requires: libpng
Requires: libva
Requires: libcurl
Requires: libde265
Requires: libXext
Requires: mesa-libGL
Requires: mesa-libGLU
Requires: libgudev
Requires: paho-c
Requires: python3
Requires: python3-pip
Requires: python3-gobject
Requires: cairo
Requires: cairo-gobject
Requires: gobject-introspection
Requires: libvpx
Requires: opus
Requires: libsrtp
Requires: libXv
Requires: libva-utils
Requires: libogg
Requires: libusb1
Requires: x265-libs
Requires: x264-libs
Requires: openexr
Requires: tbb
Requires: intel-media-driver
Requires: openvino-2025.2.0

%description
This package contains Intel DL Streamer and all required dependencies built from source.

%prep
%setup -q -n %{name}-%{version}
%setup -D -T -a 1
%setup -D -T -a 2
%setup -D -T -a 3
%setup -D -T -a 4
%setup -D -T -a 5

%build
# Set up build environment
export DESTDIR=%{buildroot}
export PREFIX=/opt/intel/dlstreamer
mkdir -p %{buildroot}$PREFIX

# 1. Build paho-mqtt-c
pushd paho.mqtt.c-1.3.4
make PREFIX=$PREFIX
make install PREFIX=$PREFIX DESTDIR=%{buildroot}
popd

# 2. Build OpenCV
pushd opencv-4.10.0
mkdir build
cd build/
cmake -DCMAKE_INSTALL_PREFIX=$PREFIX/opencv \
      -DCMAKE_BUILD_TYPE=Release \
      -DBUILD_TESTS=OFF \
      -DBUILD_PERF_TESTS=OFF \
      -DBUILD_EXAMPLES=OFF \
      -DBUILD_opencv_apps=OFF \
      -GNinja ..
ninja -j "$(nproc)"
DESTDIR=%{buildroot} ninja install
popd

# 3. Build FFmpeg
pushd ffmpeg-6.1.1
./configure --prefix=$PREFIX/ffmpeg \
            --enable-pic \
            --enable-shared \
            --enable-static \
            --enable-avfilter \
            --enable-vaapi \
            --extra-cflags="-I$PREFIX/include" \
            --extra-ldflags="-L$PREFIX/lib" \
            --extra-libs=-lpthread \
            --extra-libs=-lm
make -j "$(nproc)"
make install DESTDIR=%{buildroot}
popd

# 4. Build GStreamer 
pushd gstreamer-1.26.1
export PKG_CONFIG_PATH=$PREFIX/lib/pkgconfig:$PKG_CONFIG_PATH
meson setup -Dexamples=disabled \
            -Dtests=disabled \
            -Dvaapi=enabled \
            -Dgst-examples=disabled \
            --buildtype=release \
            --prefix=$PREFIX/gstreamer \
            --libdir=lib \
            --libexecdir=bin \
            build/
ninja -C build
DESTDIR=%{buildroot} meson install -C build/
popd

# 5. Build DL Streamer with locally built dependencies
pushd %{name}-%{version}
mkdir build
cd build
export PKG_CONFIG_PATH="$PREFIX/gstreamer/lib/pkgconfig:${PKG_CONFIG_PATH}"
# Note: OpenVINO setup would need to be handled differently in a proper RPM build
cmake -DCMAKE_INSTALL_PREFIX=$PREFIX \
      -DENABLE_PAHO_INSTALLATION=ON \
      -DENABLE_RDKAFKA_INSTALLATION=ON \
      -DENABLE_VAAPI=ON \
      -DENABLE_SAMPLES=ON ..
make -j "$(nproc)"
make install DESTDIR=%{buildroot}
popd


%install
# Build root is already populated by DESTDIR installs in %build section
# Just need to remove RPATH for all binaries/libs
find %{buildroot} -type f \( -name "*.so*" -o -perm -111 \) | while read -r file; do
    if patchelf --print-rpath "$file" &>/dev/null; then
        rpath=$(patchelf --print-rpath "$file")
        if [ -n "$rpath" ]; then
            echo "Removing RPATH from $file"
            patchelf --remove-rpath "$file"
        fi
    fi
done

%clean
rm -rf %{buildroot}

%check
# Optional: Add test commands here

%files
%defattr(-,root,root,-)
%license LICENSE
/opt/intel/dlstreamer/


%changelog
* Wed Aug 06 2025 DL Streamer Team <dlstreamer@intel.com> - 2025.2.0-1
- Initial release.