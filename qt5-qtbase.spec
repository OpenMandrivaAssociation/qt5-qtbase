# cb 05/01/2016
# because the docdir is under /usr/share/doc
# all files there get marked as doc so that when they are installed
# on abf using --excludedocs option they are missing, causing qt5-qtdoc to fail
# this makes sure the files dont get marked as docs
%define _no_default_doc_files 1

# If we ever switch back to ld.gold as default
# linker, we need to add -fuse-ld=bfd or -fuse-ld=lld
# on aarch64 as workaround for a weird signal/slot problem
# (slots defined as lambdas never called)
%global optflags %{optflags} -Ofast

#% define debug_package %{nil}
%define beta alpha
%define api 5
%define major 5

%define _qt_prefix %{_libdir}/qt%{api}
%define _qt_bindir %{_qt_prefix}/bin
%define _qt_docdir %{_docdir}/qt%{api}
%define _qt_libdir %{_libdir}
%define _qt_libexecdir %{_qt_prefix}/libexec
%define _qt_includedir %{_includedir}/qt5
%define _qt_plugindir %{_libdir}/qt%{api}/plugins
%define _qt_demodir %{_qt_prefix}/demos
%define _qt_exampledir %{_qt_prefix}/examples
%define _qt_importdir %{_qt_prefix}/imports
%define _qt_datadir %{_datadir}/qt%{api}
%define _qt_sysconfdir %{_sysconfdir}/qt%{api}
%define _qt_testsdir %{_qt_prefix}/tests
%define _qt_translationsdir %{_qt_datadir}/translations

# qt base components
%define qtbootstrapd %mklibname qt%{api}bootstrap -d
%define qtconcurrent %mklibname qt%{api}concurrent %{major}
%define qtconcurrentd %mklibname qt%{api}concurrent -d
%define qtcore %mklibname qt%{api}core %{major}
%define qtcored %mklibname qt%{api}core -d
%define qtdbus %mklibname qt%{api}dbus %{major}
%define qtdbusd %mklibname qt%{api}dbus -d
%define qteglfsdeviceintegration %mklibname qt%{api}eglfsdeviceintegration %{major}
%define qteglfsdeviceintegrationd %mklibname qt%{api}eglfsdeviceintegration -d
%define qtgui %mklibname qt%{api}gui %{major}
%define qtguid %mklibname qt%{api}gui -d
%define qtnetwork %mklibname qt%{api}network %{major}
%define qtnetworkd %mklibname qt%{api}network -d
%define qtopengl %mklibname qt%{api}opengl %{major}
%define qtopengld %mklibname qt%{api}opengl -d
%define qtprintsupport %mklibname qt%{api}printsupport %{major}
%define qtprintsupportd %mklibname qt%{api}printsupport -d
%define qtsql %mklibname qt%{api}sql %{major}
%define qtsqld %mklibname qt%{api}sql -d
%define qttest %mklibname qt%{api}test %{major}
%define qttestd %mklibname qt%{api}test -d
%define qtwidgets %mklibname qt%{api}widgets %{major}
%define qtwidgetsd %mklibname qt%{api}widgets -d
%define qtxcbqpa %mklibname qt%{api}xcbqpa %{major}
%define qtxcbqpad %mklibname qt%{api}xcbqpa -d
%define qtxml %mklibname qt%{api}xml %{major}
%define qtxmld %mklibname qt%{api}xml -d
# The following ones exist only as static libraries (probably no stable ABI yet)
%define qtaccessibilitysupportd %mklibname qt%{api}accessibilitysupport -d -s
%define qtedidsupportd %mklibname qt%{api}edidsupport -d -s
%define qtvulkansupportd %mklibname qt%{api}vulkansupport -d -s
%define qtdevicediscoverysupportd %mklibname qt%{api}devicediscoverysupport -d -s
%define qteglsupportd %mklibname qt%{api}eglsupport -d -s
%define qteventdispatchersupportd %mklibname qt%{api}eventdispatchersupport -d -s
%define qtfbsupportd %mklibname qt%{api}fbsupport -d -s
%define qtfontdatabasesupportd %mklibname qt%{api}fontdatabasesupport -d -s
%define qtglxsupportd %mklibname qt%{api}glxsupport -d -s
%define qtinputsupportd %mklibname qt%{api}inputsupport -d -s
%define qtlinuxaccessibilitysupportd %mklibname qt%{api}linuxaccessibilitysupport -d -s
%define qtplatformcompositorsupportd %mklibname qt%{api}platformcompositorsupport -d -s
%define qtservicesupportd %mklibname qt%{api}servicesupport -d -s
%define qtthemesupportd %mklibname qt%{api}themesupport -d -s
# Removed in 5.8, but we still need the names so we can obsolete it
%define qtegldeviceintegration %mklibname qt%{api}egldeviceintegration %{major}
%define qtegldeviceintegrationd %mklibname qt%{api}egldeviceintegration -d

%bcond_without bootstrap

%bcond_with directfb
# Docs require qdoc5 and qt5-tools to build
%if %{with bootstrap}
# Requires qdoc5 and qt5-tools to build
%bcond_with docs
%else
# Requires qdoc5 and qt5-tools to build
%bcond_without docs
%endif
%bcond_without gtk

%bcond_without clang
%bcond_without mysql

%define qtmajor %(echo %{version} |cut -d. -f1)
%define qtminor %(echo %{version} |cut -d. -f2)
%define qtsubminor %(echo %{version} |cut -d. -f3)
%define qtversion %{qtmajor}.%{qtminor}.%{qtsubminor}

Summary:	Version 5 of the Qt toolkit
Name:		qt5-qtbase
Version:	5.15.0
%if "%{beta}" != ""
Release:	0.%{beta}.1
%define qttarballdir qtbase-everywhere-src-%{version}-%{beta}
Source0:	http://download.qt.io/development_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}-%{beta}/submodules/%{qttarballdir}.tar.xz
%else
Release:	1
%define qttarballdir qtbase-everywhere-src-%{version}
Source0:	http://download.qt.io/official_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}/submodules/%{qttarballdir}.tar.xz
%endif
License:	LGPLv3+
Group:		Development/KDE and Qt
Url:		http://www.qt.io
Source1:	qt5.macros
# (tpg) Use software rendering in case when OpenGL supported by graphics card is older than 2.
# needs xinitrc
Source2:	10-qt5-check-opengl.xsetup
Source3:	qtlogging.ini
Source100:	%{name}.rpmlintrc
Patch0:		qtbase-everywhere-src-5.3.2-QTBUG-35459.patch
# FIXME check if this has been fixed in 5.6.0 or if the patch needs to
# be updated
#Patch1:		0001-Fix-to-make-QtWayland-compositor-work-with-the-iMX6-.patch
# Fix XDG_RUNTIME_DIR for setuid applications
# https://issues.openmandriva.org/show_bug.cgi?id=1641
Patch2:		qt-5.7.0-setuid-XDG_RUNTIME_DIR.patch
# https://codereview.qt-project.org/#/c/151459/
Patch3:		qt-5.5.1-barf-on-clang-PIE.patch
Patch4:		qt-5.8.0-no-isystem-usr-include.patch
Patch5:		qtbase-5.14.1-clang10.patch

### Fedora patches
Patch102:	qtbase-everywhere-src-5.6.0-moc_WORDSIZE.patch
### END OF FEDORA PATCHES

# FIXME this is broken -- but currently required because QtGui
# and friends prefer linking to system QtCore over linking to the
# just built QtCore. This should be fixed properly in the Makefiles.
BuildConflicts:	%{mklibname -d qt5core} < %{version}

BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	cmake(double-conversion)
# PCRE 2.x
BuildRequires:	pkgconfig(libpcre2-16)
# Build scripts
BuildRequires:	python >= 3.0
BuildRequires:	python2
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(libsctp)
# CUPS
BuildRequires:	cups-devel
# OpenGL
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(glesv2)
BuildRequires:	pkgconfig(gbm)
BuildRequires:	pkgconfig(libdrm)
# OpenVG
BuildRequires:	openvg-devel
# Vulkan
BuildRequires:	vulkan-devel
# Event loop
BuildRequires:	pkgconfig(glib-2.0)
%if %{with gtk}
# GTK theme
BuildRequires:	pkgconfig(gtk+-2.0)
%endif
# ICU
BuildRequires:	pkgconfig(icu-uc) >= 60.1
# Multimedia
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(xorg-evdev)
# For XCB platform plugin:
BuildRequires:	pkgconfig(xcb) >= 1.5
BuildRequires:	pkgconfig(xcb-icccm)
BuildRequires:	pkgconfig(xcb-image)
BuildRequires:	pkgconfig(xcb-renderutil)
BuildRequires:	pkgconfig(xcb-keysyms)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(xcb-render)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xcb-xinerama)
BuildRequires:	pkgconfig(xcb-shape)
BuildRequires:	pkgconfig(xv)
BuildRequires:	pkgconfig(xcb-xv)
BuildRequires:	pkgconfig(inputproto)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xcb-xfixes)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xcb-randr)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(xkbcomp)
BuildRequires:	pkgconfig(xkbfile)
BuildRequires:	pkgconfig(xkbcommon) >= 0.4.1
BuildRequires:	pkgconfig(xkbcommon-x11) >= 0.4.1
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(mtdev)
BuildRequires:	pkgconfig(harfbuzz)
# For proper font access
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
%if %{with directfb}
# DirectFB platform plugin:
BuildRequires:	pkgconfig(directfb)
%endif
# Accessibility
BuildRequires:	pkgconfig(atspi-2)
# Assorted...
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(libpci)
BuildRequires:	pkgconfig(libcap)
BuildRequires:	pkgconfig(libinput)
BuildRequires:	pkgconfig(libcrypto)
BuildRequires:	pkgconfig(libssl)
BuildRequires:	flex bison gperf
# Used for CPU feature detection in configure step
BuildRequires:	gdb
%if %{with docs}
BuildRequires:	qdoc5
BuildRequires:	qt5-qttools
BuildRequires:	qt5-assistant
# Platform plugin required for qhelpgenerator startup
BuildRequires:	%{qtgui}-minimal
%endif
# For the Provides: generator
BuildRequires:	cmake >= 3.11.0-1

