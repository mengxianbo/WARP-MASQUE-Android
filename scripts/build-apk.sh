#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UPSTREAM="$ROOT/upstream/usque-android"
ANDROID_PROJECT="$UPSTREAM/android/usque-vpn"

if [[ ! -f "$UPSTREAM/go.mod" ]]; then
  git -C "$ROOT" submodule update --init --recursive
fi

: "${ANDROID_HOME:=${ANDROID_SDK_ROOT:-$HOME/Android/Sdk}}"
export ANDROID_HOME
export ANDROID_SDK_ROOT="$ANDROID_HOME"
if [[ -z "${ANDROID_NDK_HOME:-}" && -d "$ANDROID_HOME/ndk/26.3.11579264" ]]; then
  export ANDROID_NDK_HOME="$ANDROID_HOME/ndk/26.3.11579264"
fi

cd "$UPSTREAM/android"
make init
make android
mkdir -p "$ANDROID_PROJECT/app/libs"
cp usque.aar "$ANDROID_PROJECT/app/libs/usque.aar"

sed -i 's/minSdk = 24/minSdk = 26/' "$ANDROID_PROJECT/app/build.gradle.kts"
cd "$ANDROID_PROJECT"
./gradlew --no-daemon clean assembleDebug

APK="$ANDROID_PROJECT/app/build/outputs/apk/debug/app-debug.apk"
test -s "$APK"
mkdir -p "$ROOT/dist"
cp "$APK" "$ROOT/dist/WARP-MASQUE-Android-debug.apk"
unzip -l "$APK" | grep -q 'lib/arm64-v8a/'
unzip -l "$APK" | grep -q 'lib/armeabi-v7a/'
sha256sum "$ROOT/dist/WARP-MASQUE-Android-debug.apk" > "$ROOT/dist/SHA256SUMS.txt"
echo "APK: $ROOT/dist/WARP-MASQUE-Android-debug.apk"
