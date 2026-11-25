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
: "${ANDROID_NDK_HOME:=$ANDROID_HOME/ndk/28.0.13004108}"
export ANDROID_NDK_HOME

# Match sing-box v1.14.4's own gomobile toolchain and build tags.
# gomobile must also be present in the target module's go.mod: gobind resolves
# github.com/sagernet/gomobile/bind from that module, not from GOBIN.
GOMOBILE_VERSION="v0.1.12"
GOBIN="$(go env GOPATH)/bin"
export GOBIN
go install "github.com/sagernet/gomobile/cmd/gomobile@$GOMOBILE_VERSION"
go install "github.com/sagernet/gomobile/cmd/gobind@$GOMOBILE_VERSION"
"$GOBIN/gomobile" init -v

mkdir -p "$BIND_DIR" "$APP/libs"
cat > "$BIND_DIR/go.mod" <<'EOF'
module github.com/mengxianbo/hidewifi-android-bind

go 1.25.5

require (
    github.com/Diniboy1123/usque v0.0.0
    github.com/sagernet/gomobile v0.1.12
    github.com/sagernet/sing-box v1.14.4
)

replace github.com/Diniboy1123/usque => ../..
EOF

cd "$BIND_DIR"
go mod download

# These are the official sing-box Android tags from cmd/internal/build_libbox.
# Keep both engines in one gomobile invocation so the resulting AAR contains
# only one Go runtime / go.Seq implementation.
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
  github.com/sagernet/sing-box/experimental/libbox

test -s "$AAR"
cp "$AAR" "$APP/libs/usque.aar"
echo "Built one combined AAR containing WARP + sing-box with one gomobile runtime:"
ls -lh "$AAR"
