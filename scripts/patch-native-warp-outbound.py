#!/usr/bin/env python3
"""Patch the pinned upstream modules with Hide Wi-Fi's native WARP dialer."""

from pathlib import Path
import sys

if len(sys.argv) != 3:
    raise SystemExit("usage: patch-native-warp-outbound.py <usque-module> <sing-box-module>")

usque = Path(sys.argv[1])
singbox = Path(sys.argv[2])


def replace_once(path: Path, old: str, new: str) -> None:
    content = path.read_text(encoding="utf-8")
    if new in content:
        return
    if old not in content:
        raise SystemExit(f"expected patch anchor not found in {path}: {old[:100]!r}")
    path.write_text(content.replace(old, new, 1), encoding="utf-8")


# Give the embedded MASQUE L4 client a socket factory. Android supplies
# sing-box's ProtectFunc so the QUIC underlay never re-enters the VPN TUN.
l4 = usque / "api/l4proxy.go"
replace_once(
    l4,
    "\tConnectTimeout    time.Duration\n\tConnectRetryCount int\n}",
    "\tConnectTimeout    time.Duration\n\tConnectRetryCount int\n"
    "\tListenUDP         func(context.Context, *net.UDPAddr) (*net.UDPConn, error)\n}",
)
replace_once(
    l4,
    "\tconnectTimeout    time.Duration\n\tconnectRetryCount int\n\tconnMu",
    "\tconnectTimeout    time.Duration\n\tconnectRetryCount int\n"
    "\tlistenUDP         func(context.Context, *net.UDPAddr) (*net.UDPConn, error)\n\tconnMu",
)
replace_once(
    l4,
    "\t\tconnectTimeout:    cfg.ConnectTimeout,\n\t\tconnectRetryCount: cfg.ConnectRetryCount,",
    "\t\tconnectTimeout:    cfg.ConnectTimeout,\n\t\tconnectRetryCount: cfg.ConnectRetryCount,\n"
    "\t\tlistenUDP:         cfg.ListenUDP,",
)
replace_once(
    l4,
    "\tudpConn, err := listenUDPForEndpoint(p.endpoint)\n",
    "\tvar udpConn *net.UDPConn\n\tvar err error\n"
    "\tif p.listenUDP != nil {\n\t\tudpConn, err = p.listenUDP(ctx, p.endpoint)\n"
    "\t} else {\n\t\tudpConn, err = listenUDPForEndpoint(p.endpoint)\n\t}\n",
)
replace_once(
    l4,
    "func closeL4HTTP3(udpConn *net.UDPConn, quicConn *quic.Conn) {\n"
    "\tif quicConn != nil {\n\t\t_ = quicConn.CloseWithError(0, \"\")\n\t}\n"
    "\tif udpConn != nil {\n\t\t_ = udpConn.Close()\n\t}\n}\n",
    "func closeL4HTTP3(udpConn *net.UDPConn, quicConn *quic.Conn) {\n"
    "\tif quicConn != nil {\n\t\t_ = quicConn.CloseWithError(0, \"\")\n\t}\n"
    "\tif udpConn != nil {\n\t\t_ = udpConn.Close()\n\t}\n}\n\n"
    "// Close releases the cached MASQUE/QUIC session. A later DialContext reconnects.\n"
    "func (p *L4Proxy) Close() error {\n"
    "\tif p == nil {\n\t\treturn nil\n\t}\n"
    "\tp.connMu.Lock()\n\tclient := p.client\n\tp.client = nil\n\tp.connMu.Unlock()\n"
    "\tif client != nil {\n\t\tcloseL4HTTP3(client.udpConn, client.quicConn)\n\t}\n"
    "\treturn nil\n}\n",
)

# Install the adapter in the pinned sing-box module copy.
target = singbox / "protocol/hidewifiwarp/outbound.go"
target.parent.mkdir(parents=True, exist_ok=True)
source = Path(__file__).resolve().parents[1] / "integration/go/protocol/hidewifiwarp/outbound.go"
target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

# Keep usque's internal-package imports inside the usque module boundary.
helper_source = Path(__file__).resolve().parents[1] / "integration/go/usque/api/hidewifi_config.go"
helper_target = usque / "api/hidewifi_config.go"
helper_target.write_text(helper_source.read_text(encoding="utf-8"), encoding="utf-8")

option_file = singbox / "option/outbound.go"
option_type = (
    "\n// WarpOutboundOptions configures the Cloudflare WARP MASQUE TCP dialer.\n"
    "type WarpOutboundOptions struct {\n"
    "\tConfigPath string `json:\"config_path\"`\n"
    "\tSNI        string `json:\"sni,omitempty\"`\n"
    "}\n"
)
content = option_file.read_text(encoding="utf-8")
if "type WarpOutboundOptions struct" not in content:
    option_file.write_text(content.rstrip() + "\n" + option_type, encoding="utf-8")

registry = singbox / "include/registry.go"
replace_once(
    registry,
    '\t"github.com/sagernet/sing-box/protocol/group"\n',
    '\t"github.com/sagernet/sing-box/protocol/group"\n'
    '\t"github.com/sagernet/sing-box/protocol/hidewifiwarp"\n',
)
replace_once(
    registry,
    '\tdirect.RegisterOutbound(registry)\n\tbridge.RegisterOutbound(registry)\n',
    '\tdirect.RegisterOutbound(registry)\n\tbridge.RegisterOutbound(registry)\n'
    '\thidewifiwarp.RegisterOutbound(registry)\n',
)
print("Installed Hide Wi-Fi WARP MASQUE TCP outbound and protected QUIC socket hook")
