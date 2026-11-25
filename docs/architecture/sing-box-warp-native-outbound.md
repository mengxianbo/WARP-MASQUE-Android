# sing-box + WARP + VLESS WebSocket + custom proxy outbounds

## Product requirements

Hide Wi-Fi retains its existing WARP feature and uses one Android VPN service and one sing-box TUN. VLESS is a first-class imported node protocol with these transports:

- VLESS + WebSocket without TLS (query parameter type=ws and security=none or omitted).
- VLESS + WebSocket + TLS (query parameter type=ws and security=tls).

The URL importer/runtime converter must preserve UUID, server, port, WS path, Host header and TLS SNI/server name. TLS certificate verification must remain enabled by default. Do not silently downgrade TLS or accept unsupported security modes as WS.

Users may add SOCKS5, HTTP and HTTPS outbounds separately. A VLESS node can store a desired egress of WARP, DIRECT, or one of those custom outbounds.

## Expected sing-box configuration shape

VLESS WS:

```json
{
  "type": "vless",
  "tag": "vless-ws",
  "server": "vless.example.com",
  "server_port": 80,
  "uuid": "00000000-0000-0000-0000-000000000000",
  "transport": { "type": "ws", "path": "/ws", "headers": { "Host": "cdn.example.com" } }
}
```

VLESS WS + TLS:

```json
{
  "type": "vless",
  "tag": "vless-ws-tls",
  "server": "vless.example.com",
  "server_port": 443,
  "uuid": "00000000-0000-0000-0000-000000000000",
  "transport": { "type": "ws", "path": "/ws", "headers": { "Host": "cdn.example.com" } },
  "tls": { "enabled": true, "server_name": "cdn.example.com" }
}
```

These are illustrative sing-box config shapes, not ready-to-use profiles.

## Custom egress examples

SOCKS5:

```json
{ "type": "socks", "tag": "custom-socks", "server": "proxy.example.com", "server_port": 1080, "version": "5" }
```

HTTP / HTTPS:

```json
{ "type": "http", "tag": "custom-http", "server": "proxy.example.com", "server_port": 8080 }
```

HTTPS additionally enables TLS in the HTTP outbound. Optional credentials are included only when supplied. Runtime must use sing-box outbound detour to chain the VLESS node through the selected egress.

## Current implementation status and limitations

- Android node management UI accepts VLESS URLs only when they specify WebSocket and either no TLS or TLS.
- Separate SOCKS5 / HTTP / HTTPS outbound profiles can be stored and selected as a per-node preference.
- Credentials are currently stored in app SharedPreferences; this is not an encrypted credential vault.
- **The live sing-box config builder and runtime detour wiring are not present in this repository's current Android source tree.** These controls currently persist management preferences and do not yet alter live traffic.
- The existing native WARP outbound is TCP-only. It can carry the VLESS server's TCP WebSocket transport; do not claim general UDP proxying through WARP.
- Do not publish this as operational chain routing until runtime config builder, sing-box config validation, Android service integration, CI build and real-device tests are complete.

## Acceptance tests

1. Import valid VLESS WS and VLESS WS+TLS share URLs; verify UUID, server, port, path, Host and SNI survive conversion.
2. Reject VLESS non-WS transports and unsupported security modes with a clear message.
3. Add/delete SOCKS5, HTTP and HTTPS outbounds; optional credentials are handled without displaying secrets.
4. Verify runtime detour for VLESS -> WARP, DIRECT, SOCKS5 and HTTP(S).
5. Test DNS fail-closed, TLS certificate validation, IPv4/IPv6, reconnect and network changes.
6. Verify one VPN service/TUN only and no plaintext DNS fallback.