%description
Version 5 of the Qt toolkit.

#----------------------------------------------------------------------------
# qt base components
#----------------------------------------------------------------------------

%package -n %{qtbootstrapd}
Summary:	Development files for version 5 if the QtBootstrap library
Group:		Development/KDE and Qt

%description -n %{qtbootstrapd}
Development files for version 5 if the QtBootstrap library.

%files -n %{qtbootstrapd}
%{_qt_libdir}/libQt%{api}Bootstrap.a
%{_qt_libdir}/libQt%{api}Bootstrap.prl
%{_libdir}/cmake/Qt%{api}Bootstrap

#----------------------------------------------------------------------------

%package -n %{qtconcurrent}
Summary:	Qt threading library
Group:		System/Libraries

%description -n %{qtconcurrent}
Qt threading library.

%files -n %{qtconcurrent}
%{_qt_libdir}/libQt%{api}Concurrent.so.%{major}*
%if "%{_qt_libdir}" != "%{_libdir}"
%{_libdir}/libQt%{api}Concurrent.so.%{major}*
%endif

#----------------------------------------------------------------------------

%package -n %{qtconcurrentd}
Summary:	Development files for version 5 of the QtConcurrent library
Group:		Development/KDE and Qt
Requires:	%{qtconcurrent} = %{EVRD}
# Was introduced by mistake
Obsoletes:	%{_lib}qt5concurrent5-devel < %{EVRD}

%description -n %{qtconcurrentd}
Development files for version 5 of the QtConcurrent library.

%files -n %{qtconcurrentd}
%{_qt_includedir}/QtConcurrent
%{_qt_libdir}/libQt%{api}Concurrent.so
%{_qt_libdir}/libQt%{api}Concurrent.prl
%{_qt_libdir}/cmake/Qt%{api}Concurrent
%{_qt_libdir}/pkgconfig/Qt%{api}Concurrent.pc
%if "%{_qt_libdir}" != "%{_libdir}"
%{_libdir}/pkgconfig/Qt%{api}Concurrent.pc
%endif

#----------------------------------------------------------------------------

%package -n %{qtcore}
Summary:	Qt Core library
Group:		System/Libraries
Suggests:	%{name}-qtcore-i18n = %{EVRD}
Suggests:	qt5-qtchooser = %{EVRD}
Obsoletes:	%{_lib}qt5v85 < 5.1.0-8
Obsoletes:	%{_lib}qt5v8_5 < 5.2.0

%description -n %{qtcore}
Qt Core library.

%files -n %{qtcore}
%{_qt_libdir}/libQt%{api}Core.so.%{major}*
%if "%{_qt_libdir}" != "%{_libdir}"
%{_libdir}/libQt%{api}Core.so.%{major}*
%endif
%dir %{_qt_plugindir}
%{_libdir}/metatypes/qt5core_metatypes.json

#----------------------------------------------------------------------------
%package -n qt5-qtchooser
Summary:	qtchooser integration for Qt 5.x
Group:		System/Libraries

%description -n qt5-qtchooser
qtchooser integration for Qt 5.x

