#!/bin/bash
# Install Android SDK + NDK for Buildozer
set -e

export ANDROID_HOME=/opt/android-sdk
export ANDROID_SDK_ROOT=/opt/android-sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools

echo "=== Installing Android SDK ==="
mkdir -p $ANDROID_HOME/cmdline-tools
cd /tmp

# Download command-line tools
wget -q https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip -O cmdtools.zip
unzip -q cmdtools.zip -d $ANDROID_HOME/cmdline-tools/
mv $ANDROID_HOME/cmdline-tools/cmdline-tools $ANDROID_HOME/cmdline-tools/latest
rm cmdtools.zip

# Accept licenses and install SDK packages
yes | sdkmanager --licenses > /dev/null 2>&1
sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0" > /dev/null 2>&1

# Install NDK
sdkmanager "ndk;25.2.9519653" > /dev/null 2>&1

echo "=== SDK Installation Complete ==="
echo "ANDROID_HOME=$ANDROID_HOME"
ls $ANDROID_HOME/ndk/
