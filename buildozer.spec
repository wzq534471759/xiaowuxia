[app]
# (str) Title of your application
title = 小武侠传说

# (str) Package name
package.name = xiawuxia

# (str) Package domain (needed for android/ios packaging)
package.domain = com.wuxia

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,json

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,images/*

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = tests, bin

# (list) List of exclusions using pattern matching
source.exclude_patterns = .git,*.pyc

# (str) Application versioning (method 1)
version = 1.0

# (str) Application versioning (method 2)
version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.3.1

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = landscape

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#

#
# author = © Copyright Info

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
android.presplash_color = #0a0a18

# (list) Permissions
android.permissions = VIBRATE,WAKE_LOCK

# (int) Target Android API, should be as high as possible.
android.api = 34

# (int) Minimum API your APK will support.
android.minapi = 23

# (int) Android SDK version to use
android.sdk = 34

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
android.ndk_api = 23

# (bool) Android x86 support
android.archs = arm64-v8a, armeabi-v7a

# (bool) usesCleartextTraffic 
android.uses_cleartext_traffic = False

# (bool) If True, then SKIP building the APK
# android.skip_build = False

# (bool) If True, then automatically accept SDK license
# agreements.
# android.accept_sdk_license = False

# (str) App name
android.app_name = 小武侠传说

# (str) App version
android.app_version = 1.0

# (str) App version code
android.app_version_code = 1

# (str) App package name
android.package = com.wuxia.xiawuxia

# (str) Storage access
android.storage_access_framework = True

# (bool) Enable AndroidX
android.enable_androidx = True

# (bool) Enable Jetifier
android.enable_jetifier = True

# (str) Path to keystore for signing release APK
# android.release_keystore = path/to/keystore

# (str) Keystore password
# android.release_keystore_password = your_password

# (str) Alias of the key in the keystore
# android.release_key_alias = your_alias

#
# Python for android (p4a) specific
#

# (str) python-for-android branch to use, defaults to master
p4a.branch = master

# (str) OUYA Console Category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
android.ouya.category = GAME

# (str) Filename of OUYA Console icon (at least 732x412)
# ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
# android.activity_intent_filters = path/to/filters.xml

# (str) launchMode to set for the main activity
# android.launch_mode = standard

# (list) Android additional libraries to copy into libs/armeabi
#android.add_libs_armeabi = libs/android/*.so
#android.add_libs_armeabi_v7a = libs/android-v7/*.so
#android.add_libs_x86 = libs/android-x86/*.so
#android.add_libs_mips = libs/android-mips/*.so

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
android.wakelock = True

# (list) Android application meta-data to set (key=value format)
#android.meta_data =

# (list) Android library project to add (will be added in the
# project.properties automatically.)
#android.library_references =

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a symlink
#android.copy_libs = True

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = arm64-v8a

# (int) overrides for the memory limit of the build process (in MB)
android.build_memory = 4096

# (str) Path to the python-for-android distribution directory
# p4a.distribution_dir = path/to/dist

# (str) Python version to use
# python_version = 3.10

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 1

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to configuration storage, absolute or relative to spec file
# config_dir = ./.buildozer

# (list) App dependencies
# app_deps =

# (str) Use this to specify a custom Python version
# custom_python = /path/to/python

# (bool) If True, use the experimental --use-setup-py feature
# use_setup_py = False

# (str) Custom URL for the Python for Android distribution
# p4a_url =

# (str) Custom branch for the Python for Android distribution
# p4a_branch =

# (str) Custom commit for the Python for Android distribution
# p4a_commit =

# (str) Custom repository for the Python for Android distribution
# p4a_repository =