%files -n qt5-qtchooser
%{_sysconfdir}/xdg/qtchooser/*.conf

#----------------------------------------------------------------------------

%package -n %{qtcored}
Summary:	Development files for version 5 of the QtCore library
Group:		Development/KDE and Qt
Requires:	%{qtcore} = %{EVRD}
Obsoletes:	%{_lib}qt5v8-devel < 5.2.0

%description -n %{qtcored}
Development files for version 5 of the QtCore library.

%files -n %{qtcored}
%dir %{_qt_docdir}
%{_qt_docdir}/global
%{_bindir}/moc-qt%{api}
%{_qt_bindir}/moc
%{_bindir}/moc
%{_qt_bindir}/syncqt*
%{_bindir}/rcc-qt%{api}
%{_qt_bindir}/rcc
%{_bindir}/rcc
%{_qt_bindir}/tracegen
%{_bindir}/tracegen
%{_bindir}/tracegen-qt5
%{_qt_includedir}/QtCore
%{_qt_libdir}/libQt%{api}Core.so
%{_qt_libdir}/libQt%{api}Core.prl
%{_qt_libdir}/cmake/Qt%{api}Core
%{_qt_libdir}/cmake/Qt%{api}/Qt%{api}Config.cmake
%{_qt_libdir}/cmake/Qt%{api}/Qt%{api}ConfigVersion.cmake
%{_qt_libdir}/cmake/Qt%{api}/Qt%{api}ModuleLocation.cmake
%{_qt_libdir}/pkgconfig/Qt%{api}Core.pc
%if "%{_qt_libdir}" != "%{_libdir}"
%{_libdir}/pkgconfig/Qt%{api}Core.pc
%endif
%dir %{_qt_libdir}/cmake
%dir %{_qt_libdir}/cmake/Qt%{api}
%dir %{_qt_libdir}/pkgconfig

#----------------------------------------------------------------------------
%package -n %{qtdbus}
Summary:	Qt DBus connector library
Group:		System/Libraries

%description -n %{qtdbus}
Qt DBus connector library.

%files -n %{qtdbus}
%{_qt_libdir}/libQt%{api}DBus.so.%{major}*
%if "%{_qt_libdir}" != "%{_libdir}"
%{_libdir}/libQt%{api}DBus.so.%{major}*
%endif

#----------------------------------------------------------------------------

%package -n %{qtdbusd}
Summary:	Development files for version 5 of the QtDBus library
Group:		Development/KDE and Qt
Requires:	%{qtdbus} = %{EVRD}

%description -n %{qtdbusd}
Development files for version 5 of the QtDBus library.

%files -n %{qtdbusd}
%{_qt_bindir}/qdbuscpp2xml
%{_bindir}/qdbuscpp2xml
%{_bindir}/qdbuscpp2xml-qt%{api}
%{_qt_bindir}/qdbusxml2cpp
%{_bindir}/qdbusxml2cpp
%{_bindir}/qdbusxml2cpp-qt%{api}
%{_qt_includedir}/QtDBus
%{_qt_libdir}/libQt%{api}DBus.so
%{_qt_libdir}/libQt%{api}DBus.prl
%{_qt_libdir}/cmake/Qt%{api}DBus
%{_qt_libdir}/pkgconfig/Qt%{api}DBus.pc
%if "%{_qt_libdir}" != "%{_libdir}"
%{_libdir}/pkgconfig/Qt%{api}DBus.pc
%endif

#----------------------------------------------------------------------------
%package -n %{qteglfsdeviceintegration}
Summary:	Qt EGL Device integration library
Group:		System/Libraries
%rename %{qtegldeviceintegration}

%description -n %{qteglfsdeviceintegration}
Qt EGL Device integration library

%files -n %{qteglfsdeviceintegration}
%{_qt_libdir}/libQt%{api}EglFSDeviceIntegration.so.%{major}*
%if "%{_qt_libdir}" != "%{_libdir}"
%{_libdir}/libQt%{api}EglFSDeviceIntegration.so.%{major}*
%endif
%{_qt_plugindir}/egldeviceintegrations

#----------------------------------------------------------------------------

%package -n %{qteglfsdeviceintegrationd}
Summary:	Development files for version 5 of the QtEGLDeviceIntegration library
Group:		Development/KDE and Qt
Requires:	%{qteglfsdeviceintegration} = %{EVRD}
%rename %{qtegldeviceintegrationd}

%description -n %{qteglfsdeviceintegrationd}
Development files for version 5 of the QtEGLDeviceIntegration library.

%files -n %{qteglfsdeviceintegrationd}
%{_qt_libdir}/libQt%{api}EglFSDeviceIntegration.so
%{_qt_libdir}/libQt%{api}EglFSDeviceIntegration.prl
%{_qt_includedir}/QtEglFSDeviceIntegration
%{_libdir}/cmake/Qt%{api}EglFSDeviceIntegration

#----------------------------------------------------------------------------

%package -n %{qtgui}
Summary:	Qt GUI library
Group:		System/Libraries
Suggests:	qt5-style-plugins
Requires:	%{_lib}qt5-output-driver = %{EVRD}
Suggests:	%{_lib}qt5-output-driver-default = %{EVRD}

%description -n %{qtgui}
Qt GUI library.

%files -n %{qtgui}
%{_qt_libdir}/libQt%{api}Gui.so.%{major}*
%if "%{_qt_libdir}" != "%{_libdir}"
%{_libdir}/libQt%{api}Gui.so.%{major}*
%endif
%{_qt_plugindir}/imageformats
%dir %{_qt_plugindir}/platforminputcontexts
%dir %{_qt_plugindir}/platforms
%if %{with gtk}
%dir %{_qt_plugindir}/platformthemes
%endif
%{_qt_plugindir}/generic
%{_qt_plugindir}/printsupport
%{_qt_datadir}/qtlogging.ini
%{_libdir}/metatypes/qt5gui_metatypes.json

#----------------------------------------------------------------------------

%package -n %{qtguid}
Summary:	Development files for version 5 of the QtGui library
Group:		Development/KDE and Qt
Requires:	%{qtgui} = %{EVRD}
Requires:	%{qtxcbqpa} = %{EVRD}
# We need all the Platform plugins because the plugin related cmake files in
# %{_qt_libdir}/cmake/Qt%{api}Gui cause fatal errors if the plugins aren't
# installed.
%if %{with directfb}
Requires:	%{qtgui}-directfb = %{EVRD}
%endif
%ifos linux
Requires:	%{qtgui}-linuxfb = %{EVRD}
%endif
Requires:	%{qtgui}-minimal = %{EVRD}
Requires:	%{qtgui}-offscreen = %{EVRD}
Requires:	%{qtgui}-x11 = %{EVRD}
Requires:	%{qtgui}-eglfs = %{EVRD}
Requires:	%{qtgui}-minimalegl = %{EVRD}
Requires:	%{qtgui}-vnc = %{EVRD}
Obsoletes:	%{qtgui}-kms < %{EVRD}
# *-platformtheme-* requirements are because of Qt5GuiConfig.cmake
# referencing the files, requiring it to exist.
%if %{with gtk}
Requires:	%{name}-platformtheme-gtk3 = %{EVRD}
%endif
Requires:	qt5-platformtheme-xdgdesktopportal
Requires:	pkgconfig(gl)
Requires:	pkgconfig(egl)
Requires:	pkgconfig(glesv2)
Requires:	vulkan-devel

%description -n %{qtguid}
Development files for version 5 of the QtGui library.

%files -n %{qtguid}
%{_qt_bindir}/uic
%{_bindir}/uic
%{_bindir}/uic-qt%{api}
%{_qt_includedir}/QtGui
%{_qt_includedir}/QtPlatformHeaders
%{_qt_libdir}/libQt%{api}Gui.so
%{_qt_libdir}/libQt%{api}Gui.prl
%dir %{_qt_libdir}/cmake/Qt%{api}Gui
%{_qt_libdir}/cmake/Qt%{api}Gui/Qt5GuiConfig.cmake
%{_qt_libdir}/cmake/Qt%{api}Gui/Qt5GuiConfigExtras.cmake
%{_qt_libdir}/cmake/Qt%{api}Gui/Qt5GuiConfigVersion.cmake
%{_qt_libdir}/cmake/Qt%{api}Gui/Qt5Gui_QEvdev*.cmake
%{_qt_libdir}/cmake/Qt%{api}Gui/Qt5Gui_QGifPlugin.cmake
%{_qt_libdir}/cmake/Qt%{api}Gui/Qt5Gui_QICOPlugin.cmake
%{_qt_libdir}/cmake/Qt%{api}Gui/Qt5Gui_QJpegPlugin.cmake
%{_qt_libdir}/cmake/Qt%{api}Gui/Qt5Gui_QLibInputPlugin.cmake
%{_qt_libdir}/cmake/Qt%{api}Gui/Qt5Gui_QGifPlugin.cmake
%{_qt_libdir}/cmake/Qt%{api}Gui/Qt5Gui_QTuioTouchPlugin.cmake
%{_qt_libdir}/pkgconfig/Qt%{api}Gui.pc
%if "%{_qt_libdir}" != "%{_libdir}"
%{_libdir}/pkgconfig/Qt%{api}Gui.pc
%endif

#----------------------------------------------------------------------------
%if %{with directfb}
%package -n %{qtgui}-directfb
Summary:	DirectFB output driver for QtGui v5
Group:		System/Libraries
Requires:	%{qtgui} = %{EVRD}
Provides:	%{_lib}qt5-output-driver = %{EVRD}

%description -n %{qtgui}-directfb
DirectFB output driver for QtGui v5.

%files -n %{qtgui}-directfb
%{_qt_plugindir}/platforms/libqdirectfb.so
%endif

#----------------------------------------------------------------------------

%package -n %{qtgui}-linuxfb
Summary:	Linux Framebuffer output driver for QtGui v5
Group:		System/Libraries
Requires:	%{qtgui} = %{EVRD}
Provides:	%{_lib}qt5-output-driver = %{EVRD}

%description -n %{qtgui}-linuxfb
Linux Framebuffer output driver for QtGui v5.

%files -n %{qtgui}-linuxfb
%{_qt_plugindir}/platforms/libqlinuxfb.so
# FIXME need to determine why those aren't built all the time. We're probably
# missing a BuildRequires: somewhere.
%optional %{_qt_libdir}/fonts

#----------------------------------------------------------------------------

%package -n %{qtgui}-minimal
Summary:	Minimal (Framebuffer based) output driver for QtGui v5
Group:		System/Libraries
Requires:	%{qtgui} = %{EVRD}
Provides:	%{_lib}qt5-output-driver = %{EVRD}

%description -n %{qtgui}-minimal
Minimal (Framebuffer based) output driver for QtGui v5.

%files -n %{qtgui}-minimal
%{_qt_plugindir}/platforms/libqminimal.so

%package -n %{qtgui}-minimal-devel
Summary:	Development files for the Minimal (FB) output driver for QtGui v5
Group:		Development/KDE and Qt
Requires:	%{qtgui}-minimal = %{EVRD}

%description -n %{qtgui}-minimal-devel
Development files for the Minimal (FB) output driver for QtGui v5

%files -n %{qtgui}-minimal-devel
%{_libdir}/cmake/Qt%{api}Gui/Qt%{api}Gui_QMinimal*.cmake

#----------------------------------------------------------------------------

%package -n %{qtgui}-offscreen
Summary:	Offscreen output driver for QtGui v5
Group:		System/Libraries
Requires:	%{qtgui} = %{EVRD}
Provides:	%{_lib}qt5-output-driver = %{EVRD}

%description -n %{qtgui}-offscreen
Offscreen output driver for QtGui v5.

%files -n %{qtgui}-offscreen
%{_qt_plugindir}/platforms/libqoffscreen.so

%package -n %{qtgui}-offscreen-devel
Summary:	Development files for the Offscreen output driver for QtGui v5
Group:		Development/KDE and Qt
Requires:	%{qtgui}-offscreen = %{EVRD}

%description -n %{qtgui}-offscreen-devel
Development files for the Offscreen output driver for QtGui v5.

%files -n %{qtgui}-offscreen-devel
%{_libdir}/cmake/Qt%{api}Gui/Qt%{api}Gui_QOffscreen*.cmake

#----------------------------------------------------------------------------

%package -n %{qtgui}-x11
Summary:	X11 output driver for QtGui v5
Group:		System/Libraries
Requires:	%{qtgui} = %{EVRD}
Provides:	%{_lib}qt5-output-driver = %{EVRD}
Provides:	%{_lib}qt5-output-driver-default = %{EVRD}
# (tpg) this is needed for %{_sysconfdir}/X11/xsetup.d/10-qt5-check-opengl.xsetup
Requires:	glxinfo
Requires:	dri-drivers >= 11.1.0-3

%description -n %{qtgui}-x11
X11 output driver for QtGui v5.

%files -n %{qtgui}-x11
%{_sysconfdir}/X11/xsetup.d/10-qt5-check-opengl.xsetup
%{_qt_plugindir}/platforms/libqxcb.so
%{_qt_plugindir}/platforminputcontexts/libcomposeplatforminputcontextplugin.so

%package -n %{qtgui}-x11-devel
Summary:	Development files for the X11 output driver for QtGui v5
Group:		Development/KDE and Qt
Requires:	%{qtgui}-x11 = %{EVRD}

%description -n %{qtgui}-x11-devel
Development files for the X11 output driver for QtGui v5.

%files -n %{qtgui}-x11-devel
%{_libdir}/cmake/Qt%{api}Gui/Qt5Gui_QComposePlatformInputContextPlugin.cmake
%{_libdir}/cmake/Qt%{api}Gui/Qt5Gui_QXcb*IntegrationPlugin.cmake
%{_includedir}/qt5/QtXkbCommonSupport/*/QtXkbCommonSupport
%{_includedir}/qt5/QtXkbCommonSupport
%{_libdir}/libQt5XkbCommonSupport.a
%{_libdir}/libQt5XkbCommonSupport.prl
%{_libdir}/cmake/Qt%{api}XkbCommonSupport

#----------------------------------------------------------------------------

%package -n %{qtgui}-ibus
Summary:	Ibus input driver for QtGui v5
Group:		System/Libraries
Requires:	%{qtgui} = %{EVRD}

%description -n %{qtgui}-ibus
Ibus input driver for QtGui v5.

%files -n %{qtgui}-ibus
%{_qt_plugindir}/platforminputcontexts/libibusplatforminputcontextplugin.so

%package -n %{qtgui}-ibus-devel
Summary:	Development files for the Ibus input driver for QtGui v5
Group:		Development/KDE and Qt
Requires:	%{qtgui}-ibus = %{EVRD}

%description -n %{qtgui}-ibus-devel
Development files for the Ibus input driver for QtGui v5.

%files -n %{qtgui}-ibus-devel
%{_libdir}/cmake/Qt%{api}Gui/Qt5Gui_QIbus*.cmake

#----------------------------------------------------------------------------

%package -n %{qtgui}-eglfs
Summary:	EGL fullscreen output driver for QtGui v5
Group:		System/Libraries
Requires:	%{qtgui} = %{EVRD}
Provides:	%{_lib}qt5-output-driver = %{EVRD}
Provides:	%{_lib}qt5-output-driver-eglfs = %{EVRD}

%description -n %{qtgui}-eglfs
EGL fullscreen output driver for QtGui v5.

%files -n %{qtgui}-eglfs
%{_qt_plugindir}/platforms/libqeglfs.so
%{_qt_libdir}/libQt%{api}EglFsKmsSupport.so.%{major}*
%if "%{_libdir}" != "%{_qt_libdir}"
%{_libdir}/libQt%{api}EglFsKmsSupport.so.%{major}*
%endif

