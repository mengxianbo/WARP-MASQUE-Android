#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UPSTREAM="$ROOT/upstream/usque-android"
ANDROID_DIR="$UPSTREAM/android"
APP="$ANDROID_DIR/usque-vpn/app"
BIND_DIR="$ANDROID_DIR/hidewifi-bind"
AAR="$ANDROID_DIR/usque.aar"

: "${ANDROID_HOME:=${ANDROID_SDK_ROOT:-$HOME/Android/Sdk}}"
export ANDROID_HOME ANDROID_SDK_ROOT="$ANDROID_HOME"
: "${ANDROID_NDK_HOME:=$ANDROID_HOME/ndk/26.3.11579264}"
export ANDROID_NDK_HOME

# Both upstream engines are Go/gomobile libraries. Binding them in one gomobile
# invocation is essential: two independently-built AARs each package go.Seq,
# go.Universe and libgojni.so, which collide at DEX/native packaging time.
GOMOBILE_VERSION="v0.1.12"
GOBIN="$(go env GOPATH)/bin"
export GOBIN
go install "github.com/sagernet/gomobile/cmd/gomobile@$GOMOBILE_VERSION"
go install "github.com/sagernet/gomobile/cmd/gobind@$GOMOBILE_VERSION"
"$GOBIN/gomobile" init -v

mkdir -p "$BIND_DIR" "$APP/libs"
cat > "$BIND_DIR/go.mod" <<'EOF'
module github.com/mengxianbo/hidewifi-android-bind

go 1.26.3

require (
    github.com/Diniboy1123/usque v0.0.0
    github.com/sagernet/sing-box v1.14.4
)

replace github.com/Diniboy1123/usque => ../..
EOF

cd "$BIND_DIR"
go mod download
"$GOBIN/gomobile" bind -v \
  -target=android/arm64,android/arm \
  -androidapi 26 \
  -ldflags="-s -w" \
  -o "$AAR" \
  github.com/Diniboy1123/usque/android \
  github.com/sagernet/sing-box/experimental/libbox

test -s "$AAR"
cp "$AAR" "$APP/libs/usque.aar"
echo "Built one combined AAR containing usque + sing-box with a single gomobile runtime:"
ls -lh "$AAR"
