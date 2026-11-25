# sing-box + WARP native outbound architecture

## Product requirement

Hide Wi-Fi must run exactly one Android `VpnService` and one sing-box TUN. WARP and user-imported proxy nodes are outbounds inside that sing-box runtime. A second WARP-owned TUN is not an acceptable implementation.

For every imported proxy node, the user can select:

- `direct`: the proxy node dials its server over the device's underlying network.
- `warp`: the proxy node's transport/dialer is carried by the WARP outbound (VLESS -> WARP -> destination).

The app also keeps standalone WARP and DIRECT as selectable global modes. Per-node preference and global mode must not overwrite one another.

## Required data plane

```text
Android VpnService (single owner)
  -> sing-box TUN
     -> route rules / DNS
        -> node selector
           -> VLESS node (detour=warp) -> WARP outbound -> Internet
           -> VLESS node (detour=direct) ----------------> Internet
           -> WARP outbound (standalone) ----------------> Internet
           -> direct outbound (standalone) --------------> Internet
```

## Implemented Go adapter milestone

The branch now contains a build-time injected sing-box outbound with type `warp`:

- It reads the existing usque account config from `config_path`, derives the client certificate, and validates the MASQUE endpoint public key.
- It uses usque's HTTP/3 L4 CONNECT client to create TCP streams through WARP.
- Its QUIC UDP socket is created through sing-box's `NetworkManager.ProtectFunc()`, so Android can protect the underlay socket from the app's VPN TUN.
- It implements sing-box outbound registration, lifecycle cleanup, and network-change reset.
- It advertises **TCP only**. This is sufficient for the VLESS server transport: VLESS UDP payloads can be encapsulated inside the VLESS TCP connection. It is not yet a general-purpose WARP UDP outbound.

Example sing-box configuration shape:

```json
{
  "outbounds": [
    {
      "type": "warp",
      "tag": "warp",
      "config_path": "/absolute/app-private-path/warp-config.json",
      "sni": "consumer-masque.cloudflareclient.com"
    },
    {
      "type": "vless",
      "tag": "node-vless",
      "server": "vless.example.com",
      "server_port": 443,
      "uuid": "00000000-0000-0000-0000-000000000000",
      "tls": { "enabled": true, "server_name": "vless.example.com" },
      "detour": "warp"
    }
  ]
}
```

The Android config builder still needs to supply the actual private app config path and select `detour: warp` per node. Do not hand this example to users as a ready-to-paste profile.

## Remaining work

- Add the runtime config builder / per-node detour wiring in Android.
- Implement a full WARP IP/UDP data plane for standalone WARP mode; this first adapter intentionally rejects packet connections.
- Add tests for MASQUE certificate pinning, TCP CONNECT, socket protection, interface changes, VLESS chain egress, DNS and IPv6.
- Build the APK and validate on a real Android device before claiming the chain is usable.

## Important distinction: current bridge is not this adapter

The existing `hidewifi_warp_bridge.go` calls `usqueandroid.StartTunnel(...)` / `StartTunnelWithFd(...)`. Those APIs start or attach a WARP tunnel to a TUN file descriptor. Binding those methods into the same gomobile `libbox` package does **not** make WARP a sing-box outbound and does **not** prove there is only one TUN owner. Do not use that bridge as the implementation of VLESS -> WARP.

Before replacing it, inspect the exact pinned usque Android API and the sing-box v1.14.4 registry, dialer, lifecycle, and Android socket-protection APIs. Add compile-time interface assertions against the pinned version.

## Acceptance criteria

1. Android starts one `VpnService`; no second WARP VPN consent prompt or second TUN descriptor is created.
2. Selecting `VLESS -> WARP` makes the VLESS server transport traverse WARP; packet capture / controlled endpoint tests prove the egress.
3. Selecting `VLESS -> DIRECT` bypasses WARP while retaining VLESS.
4. Standalone WARP and standalone DIRECT both work.
5. TCP and UDP tests are reported separately, including DNS, IPv4 and IPv6.
6. WARP underlay does not loop into TUN; airplane-mode/network-change/reconnect tests pass.
7. DNS fail-closed behavior is verified: no plaintext DNS fallback when the protected resolver is unavailable.
8. UI only reports a mode as active after the runtime acknowledges applying it. A stored preference alone is not proof of routing.

## Current implementation status

The node store still persists per-node `warp` or `direct` preferences as preview data. The Go source now contains a TCP-only `warp` outbound adapter and a build-time registration patch, but the Android config builder does not yet translate those preferences into runtime `detour` settings. The outbound and chain are therefore not yet user-operational; no APK should be described as supporting VLESS -> WARP until CI, runtime wiring and real-device acceptance tests pass.