#----------------------------------------------------------------------------

%package -n %{qtgui}-eglfs-devel
Summary:	Development files for the EGL fullscreen output driver for QtGui v5
Group:		System/Libraries
Requires:	%{qtgui} = %{EVRD}
Requires:	%{qtgui}-eglfs = %{EVRD}

%description -n %{qtgui}-eglfs-devel
Development files for the EGL fullscreen output driver for QtGui v5.

%files -n %{qtgui}-eglfs-devel
%{_qt_libdir}/libQt%{api}EglFsKmsSupport.so
%{_qt_libdir}/libQt%{api}EglFsKmsSupport.prl
%{_qt_includedir}/QtKmsSupport
%{_libdir}/libQt5KmsSupport.a
%{_libdir}/libQt5KmsSupport.prl
%{_libdir}/cmake/Qt%{api}Gui/Qt5Gui_QEglFS*.cmake
%{_libdir}/cmake/Qt%{api}EglFsKmsSupport
%{_libdir}/cmake/Qt%{api}KmsSupport

#----------------------------------------------------------------------------

%package -n %{qtgui}-minimalegl
Summary:	Minimalistic EGL output driver for QtGui v5
Group:		System/Libraries
Requires:	%{qtgui} = %{EVRD}
Provides:	%{_lib}qt5-output-driver = %{EVRD}

%description -n %{qtgui}-minimalegl
Minimalistic EGL output driver for QtGui v5.

%files -n %{qtgui}-minimalegl
%{_qt_plugindir}/platforms/libqminimalegl.so

#----------------------------------------------------------------------------

%package -n %{qtgui}-vnc
Summary:	VNC output driver for QtGui v5
Group:		System/Libraries
Requires:	%{qtgui} = %{EVRD}
Provides:	%{_lib}qt5-output-driver = %{EVRD}

%description -n %{qtgui}-vnc
VNC output driver for QtGui v5.

%files -n %{qtgui}-vnc
%{_qt_plugindir}/platforms/libqvnc.so

%package -n %{qtgui}-vnc-devel
Summary:	Development files for the VNC output driver for QtGui v5
Group:		Development/KDE and Qt
Requires:	%{qtgui}-vnc = %{EVRD}

%description -n %{qtgui}-vnc-devel
Development files for the VNC output driver for QtGui v5

%files -n %{qtgui}-vnc-devel
%{_libdir}/cmake/Qt%{api}Gui/Qt%{api}Gui_QVnc*.cmake

#----------------------------------------------------------------------------
%package -n %{qtnetwork}
Summary:	Qt Networking library
Group:		System/Libraries

%description -n %{qtnetwork}
Qt Networking library.

%files -n %{qtnetwork}
%{_qt_libdir}/libQt%{api}Network.so.%{major}*
%if "%{_qt_libdir}" != "%{_libdir}"
%{_libdir}/libQt%{api}Network.so.%{major}*
%endif
%{_qt_plugindir}/bearer

#----------------------------------------------------------------------------

%package -n %{qtnetworkd}
Summary:	Development files for version %{api} of the QtNetwork library
Group:		Development/KDE and Qt
Requires:	%{qtnetwork} = %{EVRD}

%description -n %{qtnetworkd}
Development files for version %{api} of the QtNetwork library.

%files -n %{qtnetworkd}
%{_qt_includedir}/QtNetwork
%{_qt_libdir}/libQt%{api}Network.so
%{_qt_libdir}/libQt%{api}Network.prl
%{_qt_libdir}/cmake/Qt%{api}Network
%{_qt_libdir}/pkgconfig/Qt%{api}Network.pc
%if "%{_qt_libdir}" != "%{_libdir}"
%{_libdir}/pkgconfig/Qt%{api}Network.pc
%endif

#----------------------------------------------------------------------------

%package -n %{qtopengl}
Summary:	Qt OpenGL (3D Graphics) library
Group:		System/Libraries

%description -n %{qtopengl}
Qt OpenGL (3D Graphics) library.

%files -n %{qtopengl}
%{_qt_libdir}/libQt%{api}OpenGL.so.%{major}*
%if "%{_qt_libdir}" != "%{_libdir}"
%{_libdir}/libQt%{api}OpenGL.so.%{major}*
%endif

#----------------------------------------------------------------------------

%package -n %{qtopengld}
Summary:	Development files for version 5 of the QtOpenGL library
Group:		Development/KDE and Qt
Requires:	%{qtopengl} = %{EVRD}

%description -n %{qtopengld}
Development files for version 5 of the QtOpenGL library.

%files -n %{qtopengld}
%{_qt_includedir}/QtOpenGL
%{_qt_includedir}/QtOpenGLExtensions
%{_qt_libdir}/libQt%{api}OpenGL.so
%{_qt_libdir}/libQt%{api}OpenGL.prl
%{_qt_libdir}/libQt%{api}OpenGLExtensions.a
%{_qt_libdir}/libQt%{api}OpenGLExtensions.prl
%{_qt_libdir}/cmake/Qt%{api}OpenGL
%{_qt_libdir}/cmake/Qt%{api}OpenGLExtensions
%{_qt_libdir}/pkgconfig/Qt%{api}OpenGL.pc
%{_qt_libdir}/pkgconfig/Qt%{api}OpenGLExtensions.pc
%if "%{_qt_libdir}" != "%{_libdir}"
%{_libdir}/pkgconfig/Qt%{api}OpenGL.pc
%{_libdir}/pkgconfig/Qt%{api}OpenGLExtensions.pc
%endif

#----------------------------------------------------------------------------
%package -n %{qtprintsupport}
Summary:	Qt printing library
Group:		System/Libraries

%description -n %{qtprintsupport}
Qt printing library.

%files -n %{qtprintsupport}
%{_qt_libdir}/libQt%{api}PrintSupport.so.%{major}*
%if "%{_qt_libdir}" != "%{_libdir}"
%{_libdir}/libQt%{api}PrintSupport.so.%{major}*
%endif

#----------------------------------------------------------------------------

%package -n %{qtprintsupportd}
Summary:	Development files for version 5 of the QtPrintSupport library
Group:		Development/KDE and Qt
Requires:	%{qtprintsupport} = %{EVRD}

%description -n %{qtprintsupportd}
Development files for version 5 of the QtPrintSupport library.

%files -n %{qtprintsupportd}
%{_qt_includedir}/QtPrintSupport
%{_qt_libdir}/libQt%{api}PrintSupport.so
%{_qt_libdir}/libQt%{api}PrintSupport.prl
%{_qt_libdir}/cmake/Qt%{api}PrintSupport
%{_qt_libdir}/pkgconfig/Qt%{api}PrintSupport.pc
%if "%{_qt_libdir}" != "%{_libdir}"
%{_libdir}/pkgconfig/Qt%{api}PrintSupport.pc
%endif
#----------------------------------------------------------------------------

%package -n %{qtsql}
Summary:	Qt SQL library
Group:		System/Libraries

%description -n %{qtsql}
Qt SQL library.

%files -n %{qtsql}
%{_qt_libdir}/libQt%{api}Sql.so.%{major}*
%if "%{_qt_libdir}" != "%{_libdir}"
%{_libdir}/libQt%{api}Sql.so.%{major}*
%endif
%dir %{_qt_plugindir}/sqldrivers

#----------------------------------------------------------------------------

%package -n %{qtsqld}
Summary:	Development files for version 5 of the QtSql library
Group:		Development/KDE and Qt
Requires:	%{qtsql} = %{EVRD}
# We need all the QtSql plugins because the plugin related cmake files in
# %{_qt_libdir}/cmake/Qt%{api}Sql cause fatal errors if the plugins aren't
# installed.
%if %{with mysql}
Requires:	%{qtsql}-mysql = %{EVRD}
%endif
Requires:	%{qtsql}-odbc = %{EVRD}
Requires:	%{qtsql}-postgresql = %{EVRD}
Requires:	%{qtsql}-sqlite = %{EVRD}
Requires:	%{qtsql}-tds = %{EVRD}

%description -n %{qtsqld}
Development files for version 5 of the QtSql library.

%files -n %{qtsqld}
%{_qt_includedir}/QtSql
%{_qt_libdir}/libQt%{api}Sql.so
%{_qt_libdir}/libQt%{api}Sql.prl
%{_qt_libdir}/cmake/Qt%{api}Sql
%{_qt_libdir}/pkgconfig/Qt%{api}Sql.pc
%if "%{_qt_libdir}" != "%{_libdir}"
%{_libdir}/pkgconfig/Qt%{api}Sql.pc
%endif

#----------------------------------------------------------------------------

%if %{with mysql}
%package -n %{qtsql}-mysql
Summary:	MySQL support for the QtSql library v5
Group:		System/Libraries
Requires:	%{qtsql} = %{EVRD}
Provides:	%{name}-database-plugin-mysql = %{EVRD}
BuildRequires:	pkgconfig(mariadb)

%description -n %{qtsql}-mysql
MySQL support for the QtSql library v5.

%files -n %{qtsql}-mysql
%{_qt_plugindir}/sqldrivers/libqsqlmysql.so
%endif
#----------------------------------------------------------------------------

%package -n %{qtsql}-odbc
Summary:	ODBC support for the QtSql library v5
Group:		System/Libraries
Requires:	%{qtsql} = %{EVRD}
Provides:	%{name}-database-plugin-odbc = %{EVRD}
BuildRequires:	pkgconfig(libiodbc)
BuildRequires:	unixODBC-devel

%description -n %{qtsql}-odbc
ODBC support for the QtSql library v5.

