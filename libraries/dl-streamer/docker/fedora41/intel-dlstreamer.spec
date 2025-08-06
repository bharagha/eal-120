Name:           intel-dlstreamer
Version:        2025.2.0
Release:        1%{?dist}
Summary:        Deep Learning Streamer with bundled dependencies

License:        Proprietary
Source0:        %{name}-%{version}.tar.gz
Source1:        https://github.com/opencv/opencv/archive/4.10.0.zip
Source2:        https://github.com/eclipse/paho.mqtt.c/archive/v1.3.4.tar.gz
Source3:        https://storage.openvinotoolkit.org/repositories/openvino/packages/2025.2/linux/openvino_toolkit_ubuntu24_2025.2.0.19140.c01cd93e24d_x86_64.tgz
Source4:        https://gitlab.freedesktop.org/gstreamer/gstreamer/-/archive/1.26.1/gstreamer-1.26.1.tar.gz
Source5:        https://ffmpeg.org/releases/ffmpeg-6.1.1.tar.gz
URL:            https://github.com/open-edge-platform/edge-ai-libraries/tree/release-1.2.0/libraries/dl-streamer
Packager:       DL Streamer Team <dlstreamer@intel.com>
ExclusiveArch:  x86_64
AutoReqProv:    no
%define debug_package %{nil}
%define __os_install_post %{nil}

BuildRequires:  cmake ninja-build gcc gcc-c++ make git python3 python3-pip yasm nasm meson pkgconfig openssl-devel
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
%setup -q
tar xzf %{SOURCE0}
unzip %{SOURCE1}
tar xzf %{SOURCE2}
tar xzf %{SOURCE3}
tar xzf %{SOURCE4}
tar xzf %{SOURCE5}

%build
# 1. Build paho-mqtt-c
pushd 1.3.4
make
sudo make install
popd

# 2. Build OpenCV
pushd 4.10.0
mkdir build
cd build/
cmake -DBUILD_TESTS=OFF -DBUILD_PERF_TESTS=OFF -DBUILD_EXAMPLES=OFF -DBUILD_opencv_apps=OFF -GNinja ..
ninja -j "$(nproc)"
sudo env PATH=~/python3venv/bin:$PATH ninja install 
popd

# 3. Build FFmpeg
pushd ffmpeg-6.1.1
./configure --enable-pic --enable-shared --enable-static --enable-avfilter --enable-vaapi \
 --extra-cflags="-I/include" --extra-ldflags="-L/lib" --extra-libs=-lpthread --extra-libs=-lm --bindir="/bin"
make -j "$(nproc)"
sudo make install
popd

# 4. Build GStreamer 
pushd gstreamer-1.26.1
export PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig/:/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH
sudo ldconfig
meson setup -Dexamples=disabled -Dtests=disabled -Dvaapi=enabled -Dgst-examples=disabled --buildtype=release --prefix=/opt/intel/dlstreamer/gstreamer --libdir=lib/ --libexecdir=bin/ build/
ninja -C build
sudo env PATH=~/python3venv/bin:$PATH meson install -C build/
popd

# 5. Build DL Streamer with locally built dependencies
pushd %{name}-%{version}
mkdir build
cd build
export PKG_CONFIG_PATH="/opt/intel/dlstreamer/gstreamer/lib/pkgconfig:${PKG_CONFIG_PATH}"
source /opt/intel/openvino_2025/setupvars.sh
cmake -DENABLE_PAHO_INSTALLATION=ON -DENABLE_RDKAFKA_INSTALLATION=ON -DENABLE_VAAPI=ON -DENABLE_SAMPLES=ON ..
make -j "$(nproc)"


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/opt
mkdir -p %{buildroot}/usr

cp -a opt/* %{buildroot}/opt/

# Remove RPATH for all binaries/libs
find %{buildroot} -type f \( -name "*.so*" -o -perm -111 \) | while read -r file; do
    if patchelf --print-rpath "$file" &>/dev/null; then
        rpath=$(patchelf --print-rpath "$file")
        if [ -n "$rpath" ]; then
            echo "Removing RPATH from $file"
            patchelf --remove-rpath "$file"
        fi
    fi
done

%check
# Optional: Add test commands here

%files
%license LICENSE
/opt/intel/dlstreamer/
/opt/opencv/
/opt/rdkafka/
/opt/ffmpeg/


%changelog
* Wed Aug 06 2025 DL Streamer Team <dlstreamer@intel.com> - 2025.2.0-1
- Initial release.