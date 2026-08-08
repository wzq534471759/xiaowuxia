#!/bin/bash
# Build APK for 小武侠传说
set -e

cd /data/workspace/xiawuxia_kivy

export ANDROID_HOME=/opt/android-sdk
export ANDROID_SDK_ROOT=/opt/android-sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$ANDROID_HOME/ndk/25.2.9519653

echo "=== Checking environment ==="
java -version 2>&1
echo "---"
which buildozer
echo "---"
echo "ANDROID_HOME=$ANDROID_HOME"
ls $ANDROID_HOME/ndk/ 2>/dev/null || echo "NDK not found"

echo ""
echo "=== Starting APK build ==="
buildozer android debug 2>&1

echo ""
echo "=== Build complete ==="
ls -la bin/ 2>/dev/null || echo "No bin/ directory"
find . -name "*.apk" 2>/dev/null