%files -n %{qtsql}-odbc
%{_qt_plugindir}/sqldrivers/libqsqlodbc.so

#----------------------------------------------------------------------------

%package -n %{qtsql}-postgresql
Summary:	PostgreSQL support for the QtSql library v5
Group:		System/Libraries
Requires:	%{qtsql} = %{EVRD}
Provides:	%{name}-database-plugin-postgresql = %{EVRD}
BuildRequires:	postgresql-devel >= 9.0

%description -n %{qtsql}-postgresql
PostgreSQL support for the QtSql library v5.

%files -n %{qtsql}-postgresql
%{_qt_plugindir}/sqldrivers/libqsqlpsql.so

#----------------------------------------------------------------------------

%package -n %{qtsql}-sqlite
Summary:	SQLite 3.x support for the QtSql library v5
Group:		System/Libraries
Requires:	%{qtsql} = %{EVRD}
Provides:	%{name}-database-plugin-sqlite = %{EVRD}
%rename		qt5-database-plugin-sqlite
BuildRequires:	pkgconfig(sqlite3)
# Let's not build support for prehistoric sqlite 2.x
BuildConflicts:	pkgconfig(sqlite)

%description -n %{qtsql}-sqlite
SQLite 3.x support for the QtSql library v5.

%files -n %{qtsql}-sqlite
%{_qt_plugindir}/sqldrivers/libqsqlite.so

#----------------------------------------------------------------------------

%package -n %{qtsql}-tds
Summary:	TDS (MS SQL) support for the QtSql library v5
Group:		System/Libraries
Requires:	%{qtsql} = %{EVRD}
Provides:	%{name}-database-plugin-tds = %{EVRD}
BuildRequires:	freetds-devel

%description -n %{qtsql}-tds
TDS (MS SQL) support for the QtSql library v5.

%files -n %{qtsql}-tds
%{_qt_plugindir}/sqldrivers/libqsqltds.so


#----------------------------------------------------------------------------

%package -n %{qttest}
Summary:	Qt unit test library
Group:		System/Libraries

%description -n %{qttest}
Qt unit test library.

%files -n %{qttest}
%{_qt_libdir}/libQt%{api}Test.so.%{major}*
%if "%{_qt_libdir}" != "%{_libdir}"
%{_libdir}/libQt%{api}Test.so.%{major}*
%endif

#----------------------------------------------------------------------------

%package -n %{qttestd}
Summary:	Development files for version 5 of the QtTest library
Group:		Development/KDE and Qt
Requires:	%{qttest} = %{EVRD}

%description -n %{qttestd}
Development files for version 5 of the QtTest library.

%files -n %{qttestd}
%{_qt_includedir}/QtTest
%{_qt_libdir}/libQt%{api}Test.so
%{_qt_libdir}/libQt%{api}Test.prl
%{_qt_libdir}/cmake/Qt%{api}Test
%{_qt_libdir}/pkgconfig/Qt%{api}Test.pc
%if "%{_qt_libdir}" != "%{_libdir}"
%{_libdir}/pkgconfig/Qt%{api}Test.pc
%endif

#----------------------------------------------------------------------------

%package -n %{qtwidgets}
Summary:	Qt Widget library
Group:		System/Libraries

%description -n %{qtwidgets}
Qt Widget library.

%files -n %{qtwidgets}
%{_qt_libdir}/libQt%{api}Widgets.so.%{major}*
%if "%{_qt_libdir}" != "%{_libdir}"
%{_libdir}/libQt%{api}Widgets.so.%{major}*
%endif
%{_libdir}/metatypes/qt5widgets_metatypes.json

#----------------------------------------------------------------------------

%package -n %{qtwidgetsd}
Summary:	Development files for version 5 of the QtWidgets library
Group:		Development/KDE and Qt
Requires:	%{qtwidgets} = %{EVRD}

%description -n %{qtwidgetsd}
Development files for version 5 of the QtWidgets library.

%files -n %{qtwidgetsd}
%{_qt_includedir}/QtWidgets
%{_qt_libdir}/libQt%{api}Widgets.so
%{_qt_libdir}/libQt%{api}Widgets.prl
%{_qt_libdir}/cmake/Qt%{api}Widgets
%{_qt_libdir}/pkgconfig/Qt%{api}Widgets.pc
%if "%{_qt_libdir}" != "%{_libdir}"
%{_libdir}/pkgconfig/Qt%{api}Widgets.pc
%endif

#----------------------------------------------------------------------------
%package -n %{qtxcbqpa}
Summary:	Qt XCB QPA library
Group:		System/Libraries

%description -n %{qtxcbqpa}
Qt XCB QPA library.

%files -n %{qtxcbqpa}
%{_qt_libdir}/libQt%{api}XcbQpa.so.%{major}*
%if "%{_qt_libdir}" != "%{_libdir}"
%{_libdir}/libQt%{api}XcbQpa.so.%{major}*
%endif
%{_qt_plugindir}/xcbglintegrations

#----------------------------------------------------------------------------

%package -n %{qtxcbqpad}
Summary:	Development files for version 5 of the QtXcbQpa library
Group:		Development/KDE and Qt
Requires:	%{qtxcbqpa} = %{EVRD}

%description -n %{qtxcbqpad}
Development files for version 5 of the QtXcbQpa library.

%files -n %{qtxcbqpad}
%{_qt_libdir}/libQt%{api}XcbQpa.so
%{_qt_libdir}/libQt%{api}XcbQpa.prl
%{_libdir}/cmake/Qt%{api}XcbQpa


#----------------------------------------------------------------------------
%package -n %{qtxml}
Summary:	Qt XML library
Group:		System/Libraries

%description -n %{qtxml}
Qt XML library.

%files -n %{qtxml}
%{_qt_libdir}/libQt%{api}Xml.so.%{major}*
%if "%{_qt_libdir}" != "%{_libdir}"
%{_libdir}/libQt%{api}Xml.so.%{major}*
%endif

#----------------------------------------------------------------------------

%package -n %{qtxmld}
Summary:	Development files for version 5 of the QtXml library
Group:		Development/KDE and Qt
Requires:	%{qtxml} = %{EVRD}

%description -n %{qtxmld}
Development files for version 5 of the QtXml library.

%files -n %{qtxmld}
%{_qt_includedir}/QtXml
%{_qt_libdir}/libQt%{api}Xml.so
%{_qt_libdir}/libQt%{api}Xml.prl
%{_qt_libdir}/cmake/Qt%{api}Xml
%{_qt_libdir}/pkgconfig/Qt%{api}Xml.pc
%if "%{_qt_libdir}" != "%{_libdir}"
%{_libdir}/pkgconfig/Qt%{api}Xml.pc
%endif

#----------------------------------------------------------------------------
# qt extras
#----------------------------------------------------------------------------
%package devel
Summary:	Meta-package for installing all Qt 5 Base development files
Group:		Development/KDE and Qt
Requires:	%{qtbootstrapd} = %{EVRD}
Requires:	%{qtconcurrentd} = %{EVRD}
Requires:	%{qtcored} = %{EVRD}
Requires:	%{qtdbusd} = %{EVRD}
Requires:	%{qtegldeviceintegrationd} = %{EVRD}
Requires:	%{qtguid} = %{EVRD}
Requires:	%{qtnetworkd} = %{EVRD}
Requires:	%{qtopengld} = %{EVRD}
Requires:	%{qtprintsupportd} = %{EVRD}
Requires:	%{qtsqld} = %{EVRD}
Requires:	%{qtwidgetsd} = %{EVRD}
Requires:	%{qtxcbqpad} = %{EVRD}
Requires:	%{qtxmld} = %{EVRD}
Requires:	qmake%{api} = %{EVRD}
Requires:	qlalr%{api} = %{EVRD}
Requires:	qt5-macros = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Suggests:	%{qtaccessibilitysupportd} = %{EVRD}
Suggests:	%{qtedidsupportd} = %{EVRD}
Suggests:	%{qtvulkansupportd} = %{EVRD}
Suggests:	%{qtdevicediscoverysupportd} = %{EVRD}
Suggests:	%{qteglsupportd} = %{EVRD}
Suggests:	%{qteventdispatchersupportd} = %{EVRD}
Suggests:	%{qtfbsupportd} = %{EVRD}
Suggests:	%{qtfontdatabasesupportd} = %{EVRD}
Suggests:	%{qtglxsupportd} = %{EVRD}
Suggests:	%{qtinputsupportd} = %{EVRD}
Suggests:	%{qtlinuxaccessibilitysupportd} = %{EVRD}
Suggests:	%{qtplatformcompositorsupportd} = %{EVRD}
Suggests:	%{qtservicesupportd} = %{EVRD}
Suggests:	%{qtthemesupportd} = %{EVRD}

%description devel
Meta-package for installing all Qt 5 Base development files.

%files devel
# Intentionally empty, we just pull in dependencies

