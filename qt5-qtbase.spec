# cb 05/01/2016
# because the docdir is under /usr/share/doc
# all files there get marked as doc so that when they are installed
# on abf using --excludedocs option they are missing, causing qt5-qtdoc to fail
# this makes sure the files dont get marked as docs
%define _no_default_doc_files 1

# WARNING
# Don't ever add -Ofast to compiler flags. It breaks
# QVariant in subtle ways (causing non-POD types to
# easily convert to the number 0, breaking among other
# things display of HTML messages in kmail and the
# UI of plasma-systemmonitor [we have a workaround
# for this in plasma-systemmonitor, so double-check
# without that patch]).
# Also, if we ever switch back to ld.gold as default
# linker, we need to add -fuse-ld=bfd or -fuse-ld=lld
# on aarch64 as workaround for a weird signal/slot problem
# (slots defined as lambdas never called)
%global optflags %{optflags} -O3

#% define debug_package %{nil}
%define beta %{nil}
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

# OpenGL ES is less cluttered and there's a couple of
# chipsets (esp. in ARM SOCs) that do only ES.
# ES is also closer to WebGL - which should be a nice
# performance boost there.
# However, as of Mesa 20.2, Qt 5.15.1, gltype es2 seems
# to break:
# - plasmashell when using the nouveau driver
# - Launching obs-studio
# - VirtualBox
# Until those are fixed, let's stick with OpenGL
# Desktop on x86 and use ES on platforms that may
# not have anything else.
%ifarch %{arm} %{aarch64}
%define gltype es2
%else
%define gltype desktop
%endif

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

%bcond_with bootstrap

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
Version:	5.15.3
%if "%{beta}" != ""
%define qttarballdir qtbase-everywhere-src-%{version}-%{beta}
Source0:	http://download.qt.io/development_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}-%{beta}/submodules/%{qttarballdir}.tar.xz
Release:	0.%{beta}.1
%else
# Since Qt has stopped making 5.15 releases (but the tags keep
# rolling in through kde's qt branch), we have to hardcode 5.15.2
# (last release) here, even if %{version} keeps rising
%define qttarballdir qtbase-everywhere-src-5.15.2
Source0:	http://download.qt.io/official_releases/qt/5.15/5.15.2/submodules/%{qttarballdir}.tar.xz
Release:	6
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
Patch1:		https://src.fedoraproject.org/rpms/qt5-qtbase/raw/rawhide/f/qt5-qtbase-gcc11.patch
# Fix XDG_RUNTIME_DIR for setuid applications
# https://issues.openmandriva.org/show_bug.cgi?id=1641
#Patch2:		qt-5.7.0-setuid-XDG_RUNTIME_DIR.patch
# https://codereview.qt-project.org/#/c/151459/
Patch3:		qt-5.5.1-barf-on-clang-PIE.patch
Patch4:		qt-5.8.0-no-isystem-usr-include.patch
Patch5:		qtbase-5.14.1-clang10.patch
Patch6:		qtbase-5.15-qsqlite-blocking-changes-from-akonadi.patch

### Fedora patches
Patch102:	qtbase-everywhere-src-5.6.0-moc_WORDSIZE.patch
### END OF FEDORA PATCHES
# (tpg) https://bugreports.qt.io/browse/QTBUG-88491
Patch103:	0001-Avoid-SIGABRT-on-platform-plugin-initialization-fail.patch

