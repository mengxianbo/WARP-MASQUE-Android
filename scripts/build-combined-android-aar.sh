#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UPSTREAM="$ROOT/upstream/usque-android"
ANDROID_DIR="$UPSTREAM/android"
APP="$ANDROID_DIR/usque-vpn/app"
BUILD_ROOT="$ANDROID_DIR/hidewifi-bind"
SINGBOX_DIR="$BUILD_ROOT/sing-box"
AAR="$ANDROID_DIR/usque.aar"

: "${ANDROID_HOME:=${ANDROID_SDK_ROOT:-$HOME/Android/Sdk}}"
export ANDROID_HOME ANDROID_SDK_ROOT="$ANDROID_HOME"
: "${ANDROID_NDK_HOME:=$ANDROID_HOME/ndk/28.0.13004108}"
export ANDROID_NDK_HOME

# Use the exact gomobile version pinned by sing-box v1.14.4.
GOMOBILE_VERSION="v0.1.12"
GOBIN="$(go env GOPATH)/bin"
export GOBIN
go install "github.com/sagernet/gomobile/cmd/gomobile@$GOMOBILE_VERSION"
go install "github.com/sagernet/gomobile/cmd/gobind@$GOMOBILE_VERSION"
"$GOBIN/gomobile" init -v

mkdir -p "$BUILD_ROOT" "$APP/libs"
# Build from sing-box's own module root, not from a synthetic wrapper module.
# Go ignores replace directives in dependency go.mod files; using sing-box as
# the main module preserves its pinned fork replacements and build constraints.
if [[ ! -f "$SINGBOX_DIR/go.mod" ]]; then
  module_json="$(go mod download -json github.com/sagernet/sing-box@v1.14.4)"
  module_dir="$(python3 -c 'import json,sys; print(json.load(sys.stdin)["Dir"])' <<< "$module_json")"
  cp -a "$module_dir" "$SINGBOX_DIR"
fi

cd "$SINGBOX_DIR"
go mod edit -require=github.com/Diniboy1123/usque@v0.0.0
go mod edit -replace="github.com/Diniboy1123/usque=$UPSTREAM"
go mod download

# Official sing-box Android build tags and linker flags (v1.14.4).
# Both exported packages are bound in one invocation and one Go runtime.
"$GOBIN/gomobile" bind -v \
  -target=android/arm64,android/arm \
  -androidapi 26 \
  -javapkg=io.nekohasekai \
  -libname=box \
  -trimpath \
  -buildvcs=false \
  -tags=with_gvisor,with_quic,with_wireguard,with_utls,with_naive_outbound,with_clash_api,with_usbip,with_openvpn,with_openconnect,badlinkname,tfogo_checklinkname0,with_tailscale,ts_omit_logtail,ts_omit_ssh,ts_omit_drive,ts_omit_taildrop,ts_omit_webclient,ts_omit_doctor,ts_omit_capture,ts_omit_kube,ts_omit_aws,ts_omit_synology,ts_omit_bird \
  -ldflags="-s -w -buildid= -X github.com/sagernet/sing-box/constant.Version=1.14.4 -X runtime.godebugDefault=multipathtcp=0,tlssha1=1 -checklinkname=0" \
  -o "$AAR" \
  github.com/Diniboy1123/usque/android \
  ./experimental/libbox

test -s "$AAR"
cp "$AAR" "$APP/libs/usque.aar"
echo "Built one combined WARP + sing-box AAR:"
ls -lh "$AAR"