#----------------------------------------------------------------------------
# qt extras
#----------------------------------------------------------------------------
%package -n qt5-devel
Summary:	Meta-package for installing all Qt 5 development files
Group:		Development/KDE and Qt
Requires:	%{name}-devel = %{EVRD}
%if !%{with bootstrap}
Requires:	pkgconfig(Enginio) >= 1.1.0
Requires:	pkgconfig(Qt5Bluetooth) = %{version}
Requires:	pkgconfig(Qt5Location) = %{version}
Requires:	pkgconfig(Qt5Positioning) = %{version}
Requires:	pkgconfig(Qt5Sensors) = %{version}
Requires:	pkgconfig(Qt5Test) = %{version}
Requires:	pkgconfig(Qt5Designer) = %{version}
Requires:	pkgconfig(Qt5Help) = %{version}
Requires:	pkgconfig(Qt5Multimedia) = %{version}
Requires:	pkgconfig(Qt5MultimediaWidgets) = %{version}
Requires:	pkgconfig(Qt5Nfc) = %{version}
Requires:	pkgconfig(Qt5Qml) = %{version}
Requires:	pkgconfig(Qt5Quick) = %{version}
Requires:	pkgconfig(Qt5QuickTest) = %{version}
Requires:	pkgconfig(Qt5QuickWidgets) = %{version}
Requires:	pkgconfig(Qt5Script) = %{version}
Requires:	pkgconfig(Qt5ScriptTools) = %{version}
Requires:	pkgconfig(Qt5Svg) = %{version}
Suggests:	pkgconfig(Qt5WaylandClient) = %{version}
Suggests:	pkgconfig(Qt5WaylandCompositor) = %{version}
%ifnarch %arm
Requires:	pkgconfig(Qt5WebEngine) >= %{version}
%endif
Requires:	pkgconfig(Qt5WebChannel) = %{version}
Requires:	pkgconfig(Qt5WebSockets) = %{version}
Requires:	pkgconfig(Qt5XmlPatterns) = %{version}
%endif

%description -n qt5-devel
Meta-package for installing all Qt 5 development files.

%files -n qt5-devel
# Intentionally empty, we just pull in dependencies

#----------------------------------------------------------------------------
# qt tools etc
#----------------------------------------------------------------------------

%if %{with docs}
%package -n qt5-doc
Summary:	Qt QCH documentation
Group:		Books/Computer books
BuildArch:	noarch
# Was introduced by mistake
%rename %{name}-doc

%description -n qt5-doc
QCH documentation for the Qt toolkit.

%files -n qt5-doc
%{_qt_docdir}/*.{tags,qch}
%{_qt_docdir}/config/exampleurl-*.qdocconf
%endif

#----------------------------------------------------------------------------
%package -n qt5-porting-tools
Summary:	Tools that help porting code from Qt 4.x to 5.x
Group:		Development/Tools

%description -n qt5-porting-tools
Tools that help porting code from Qt 4.x to 5.x

%files -n qt5-porting-tools
%{_qt_bindir}/fixqt4headers.pl
%{_bindir}/fixqt4headers.pl

#----------------------------------------------------------------------------

%package -n qt5-examples
Summary:	Example applications for %{name}
Group:		Development/KDE and Qt
# Was introduced by mistake
%rename %{name}-examples

%description -n qt5-examples
Example applications for %{name}.

%files -n qt5-examples
%{_qt_exampledir}

#----------------------------------------------------------------------------

%package -n qt5-macros
Summary:	Base macros for Qt 5
Group:		Development/KDE and Qt
# Was introduced by mistake
%rename %{name}-macros

%description -n qt5-macros
Base macros for Qt 5.

%files -n qt5-macros
%{_sysconfdir}/rpm/macros.d/qt5.macros

#----------------------------------------------------------------------------
%package -n qt5-platformtheme-xdgdesktopportal
Summary:	XDG Desktop Portal platform theme for Qt 5
Group:		Graphical desktop/KDE
Requires:	%{qtgui} = %{EVRD}
%if %{with gtk}
BuildRequires:	pkgconfig(gtk+-x11-3.0)
%endif
Obsoletes:	qt5-platformtheme-flatpak < %{EVRD}

%description -n qt5-platformtheme-xdgdesktopportal
XDG Desktop Portal platform theme for Qt 5.

%files -n qt5-platformtheme-xdgdesktopportal
%{_qt_plugindir}/platformthemes/libqxdgdesktopportal.so

%package -n qt5-platformtheme-xdgdesktopportal-devel
Summary:	Development files for the Qt5 XDG Desktop Portal platform theme integration
Group:		Development/KDE and Qt
Requires:	qt5-platformtheme-xdgdesktopportal = %{EVRD}

%description -n qt5-platformtheme-xdgdesktopportal-devel
Development files for the Qt5 XDG Desktop Portal platform theme integration

%files -n qt5-platformtheme-xdgdesktopportal-devel
%{_libdir}/cmake/Qt%{api}Gui/Qt5Gui_QXdgDesktopPortalThemePlugin.cmake

#----------------------------------------------------------------------------
%if %{with gtk}
%package -n qt5-platformtheme-gtk3
Summary:	GTK 3.x platform theme for Qt 5
Group:		Graphical desktop/KDE
Requires:	%{qtgui} = %{EVRD}
Provides:	%{name}-platformtheme-gtk3 = %{EVRD}
BuildRequires:	pkgconfig(gtk+-x11-3.0)
# Not really... But the gtk2 platformtheme doesn't exist anymore for >= 5.7
%rename	qt5-platformtheme-gtk2

%description -n qt5-platformtheme-gtk3
GTK 3.x platform theme for Qt 5. This plugin allows Qt to render
controls using GTK 3.x themes - making it integrate better with GTK
based desktops.

%files -n qt5-platformtheme-gtk3
%{_qt_plugindir}/platformthemes/libqgtk3.so

%package -n qt5-platformtheme-gtk3-devel
Summary:	Development files for the Qt5 GTK3 platform theme integration
Group:		Development/KDE and Qt
Requires:	qt5-platformtheme-gtk3 = %{EVRD}

%description -n qt5-platformtheme-gtk3-devel
Development files for the Qt5 GTK3 platform theme integration

%files -n qt5-platformtheme-gtk3-devel
%{_libdir}/cmake/Qt%{api}Gui/Qt5Gui_QGtk3ThemePlugin.cmake
%endif

#----------------------------------------------------------------------------
%package -n %{qtaccessibilitysupportd}
Summary:	Helper library for Qt accessibility support
Group:		Graphical desktop/KDE
Requires:	%{qtcored} = %{EVRD}

%description -n %{qtaccessibilitysupportd}
Helper library for Qt accessibility support

%files -n %{qtaccessibilitysupportd}
%{_includedir}/qt%{api}/QtAccessibilitySupport
%{_libdir}/libQt%{api}AccessibilitySupport.a
%{_libdir}/libQt%{api}AccessibilitySupport.prl
%{_libdir}/pkgconfig/Qt5LinuxAccessibilitySupport.pc
%{_libdir}/cmake/Qt%{api}AccessibilitySupport

#----------------------------------------------------------------------------
%package -n %{qtedidsupportd}
Summary:	Helper library for Qt accessibility support
Group:		Graphical desktop/KDE
Requires:	%{qtcored} = %{EVRD}

%description -n %{qtedidsupportd}
Helper library for Qt EDID support

%files -n %{qtedidsupportd}
%{_includedir}/qt%{api}/QtEdidSupport
%{_libdir}/libQt%{api}EdidSupport.a
%{_libdir}/libQt%{api}EdidSupport.prl
%{_libdir}/cmake/Qt%{api}EdidSupport

#----------------------------------------------------------------------------
%package -n %{qtvulkansupportd}
Summary:	Helper library for Qt Vulkan support
Group:		Graphical desktop/KDE
Requires:	%{qtcored} = %{EVRD}

%description -n %{qtvulkansupportd}
Helper library for Qt Vulkan support

%files -n %{qtvulkansupportd}
%{_includedir}/qt%{api}/QtVulkanSupport
%{_libdir}/libQt%{api}VulkanSupport.a
%{_libdir}/libQt%{api}VulkanSupport.prl
%{_libdir}/qt%{api}/bin/qvkgen
%{_libdir}/cmake/Qt%{api}VulkanSupport

#----------------------------------------------------------------------------
%package -n %{qtdevicediscoverysupportd}
Summary:	Helper library for Qt device discovery
Group:		Graphical desktop/KDE
Requires:	%{qtcored} = %{EVRD}

%description -n %{qtdevicediscoverysupportd}
Helper library for Qt device discovery

%files -n %{qtdevicediscoverysupportd}
%{_includedir}/qt%{api}/QtDeviceDiscoverySupport
%{_libdir}/libQt%{api}DeviceDiscoverySupport.a
%{_libdir}/libQt%{api}DeviceDiscoverySupport.prl
%{_libdir}/cmake/Qt%{api}DeviceDiscoverySupport

#----------------------------------------------------------------------------
%package -n %{qteglsupportd}
Summary:	Helper library for Qt EGL support
Group:		Graphical desktop/KDE
Requires:	%{qtcored} = %{EVRD}

%description -n %{qteglsupportd}
Helper library for Qt EGL support

%files -n %{qteglsupportd}
%{_includedir}/qt%{api}/QtEglSupport
%{_libdir}/libQt%{api}EglSupport.a
%{_libdir}/libQt%{api}EglSupport.prl
%{_libdir}/cmake/Qt%{api}EglSupport

#----------------------------------------------------------------------------
%package -n %{qteventdispatchersupportd}
Summary:	Helper library for Qt event dispatcher support
Group:		Graphical desktop/KDE
Requires:	%{qtcored} = %{EVRD}

%description -n %{qteventdispatchersupportd}
Helper library for Qt event dispatcher support

%files -n %{qteventdispatchersupportd}
%{_includedir}/qt%{api}/QtEventDispatcherSupport
%{_libdir}/libQt%{api}EventDispatcherSupport.a
%{_libdir}/libQt%{api}EventDispatcherSupport.prl
%{_libdir}/cmake/Qt%{api}EventDispatcherSupport

#----------------------------------------------------------------------------
%package -n %{qtfbsupportd}
Summary:	Helper library for Qt framebuffer support
Group:		Graphical desktop/KDE
Requires:	%{qtcored} = %{EVRD}

%description -n %{qtfbsupportd}
Helper library for Qt framebuffer support

%files -n %{qtfbsupportd}
%{_includedir}/qt%{api}/QtFbSupport
%{_libdir}/libQt%{api}FbSupport.a
%{_libdir}/libQt%{api}FbSupport.prl
%{_libdir}/cmake/Qt%{api}Gui/Qt%{api}Gui_QLinuxFb*.cmake
%{_libdir}/cmake/Qt%{api}FbSupport

#----------------------------------------------------------------------------
%package -n %{qtfontdatabasesupportd}
Summary:	Helper library for Qt font database support
Group:		Graphical desktop/KDE
Requires:	%{qtcored} = %{EVRD}

%description -n %{qtfontdatabasesupportd}
Helper library for Qt font database support

%files -n %{qtfontdatabasesupportd}
%{_includedir}/qt%{api}/QtFontDatabaseSupport
%{_libdir}/libQt%{api}FontDatabaseSupport.a
%{_libdir}/libQt%{api}FontDatabaseSupport.prl
%{_libdir}/cmake/Qt%{api}FontDatabaseSupport

#----------------------------------------------------------------------------
%package -n %{qtglxsupportd}
Summary:	Helper library for Qt GLX support
Group:		Graphical desktop/KDE
Requires:	%{qtcored} = %{EVRD}

%description -n %{qtglxsupportd}
Helper library for Qt GLX support

%files -n %{qtglxsupportd}
%{_includedir}/qt%{api}/QtGlxSupport
%{_libdir}/libQt%{api}GlxSupport.a
%{_libdir}/libQt%{api}GlxSupport.prl
%{_libdir}/cmake/Qt%{api}GlxSupport

#----------------------------------------------------------------------------
%package -n %{qtinputsupportd}
Summary:	Helper library for Qt input support
Group:		Graphical desktop/KDE
Requires:	%{qtcored} = %{EVRD}

%description -n %{qtinputsupportd}
Helper library for Qt input support

%files -n %{qtinputsupportd}
%{_includedir}/qt%{api}/QtInputSupport
%{_libdir}/libQt%{api}InputSupport.a
%{_libdir}/libQt%{api}InputSupport.prl
%{_libdir}/cmake/Qt%{api}InputSupport

#----------------------------------------------------------------------------
%package -n %{qtlinuxaccessibilitysupportd}
Summary:	Helper library for Qt Linux accessibility support
Group:		Graphical desktop/KDE
Requires:	%{qtcored} = %{EVRD}

%description -n %{qtlinuxaccessibilitysupportd}
Helper library for Qt Linux accessibility support

%files -n %{qtlinuxaccessibilitysupportd}
%{_includedir}/qt%{api}/QtLinuxAccessibilitySupport
%{_libdir}/libQt%{api}LinuxAccessibilitySupport.a
%{_libdir}/libQt%{api}LinuxAccessibilitySupport.prl
%{_libdir}/cmake/Qt%{api}LinuxAccessibilitySupport

#----------------------------------------------------------------------------
%package -n %{qtplatformcompositorsupportd}
Summary:	Helper library for Qt platform compositor support
Group:		Graphical desktop/KDE
Requires:	%{qtcored} = %{EVRD}

%description -n %{qtplatformcompositorsupportd}
Helper library for Qt platform compositor support

%files -n %{qtplatformcompositorsupportd}
%{_includedir}/qt%{api}/QtPlatformCompositorSupport
%{_libdir}/libQt%{api}PlatformCompositorSupport.a
%{_libdir}/libQt%{api}PlatformCompositorSupport.prl
%{_libdir}/cmake/Qt%{api}PlatformCompositorSupport

#----------------------------------------------------------------------------
%package -n %{qtservicesupportd}
Summary:	Helper library for Qt service support
Group:		Graphical desktop/KDE
Requires:	%{qtcored} = %{EVRD}

%description -n %{qtservicesupportd}
Helper library for Qt service support

%files -n %{qtservicesupportd}
%{_includedir}/qt%{api}/QtServiceSupport
%{_libdir}/libQt%{api}ServiceSupport.a
%{_libdir}/libQt%{api}ServiceSupport.prl
%{_libdir}/cmake/Qt%{api}ServiceSupport

#----------------------------------------------------------------------------
%package -n %{qtthemesupportd}
Summary:	Helper library for Qt theme support
Group:		Graphical desktop/KDE
Requires:	%{qtcored} = %{EVRD}

%description -n %{qtthemesupportd}
Helper library for Qt theme support

%files -n %{qtthemesupportd}
%{_includedir}/qt%{api}/QtThemeSupport
%{_libdir}/libQt%{api}ThemeSupport.a
%{_libdir}/libQt%{api}ThemeSupport.prl
%{_libdir}/cmake/Qt%{api}ThemeSupport

#----------------------------------------------------------------------------

%package -n qmake%{api}
Summary:	Makefile generation system for Qt 5
Group:		Development/KDE and Qt
Requires:	%{name}-macros = %{EVRD}

%description -n qmake%{api}
Makefile generation system for Qt 5.

%files -n qmake%{api}
%{_bindir}/qmake-qt%{api}
%{_bindir}/qmake
%{_qt_bindir}/qmake
%{_qt_prefix}/mkspecs

#----------------------------------------------------------------------------

%package -n qlalr%{api}
Summary:	Qt LALR parser generator
Group:		Development/KDE and Qt
Provides:	qlalr = %{EVRD}

%description -n qlalr%{api}
Qt LALR parser generator.

%files -n qlalr%{api}
%{_qt_bindir}/qlalr
%{_bindir}/qlalr

#----------------------------------------------------------------------------

%prep
%autosetup -n %qttarballdir -p1
# respect cflags
sed -i -e '/^CPPFLAGS\s*=/ s/-g //' qmake/Makefile.unix
sed -i -e "s|^\(QMAKE_LFLAGS_RELEASE.*\)|\1 %{ldflags}|" mkspecs/common/g++-unix.conf
OPTFLAGS="%{optflags}"
%ifarch %{arm}
OPTFLAGS="`echo ${OPTFLAGS} |sed -e 's,-mfpu=neon ,-mfpu=neon-vfpv4 ,g;s,-mfpu=neon$,-mfpu=neon-vfpv4,'`"
%endif
sed -i -e "s|-O2|${OPTFLAGS}|g" mkspecs/common/gcc-base.conf
sed -i -e "s|-O3|${OPTFLAGS}|g" mkspecs/common/gcc-base.conf
%if !%{without clang}
sed -i -e "s|gcc-nm|llvm-nm|g" mkspecs/common/clang.conf
# drop flags that clang doesn't recognize
sed -i -e "s|-fvar-tracking-assignments||g" mkspecs/common/gcc-base.conf
sed -i -e "s|-frecord-gcc-switches||g" mkspecs/common/gcc-base.conf
sed -i -e "s|-Wp,-D_FORTIFY_SOURCE=2||g" mkspecs/common/gcc-base.conf

# Make sure we have -flto in the linker flags if we have it in the compiler
# flags...
cat >>mkspecs/common/clang.conf <<'EOF'
QMAKE_LFLAGS += $$QMAKE_CXXFLAGS
QMAKE_LFLAGS_RELEASE += $$QMAKE_CXXFLAGS_RELEASE
QMAKE_LFLAGS_DEBUG += $$QMAKE_CXXFLAGS_DEBUG
EOF
cat >>mkspecs/common/g++-unix.conf <<'EOF'
QMAKE_LFLAGS += $$QMAKE_CXXFLAGS
QMAKE_LFLAGS_RELEASE += $$QMAKE_CXXFLAGS_RELEASE
QMAKE_LFLAGS_DEBUG += $$QMAKE_CXXFLAGS_DEBUG
EOF
%endif

# drop weird X11R6 lib from path in *.pc files
sed -i 's!X11R6/!!g' mkspecs/linux-g++*/qmake.conf