# From KDE https://invent.kde.org/qt/qt/qtbase
Patch1000:	0001-toolchain.prf-Use-vswhere-to-obtain-VS-installation-.patch
Patch1001:	0002-Fix-allocated-memory-of-QByteArray-returned-by-QIODe.patch
Patch1003:	0004-QLayout-docs-explain-better-what-the-QWidget-ctor-ar.patch
Patch1004:	0005-QMacStyle-fix-tab-rendering.patch
Patch1005:	0006-QMacStyle-more-pixel-refinements.patch
Patch1009:	0010-QAbstractItemModelTester-don-t-rely-on-hasChildren.patch
Patch1010:	0011-Doc-Remove-mentioning-of-old-macos-versions-from-QSe.patch
Patch1011:	0012-Pass-SameSite-through-QNetworkCookie.patch
Patch1012:	0013-doc-fix-typo-consise-concise.patch
Patch1013:	0014-Selftest-copy-XAUTHORITY-environment-variable.patch
Patch1014:	0015-Fix-delay-first-time-a-font-is-used.patch
Patch1016:	0017-Android-Request-cursor-to-be-in-proper-position.patch
Patch1017:	0018-testlib-Let-logger-report-whether-it-is-logging-to-s.patch
Patch1020:	0021-Use-void-instead-of-Q_UNUSED.patch
Patch1021:	0022-Don-t-show-QPushButton-as-hovered-unless-the-mouse-i.patch
Patch1022:	0023-MinGW-Fix-assert-in-QCoreApplication-arguments-when-.patch
Patch1023:	0024-QCombobox-propagate-the-palette-to-the-embedded-line.patch
Patch1024:	0025-QMarginsF-document-that-isNull-operator-operator-are.patch
Patch1025:	0026-qmake-vcxproj-Fix-handling-of-extra-compiler-outputs.patch
Patch1026:	0027-Android-fix-documentation-about-ANDROID_EXTRA_LIBS.patch
Patch1027:	0028-Offscreen-QPA-implement-a-native-interface.patch
Patch1028:	0029-DropSite-example-support-markdown.patch
Patch1029:	0030-Do-not-define-dynamic_cast.patch
Patch1030:	0031-Android-fix-crash-by-passing-the-right-Handle-to-dls.patch
Patch1031:	0032-testlib-Add-private-API-to-add-test-logger.patch
Patch1032:	0033-Update-third-party-md4c-to-version-0.4.6.patch
Patch1033:	0034-moc-Handle-include-in-enum-take-2.patch
Patch1034:	0035-InputMethod-should-call-reset-function-when-proxywid.patch
Patch1035:	0036-Add-possibility-to-set-QNX-Screen-pipeline-value.patch
Patch1036:	0037-qglobal-Only-define-QT_ENSURE_STACK_ALIGNED_FOR_SSE-.patch
Patch1037:	0038-macOS-FreeType-fix-crash-with-non-printable-unicode.patch
Patch1038:	0039-Linux-fix-crash-in-AtSpi-adaptor-when-handling-windo.patch
Patch1039:	0040-Add-_MSC_VER-check-to-MSVC-ARM-compiler-workaround.patch
Patch1040:	0041-QMap-suppress-warning-about-strict-aliasing-violatio.patch
Source1042:	0043-Set-the-url-to-have-the-AtNx-filename-if-one-is-foun.patch
Patch1043:	0044-QMap-don-t-tell-everyone-QMapNode-has-no-friends.patch
Patch1044:	0045-QNAM-Work-around-QObject-finicky-orphan-cleanup-deta.patch
Patch1045:	0046-xcb-ensure-that-available-glx-version-is-greater-tha.patch
Patch1046:	0047-Protect-QImage-colorspace-transform-on-shutdown.patch
Patch1047:	0048-Fix-qstylesheetstyle-clip-border-error.patch
Patch1048:	0049-Correct-processEvents-documentation.patch
Patch1049:	0050-Update-CLDR-to-v38.patch
Patch1051:	0052-Reduce-memory-reallocations-in-QTextTablePrivate-upd.patch
Patch1052:	0053-Fix-regular-expression-initialize-with-incorrect-fil.patch
Patch1053:	0054-Cocoa-Allow-CMD-H-to-hide-the-application-when-a-too.patch
Patch1054:	0055-Fix-pcre2-feature-conditions.patch
Patch1055:	0056-Q_PRIMITIVE_TYPE-improve-the-documentation.patch
Patch1056:	0057-QAsn1Element-Read-value-in-blocks-to-avoid-oom-at-wr.patch
Patch1057:	0058-Android-Don-t-use-putIfAbsent-as-that-is-not-availab.patch
Patch1058:	0059-QMutex-order-reads-from-QMutexPrivate-waiters-and-QB.patch
Patch1059:	0060-Android-Add-the-QtAndroidBearer.jar-to-the-jar-depen.patch
Patch1060:	0061-Android-Add-the-required-linker-flags-for-unwinding-.patch
Patch1061:	0062-Android-recommend-against-using-ANDROID_ABIS-inside-.patch
Patch1062:	0063-Android-fix-android-java-and-templates-targets-with-.patch
Patch1063:	0064-QCharRef-properly-disable-assignment-from-char.patch
Patch1064:	0065-Android-Treat-ACTION_CANCEL-as-TouchPointReleased.patch
Patch1065:	0066-Fix-misidentification-of-some-shearing-QTransforms-a.patch
Patch1066:	0067-Fix-QGraphicsItem-crash-if-click-right-button-of-mou.patch
Patch1067:	0068-Bump-version.patch
Patch1068:	0069-Android-Ensure-windows-always-have-a-geometry-on-cre.patch
Patch1069:	0070-macOS-Account-for-Big-Sur-always-enabling-layer-back.patch
Patch1070:	0071-Fix-shaping-problems-on-iOS-14-macOS-11.patch
Patch1071:	0072-Link-to-qAlpha-in-qRgb-and-qRgba-docs.patch
Patch1072:	0073-HTTP2-fix-crash-from-assertion.patch
Patch1073:	0074-Fuzzing-Add-a-test-for-QDateTime-fromString.patch
Patch1074:	0075-QSocks5SocketEngine-Fix-out-of-bounds-access-of-QBA.patch
Patch1075:	0076-Use-QTRY_COMPARE-in-an-attempt-to-make-the-test-less.patch
Patch1076:	0077-Doc-Document-QGradient-Preset-enum-values.patch
Patch1077:	0078-Doc-Fix-documentation-warnings-for-Qt-XML.patch
Patch1078:	0079-Doc-Fix-documentation-warnings-in-Qt-Network.patch
Patch1079:	0080-Ensure-that-QMenu-is-polished-before-setting-the-scr.patch
Patch1080:	0081-widgets-Don-t-report-new-focus-object-during-clearFo.patch
Patch1081:	0082-QDtls-remove-redundant-RAII-struct.patch
Patch1082:	0083-macOS-Propagate-device-pixel-ratio-of-system-tray-ic.patch
Patch1083:	0084-tst_qocsp-improve-code-coverage.patch
Patch1084:	0085-Doc-explain-how-to-create-a-test-touch-device-for-us.patch
Patch1085:	0086-macOS-Upgrade-supported-SDK-to-11.0.patch
Patch1086:	0087-Fix-logic-error-in-QString-replace-ch-after-cs.patch
Patch1087:	0088-Be-more-consistent-when-converting-JSON-values-from-.patch
Patch1088:	0089-QCoreApplication-add-more-information-to-processEven.patch
Patch1089:	0090-Fix-QSFPM-not-emitting-dataChanged-when-source-model.patch
Patch1090:	0091-Android-Fix-android-accessibility-not-being-set-acti.patch
Patch1091:	0092-Fix-x-height-name-in-stylesheet-docs.patch
Patch1092:	0093-QMutex-Work-around-ICC-bug-in-dealing-with-constexpr.patch
Patch1093:	0094-wasm-fix-resizing-of-qwidget-windows.patch
Patch1094:	0095-Avoid-integer-overflow-and-division-by-zero.patch
Patch1095:	0096-QPasswordDigestor-improve-code-coverage.patch
Patch1096:	0097-QStackedLayout-fix-a-memory-leak.patch
Patch1097:	0098-Limit-value-in-setFontWeightFromValue.patch
Patch1098:	0099-Doc-Fix-documentation-of-qmake-s-exists-function.patch
Patch1099:	0100-QVLA-do-not-include-QtTest.patch
Patch1100:	0101-Clean-up-docs-of-QCalendar-related-QLocale-toString-.patch
Patch1101:	0102-Change-android-target-SDK-version-to-29.patch
Patch1102:	0103-QVLA-always-use-new-to-create-new-objects.patch
Patch1103:	0104-QPushButton-fix-support-of-style-sheet-rule-for-text.patch
Patch1104:	0105-Limit-pen-width-to-maximal-32767.patch
Patch1105:	0106-Doc-Consistently-use-book-style-capitalization-for-Q.patch
Patch1106:	0107-qstring.h-fix-warnings-about-shortening-qsizetype-to.patch
Patch1107:	0108-Fix-invalid-QSortFilterProxyModel-dataChanged-parame.patch
Patch1108:	0109-Minor-refactor-of-installMetaFile.patch
Patch1109:	0110-Return-a-more-useful-date-time-on-parser-failure-in-.patch
Patch1110:	0111-QCalendar-increase-coverage-by-tests.patch
Patch1111:	0112-Bounds-check-time-zone-offsets-when-parsing.patch
Patch1112:	0113-Network-self-test-make-it-work-with-docker-container.patch
Patch1113:	0114-QSslConfiguration-improve-code-coverage.patch
Patch1114:	0115-Add-new-way-to-mess-up-projects-with-QMAKE_INSTALL_R.patch
Patch1115:	0116-Install-3rd-party-headers-and-meta-for-static-builds.patch
Patch1116:	0117-Create-qtlibjpeg-for-jpeg-image-plugin.patch
Patch1117:	0118-QStandardPaths-Don-t-change-permissions-of-XDG_RUNTI.patch
Patch1118:	0119-tst_QSslCertificate-improve-code-coverage.patch
Patch1119:	0120-Let-QXcbConnection-getTimestamp-properly-exit-when-X.patch
Patch1120:	0121-QDtls-cookie-verifier-make-sure-a-server-can-re-use-.patch
Patch1121:	0122-QMacStyle-remove-vertical-adjustment-for-inactive-ta.patch
Patch1122:	0123-Revert-xcb-add-xcb-util-dependency-for-xcb-image.patch
Patch1123:	0124-Containers-call-constructors-even-for-primitive-type.patch
Patch1124:	0125-Android-print-tailored-warning-if-qml-dependency-pat.patch
Patch1125:	0126-Cosmetic-stroker-avoid-overflows-for-non-finite-coor.patch
Patch1126:	0127-QSslCipher-improve-its-code-coverage-and-auto-tests.patch
Patch1127:	0128-tst_qsslkey-handle-QT_NO_SSL-properly.patch
Patch1128:	0129-Add-the-Qt-6.0-deprecation-macros.patch
Patch1129:	0130-wasm-fix-mouse-double-click.patch
Patch1130:	0131-Android-avoid-reflection-with-ClipData-addItem.patch
Patch1131:	0132-QHeaderView-fix-spurious-sorting.patch
Patch1132:	0133-Fix-exception-with-Android-5.x.patch
Patch1133:	0134-Http2-Remove-errored-out-requests-from-queue.patch
Patch1134:	0135-Http2-don-t-call-ensureConnection-when-there-s-no-re.patch
Patch1135:	0136-Fix-QTranslator-load-search-order-not-following-uiLa.patch
Patch1136:	0137-Avoid-signed-overflow-in-moc.patch
Patch1137:	0138-Android-Kill-calls-to-deprecated-func-in-API-29.patch
Patch1138:	0139-Doc-Improve-_CAST_FROM_ASCII-documentation.patch
Patch1139:	0140-Improve-documented-function-argument-names.patch
Patch1140:	0141-Fix-QImage-setPixelColor-on-RGBA64_Premultiplied.patch
Patch1141:	0142-macOS-Make-sure-that-the-reserved-characters-are-not.patch
Patch1142:	0143-Enable-testing-for-whether-a-calendar-registered-its.patch
Patch1143:	0144-tests-add-a-shortcut-to-quit-app-in-allcursors.patch
Patch1144:	0145-QSslSocket-Don-t-call-transmit-in-unencrypted-mode.patch
Patch1145:	0146-QStringView-operator-operator-operator-currently-Qt6.patch
Patch1146:	0147-QCborStreamReader-move-the-readStringChunk-code-to-t.patch
Patch1147:	0148-Improve-the-documentation-for-QElapsedTimer-restart-.patch
Patch1148:	0149-QSslSocket-verify-do-not-alter-the-default-configura.patch
Patch1149:	0150-Fix-tst_QFontDatabase-aliases-failure-with-ambiguous.patch
Patch1150:	0151-QStyleAnimation-make-sure-the-last-frame-of-animatio.patch
Patch1151:	0152-PCRE-update-to-10.36.patch
Patch1152:	0153-tst_QCborValue-adjust-the-size-of-the-minimum-string.patch
Patch1153:	0154-macOS-Always-allow-interacting-with-popup-windows-du.patch
Patch1154:	0155-macOS-Add-missing-QT_MANGLE_NAMESPACE.patch
Patch1155:	0156-QSplashScreen-draw-pixmap-with-SmoothTransfrom.patch
Patch1156:	0157-Android-Qml-accessibility-fixes.patch
Patch1157:	0158-Http2-set-the-reply-s-error-code-and-string-on-error.patch
Patch1158:	0159-Try-again-to-fix-Clang-s-Wconstant-logical-operand-w.patch
Patch1159:	0160-Revert-Android-print-tailored-warning-if-qml-depende.patch
Patch1160:	0161-QUrl-fix-parsing-of-empty-IPv6-addresses.patch
Patch1161:	0162-tst_QSslError-improve-the-code-coverage-as-pointed-a.patch
Patch1162:	0163-macOS-Disable-WA_QuitOnClose-on-menu-item-widget-con.patch
Patch1163:	0164-QString-fix-count-QRegularExpression.patch
Patch1164:	0165-QString-lastIndexOf-fix-off-by-one-for-zero-length-m.patch
Patch1165:	0166-secureudpclient-a-speculative-fix-for-non-reproducib.patch
Patch1166:	0167-Android-don-t-use-avx-and-avx2-when-building-for-And.patch
Patch1167:	0168-Fuzzing-Provide-link-to-oss-fuzz.patch
Patch1168:	0169-Blacklist-tst_QMdiArea-updateScrollBars-on-macos.patch
Patch1169:	0170-Fix-build-with-GCC-11-include-limits.patch
Patch1170:	0171-Build-fixes-for-GCC-11.patch
Patch1171:	0172-Partially-revert-813a928c7c3cf98670b6043149880ed5c95.patch
Patch1172:	0173-Fix-removing-columns-when-QSortFilterProxyModel-has-.patch
Patch1173:	0174-Fix-get-out-of-bounds-index-in-QSortFilterProxyModel.patch
Patch1174:	0175-Fix-handling-of-surrogates-in-QBidiAlgorithm.patch
Patch1175:	0176-Avoid-undefined-color-values-in-corrupt-xpm-image.patch
Patch1176:	0177-Gracefully-reject-requests-for-absurd-font-sizes.patch
Patch1177:	0178-Don-t-own-unique-name-for-QDBusTrayIcon.patch
Patch1178:	0179-QAbstractItemModelTester-fix-false-positive-when-mod.patch
Patch1179:	0180-Fix-QAbstractItemModelTester-false-positive.patch
Patch1180:	0181-Deprecate-QMutex-in-recursive-mode.patch
Patch1181:	0182-Fix-QAbstractItemModelTester-false-positive.patch
Patch1182:	0183-Fix-crash-on-serializing-default-constructed-QTimeZo.patch
Patch1183:	0184-Fix-QTreeModel-calling-beginRemoveRows-twice.patch
Patch1184:	0185-QConcatenateTablesProxyModel-skip-dataChanged-in-hid.patch
Patch1185:	0186-QComboBox-fix-select-all-columns-in-the-view.patch
Patch1186:	0187-QTableView-honor-spans-when-calculating-height-width.patch
Patch1187:	0188-TableView-Trigger-the-resizing-of-editors-resizing-a.patch
Patch1188:	0189-Fix-no-mapping-for-SysReq-key.patch
Patch1189:	0190-qdbus-add-support-for-aay-QByteArrayList.patch
Patch1190:	0191-QRandom-drop-a-usage-of-std-is_literal_type.patch
Patch1191:	0192-fix-Optimize-the-performance-of-the-inotify-file-sys.patch
Patch1192:	0193-Remove-the-unnecessary-template-parameter-from-the-c.patch
Patch1193:	0194-Fix-memory-leak-when-using-small-caps-font.patch
Patch1194:	0195-Make-sure-_q_printerChanged-is-called-even-if-only-p.patch
Patch1195:	0196-fix-Alt-shortcut-on-non-US-layouts.patch
Patch1196:	0197-Fix-copy-and-paste-bug-in-QDTEP-getMaximum.patch
Patch1197:	0198-QSortFilterProxyModel-create-mappings-on-demand-agai.patch
Patch1198:	0199-xcb-fix-thread-synchronization-in-QXcbEventQueue-wai.patch
Patch1199:	0200-Optimize-quadratic-time-insertion-in-QSortFilterProx.patch

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
# Binary patch
BuildRequires:	git-core
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
BuildRequires:	pkgconfig(dri)
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
BuildRequires:	pkgconfig(xcb-util)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(xcb-render)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xcb-xinerama)
BuildRequires:	pkgconfig(xcb-xinput)
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
BuildRequires:	pkgconfig(mit-krb5-gssapi)
BuildConflicts:	heimdal-devel
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
%if  "%{gltype}" == "desktop"
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
%endif

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

