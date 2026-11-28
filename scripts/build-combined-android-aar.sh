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

# Match the gomobile version pinned by sing-box v1.14.4.
GOMOBILE_VERSION="v0.1.12"
GOBIN="$(go env GOPATH)/bin"
export GOBIN
go install "github.com/sagernet/gomobile/cmd/gomobile@$GOMOBILE_VERSION"
go install "github.com/sagernet/gomobile/cmd/gobind@$GOMOBILE_VERSION"
"$GOBIN/gomobile" init -v

mkdir -p "$BUILD_ROOT" "$APP/libs"
# Keep sing-box as the main module so its pinned fork replacements remain active.
if [[ ! -f "$SINGBOX_DIR/go.mod" ]]; then
  module_json="$(go mod download -json github.com/sagernet/sing-box@v1.14.4)"
  module_dir="$(python3 -c 'import json,sys; print(json.load(sys.stdin)["Dir"])' <<< "$module_json")"
  cp -a "$module_dir" "$SINGBOX_DIR"
fi
# Go's module cache marks downloaded source files read-only. The integration
# step edits go.mod and adds a bridge source file, so make this private build
# copy writable without changing the shared module cache.
chmod -R u+rwX "$SINGBOX_DIR"

cd "$SINGBOX_DIR"
go mod edit -require=github.com/Diniboy1123/usque@v0.0.0
go mod edit -replace="github.com/Diniboy1123/usque=$UPSTREAM"
# Resolve and record every transitive dependency used by the generated sing-box + WARP bridge.
go mod tidy

# Inject the real sing-box WARP MASQUE TCP outbound and Android-protected
# QUIC underlay socket factory into the pinned source copies.
python3 "$ROOT/scripts/patch-native-warp-outbound.py" "$UPSTREAM" "$SINGBOX_DIR"

# Legacy Android tunnel-control compatibility API only:
# The native hidewifiwarp outbound above does not call StartTunnel or consume
# an Android TUN descriptor. Never start this legacy tunnel concurrently with
# the sing-box VpnService; the app must migrate to one VpnService owner.
cat > experimental/libbox/hidewifi_warp_bridge.go <<'GO_BRIDGE'
//go:build android

// Package libbox exposes the Hide Wi-Fi WARP bridge through the same gomobile
// binding entrypoint and Go runtime as sing-box.
package libbox

import usqueandroid "github.com/Diniboy1123/usque/android"

// HideWifiWarpPacketFlow receives packets emitted by the WARP MASQUE tunnel.
type HideWifiWarpPacketFlow interface {
	WritePacket(data []byte)
}

// HideWifiWarpStateCallback receives WARP tunnel lifecycle events.
type HideWifiWarpStateCallback interface {
	OnConnected()
	OnDisconnected(reason string)
	OnError(message string)
}

func WarpRegister(configPath string, deviceName string) string {
	return usqueandroid.Register(configPath, deviceName)
}

func WarpIsRegistered(configPath string) bool {
	return usqueandroid.IsRegistered(configPath)
}

func WarpGetAssignedIPv4(configPath string) string {
	return usqueandroid.GetAssignedIPv4(configPath)
}

func WarpGetAssignedIPv6(configPath string) string {
	return usqueandroid.GetAssignedIPv6(configPath)
}

func WarpGetDefaultEndpoint(configPath string) string {
	return usqueandroid.GetDefaultEndpoint(configPath)
}

func WarpStartTunnel(configPath string, tunFd int, mtu int, packetFlow HideWifiWarpPacketFlow, callback HideWifiWarpStateCallback) string {
	return usqueandroid.StartTunnel(configPath, tunFd, mtu, packetFlow, callback)
}

func WarpStartTunnelWithFd(configPath string, tunFd int, callback HideWifiWarpStateCallback) string {
	return usqueandroid.StartTunnelWithFd(configPath, tunFd, callback)
}

func WarpStopTunnel() {
	usqueandroid.StopTunnel()
}

func WarpIsRunning() bool {
	return usqueandroid.IsRunning()
}

func WarpIsConnected() bool {
	return usqueandroid.IsConnected()
}

func WarpGetVersion() string {
	return usqueandroid.GetVersion()
}

func WarpSetSNI(sni string) {
	usqueandroid.SetSNI(sni)
}

func WarpGetSNI() string {
	return usqueandroid.GetSNI()
}

func WarpSetEndpoint(endpoint string) {
	usqueandroid.SetEndpoint(endpoint)
}

func WarpGetEndpoint() string {
	return usqueandroid.GetEndpoint()
}

func WarpResetConnectionOptions() {
	usqueandroid.ResetConnectionOptions()
}

func WarpTestEndpoint(configPath string, endpoint string, timeoutMs int64) string {
	return usqueandroid.TestEndpoint(configPath, endpoint, timeoutMs)
}
GO_BRIDGE

# Compile-check the custom WARP outbound and libbox bridge before binding.
gofmt -w protocol/hidewifiwarp/outbound.go experimental/libbox/hidewifi_warp_bridge.go "$UPSTREAM/api/l4proxy.go" "$UPSTREAM/api/hidewifi_config.go"
go test -run '^$' -tags=with_gvisor,with_quic,with_wireguard,with_utls,with_naive_outbound,with_clash_api,with_usbip,with_openvpn,with_openconnect,badlinkname,tfogo_checklinkname0,with_tailscale,ts_omit_logtail,ts_omit_ssh,ts_omit_drive,ts_omit_taildrop,ts_omit_webclient,ts_omit_doctor,ts_omit_capture,ts_omit_kube,ts_omit_aws,ts_omit_synology,ts_omit_bird ./protocol/hidewifiwarp ./experimental/libbox

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
  ./experimental/libbox

test -s "$AAR"
cp "$AAR" "$APP/libs/usque.aar"
echo "Built unified WARP + sing-box AAR from the single libbox binding package:"
ls -lh "$AAR"