# There's a bogus /lib and /usr/lib hardcode in configure...
%if "%{_lib}" != "lib"
sed -i -e 's,/lib\\,/%{_lib}\\,g' configure
%endif

# Pass CXXFLAGS to CXX even while linking -- for LTO
sed -i -e 's,\$(CXX) -o,\$(CXX) \$(CXXFLAGS) -o,' qmake/Makefile.unix

# move some bundled libs to ensure they're not accidentally used
pushd src/3rdparty
mkdir UNUSED
# FIXME
mv freetype libjpeg libpng zlib xcb sqlite UNUSED/
popd

%ifnarch %{riscv}
# Check for clang bug #28194
cat >test1.cpp <<'EOF'
struct A {} a;
EOF
cat >test2.cpp <<'EOF'
enum A {} a;
EOF
%{__cxx} -Os -gdwarf-4 -flto -fPIC -o test1.o -c test1.cpp
%{__cxx} -Os -gdwarf-4 -flto -fPIC -o test2.o -c test2.cpp
if LC_ALL=C %{__cxx} -Os -gdwarf-4 -flto -fPIC -shared -fuse-ld=gold -o test.so test1.o test2.o 2>&1 |grep -q "invalid debug info"; then
	echo "Applying workaround for clang bug #28194"
	sed -i -e 's,Operator,ComparisonOperator,g' src/gui/opengl/qopengl.cpp
elif ! echo %{__cxx} |grep -q clang; then
	echo "Not using clang - workaround not needed"
else
	echo "Clang bug #28194 is fixed, please remove the workaround"
	echo "(search the spec file for \"Check for clang bug #28194\")"
	exit 1
fi
%endif

%build
%setup_compile_flags
# build with python2
mkdir pybin
ln -s %{_bindir}/python2 pybin/python
export PATH="$(pwd)/pybin:$PATH"