# Patch includes a git binary diff
git init
git config user.name "OpenMandriva Builder"
git config user.email "info@openmandriva.org"
git apply %{S:1042}

# needed after applying patch that bumps the version number
bin/syncqt.pl -version %{version}

# respect cflags
sed -i -e '/^CPPFLAGS\s*=/ s/-g //' qmake/Makefile.unix
sed -i -e "s|^\(QMAKE_LFLAGS_RELEASE.*\)|\1 %{build_ldflags}|" mkspecs/common/g++-unix.conf
#OPTFLAGS="%{optflags} -fno-semantic-interposition -fPIC"
OPTFLAGS="%{optflags}"
%ifarch %{arm}
OPTFLAGS="$(echo ${OPTFLAGS} |sed -e 's,-mfpu=neon ,-mfpu=neon-vfpv4 ,g;s,-mfpu=neon$,-mfpu=neon-vfpv4,')"
%endif
sed -i -e "s|-O2|${OPTFLAGS}|g" mkspecs/common/gcc-base.conf
sed -i -e "s|-O3|${OPTFLAGS}|g" mkspecs/common/gcc-base.conf
%if !%{without clang}
sed -i -e "s|gcc-nm|llvm-nm|g" mkspecs/common/clang.conf
# drop flags that clang doesn't recognize
sed -i -e "s|-fvar-tracking-assignments||g" mkspecs/common/gcc-base.conf
sed -i -e "s|-frecord-gcc-switches||g" mkspecs/common/gcc-base.conf
sed -i -e "s|-Wp,-D_FORTIFY_SOURCE=2||g" mkspecs/common/gcc-base.conf
# full LTO takes a long time to compile, but can potentially
# optimize a bit better than thinlto
sed -i -e "s,-flto=thin,-flto,g" mkspecs/common/clang.conf

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
cd src/3rdparty
mkdir UNUSED
# FIXME
mv freetype libjpeg libpng zlib xcb sqlite UNUSED/
cd -

# FIXME this is still a valid bug, but it only occurs with the
# combination of clang, LTO and -fuse-ld=gold.
# Since we default to lld these days, the workaround is no
# longer needed.
%if 0
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
%set_build_flags

# As of Qt 5.12.0, clang 7.0.1 (and gcc 8.2.0),
# -reduce-relocations breaks the signal/slot system badly.
# Immediately obvious effect: sddm crashes
# Probably related to
# https://bugreports.qt.io/browse/QTBUG-52439
# (tpg) 2020-05-28 according to this bugs, it's clang issue
# https://bugreports.qt.io/browse/QTBUG-43556
# https://bugreports.qt.io/browse/QTBUG-61710
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
	-zstd \
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
	-opengl %{gltype} -egl -eglfs -gbm -kms \
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
	-qpa "xcb;wayland" \
	-xcb-xlib \
	-no-bundled-xcb-xinput \
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