# As of Qt 5.12.0, clang 7.0.1 (and gcc 8.2.0),
# -reduce-relocations breaks the signal/slot system badly.
# Immediately obvious effect: sddm crashes
# Probably related to
# https://bugreports.qt.io/browse/QTBUG-52439
./configure \
	-prefix %{_qt_prefix} \
	-bindir %{_qt_bindir} \
	-libdir %{_qt_libdir} \
	-datadir %{_qt_datadir} \
	-docdir %{_qt_docdir} \
	-headerdir %{_qt_includedir} \
	-plugindir %{_qt_plugindir} \
	-importdir %{_qt_importdir} \
	-translationdir %{_qt_translationsdir} \
	-sysconfdir %{_qt_sysconfdir} \
	-examplesdir %{_qt_exampledir} \
	-testsdir %{_qt_testsdir} \
	-release \
	-opensource \
	-shared \
	-accessibility \
	-no-sql-db2 \
	-no-sql-ibase \
%if %{with mysql}
	-sql-mysql \
%else
	-no-sql-mysql \
%endif
	-sql-odbc \
	-sql-psql \
	-sql-sqlite \
	-sqlite \
%if %{without clang}
%ifarch %{x86_64} %{aarch64}
	-platform linux-g++-64 \
%endif
%ifarch %{ix86}
	-platform linux-g++-32 \
%endif
%ifarch %{armx}
	-platform linux-g++ \
%endif
%else
	-platform linux-clang \
%endif
	-system-zlib \
	-system-libpng \
	-system-libjpeg \
	-system-pcre \
	-system-harfbuzz \
	-system-freetype  \
	-system-doubleconversion \
	-optimized-qmake \
	-optimized-tools \
	-sctp \
	-ssl \
	-xcb \
	-openssl-linked \
	-cups \
	-icu \
	-inotify \
	-eventfd \
	-no-strip \
	-pch \
	-ltcg \
	-nomake tests \
	-dbus-linked \
%ifarch %{armx}
	-no-sse2 \
	-no-sse3 \
	-no-ssse3 \
	-no-sse4.1 \
	-no-sse4.2 \
	-no-avx \
	-no-avx2 \
%endif
%ifarch znver1
	-sse2 \
	-sse3 \
	-ssse3 \
	-sse4.1 \
	-sse4.2 \
	-avx \
	-avx2 \
%endif
%ifarch x86_64
	-sse2 \
	-sse3 \
	-avx \
%endif
	-reduce-exports \
	-no-reduce-relocations \
%if %{with directfb}
	-directfb \
%else
	-no-directfb \
%endif
%if %{with gtk}
	-gtk \
%endif
	-fontconfig \
	-accessibility \
	-opengl desktop -egl -eglfs -gbm -kms \
	-gnumake \
	-pkg-config \
	-sm \
	-gif \
	-ico \
	-c++std c++2a \
	-confirm-license \
	-system-proxies \
	-mtdev \
	-journald \
	-linuxfb \
	-evdev \
	-libudev \
	-qpa xcb \
	-xcb-xlib \
	-no-separate-debug-info \
	-no-strip \
	-xkbcommon \
%if "%{_qt_libdir}" == "%{_libdir}"
	-no-rpath \
%endif
	-I %{_includedir}/iodbc \
%if %{with mysql}
	-I %{_includedir}/mysql \
%endif
	-I %{_includedir}/vg \
%if 0%{cross_compiling}
	-sysroot %{_prefix}%{_target_platform} -gcc-sysroot \
%endif
	-D PCRE2_CODE_UNIT_WIDTH=16

%make_build STRIP=/bin/true || make STRIP=/bin/true

%if %{with docs}
%make_build docs
%endif

%install
export PATH="$(pwd)/pybin:$PATH"

%make_install STRIP=/bin/true INSTALL_ROOT=%{buildroot}

# Drop internal libpng -- we don't actually use it,
# but the qmake files insist on building it
rm -f %{buildroot}%{_libdir}/libqtlibpng.*

%if %{with docs}
make install_qch_docs INSTALL_ROOT=%{buildroot}
cp doc/*/*.tags %{buildroot}%{_qt_docdir}/
%else
rm -f %{buildroot}%{_qt_docdir}/config/exampleurl-*.qdocconf
%endif

# Those will eventually get installed... By the qt5-qtdeclarative
# source package.
# Not sure why they exist in the qtcore sources as well, probably an
# upstream packaging bug.
rm -rf	%{buildroot}%{_libdir}/cmake/Qt%{api}PacketProtocol \
	%{buildroot}%{_libdir}/cmake/Qt%{api}QmlDebug \
	%{buildroot}%{_libdir}/cmake/Qt%{api}QmlDevTools \
	%{buildroot}%{_libdir}/cmake/Qt%{api}QuickParticles \
	%{buildroot}%{_libdir}/cmake/Qt%{api}QuickShapes

# Probably not useful outside of Qt source tree?
rm -f %{buildroot}%{_qt_bindir}/qtmodule-configtests
# Let's not ship -devel files for private libraries... At least not until
# applications teach us otherwise
rm -f %{buildroot}%{_qt_libdir}/libQt%{api}MultimediaQuick_p.so %{buildroot}%{_qt_libdir}/libQt%{api}MultimediaQuick_p.prl %{buildroot}%{_qt_libdir}/pkgconfig/Qt%{api}MultimediaQuick_p.pc
# qtconfig doesn't exist anymore - we don't need its translations
rm -f %{buildroot}%{_qt_translationsdir}/qtconfig_*.qm
# Let's make life easier for packagers
mkdir -p %{buildroot}%{_bindir}
for i in qmake moc uic rcc tracegen qdbuscpp2xml qdbusxml2cpp; do
    ln -s ../%{_lib}/qt%{api}/bin/$i %{buildroot}%{_bindir}/$i-qt%{api}
    ln -s ../%{_lib}/qt%{api}/bin/$i %{buildroot}%{_bindir}/$i
done
for i in fixqt4headers.pl qlalr; do
    ln -s ../%{_lib}/qt%{api}/bin/$i %{buildroot}%{_bindir}/$i
done

%if "%{_qt_libdir}" != "%{_libdir}"
pushd %{buildroot}%{_libdir}
ln -s ../%{_lib}/qt%{api}/%{_lib}/*.so.* .
mkdir pkgconfig
cd pkgconfig
ln -s ../../%{_lib}/qt%{api}/%{_lib}/pkgconfig/*.pc .
popd
%endif

if [ -e %{buildroot}%{_libdir}/pkgconfig/Qt5LinuxAccessibilitySupport.pc ]; then
	echo "Qt5LinuxAccessibilitySupport.pc has been added upstream, remove the workaround"
	exit 1
else
	# This is used by Qt5Wayland -- but never actually created
	# See also https://bugreports.qt.io/browse/QTBUG-76042
	cat >%{buildroot}%{_libdir}/pkgconfig/Qt5LinuxAccessibilitySupport.pc <<EOF
prefix=%{_qt_prefix}
exec_prefix=\${prefix}
libdir=%{_libdir}
includedir=%{_includedir}/qt5
Name: Qt%{api} Linux Accessibility Support
Description: Qt%{api} Linux Accessibility Support
Version: %{version}
Libs: -lQt%{api}AccessibilitySupport
Cflags: -I\${includedir}/QtAccessibilitySupport -I\${includedir}
Requires: Qt%{api}Core
EOF
fi


# Fix some wrong permissions
find %{buildroot} -type f -perm -0755 -name "*.png" |xargs --no-run-if-empty chmod 0644
find %{buildroot} -type f -perm -0755 -name "*.svg" |xargs --no-run-if-empty chmod 0644
find %{buildroot} -type f -perm -0755 -name "*.jpg" |xargs --no-run-if-empty chmod 0644
find %{buildroot} -type f -perm -0755 -name "*.xml" |xargs --no-run-if-empty chmod 0644
find %{buildroot} -type f -perm -0755 -name "*.xsl" |xargs --no-run-if-empty chmod 0644
find %{buildroot} -type f -perm -0755 -name "*.php" |xargs --no-run-if-empty chmod 0644
find %{buildroot} -type f -perm -0755 -name "*.html" |xargs --no-run-if-empty chmod 0644
find %{buildroot} -type f -perm -0755 -name "*.js" |xargs --no-run-if-empty chmod 0644
find %{buildroot} -type f -perm -0755 -name "*.plist.app" |xargs --no-run-if-empty chmod 0644

# "make dep" output packaged into examples is bogus...
find %{buildroot} -name .deps |xargs rm -rf

# Workaround for
# *** ERROR: same build ID in nonidentical files!
#        /usr/lib/qt5/bin/qdbuscpp2xml
#   and  /usr/lib/qt5/bin/moc
# ...
# while generating debug info
find %{buildroot} -type f -perm -0755 |grep -vE '\.(so|qml|sh|pl|ttf|eot|woff|py)' |xargs %__strip --strip-unneeded

# Install rpm macros
mkdir -p %{buildroot}%{_sysconfdir}/rpm/macros.d
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/rpm/macros.d

# Tell qtchooser about us
mkdir -p %{buildroot}%{_sysconfdir}/xdg/qtchooser
cat >%{buildroot}%{_sysconfdir}/xdg/qtchooser/%{name}.conf <<'EOF'
%{_qt_bindir}
%{_qt_libdir}
EOF

# QMAKE_PRL_BUILD_DIR = /builddir/build/BUILD/qt-everywhere-everywhere-src-5.4.0-beta/qtwayland/src/client
## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

install -p -m755 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/X11/xsetup.d/10-qt5-check-opengl.xsetup
install -m644 -p -D %{SOURCE3} %{buildroot}%{_qt_datadir}/qtlogging.ini
