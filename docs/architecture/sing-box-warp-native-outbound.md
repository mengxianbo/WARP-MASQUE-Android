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

## WARP outbound contract

Implement a real sing-box outbound adapter (not an Android VPN service wrapper):

- Register an outbound type/tag (for example `warp`) in the sing-box outbound registry used by the pinned v1.14.4 build.
- Implement the sing-box outbound dialer contract for TCP and packet/UDP traffic, lifecycle start/close, interface-change handling, and cancellation.
- Carry WARP's MASQUE/QUIC transport without creating or owning an Android TUN descriptor.
- Ensure the WARP underlay socket is protected/bound to the physical network so it cannot re-enter the sing-box TUN.
- Expose WARP as a dialer usable by VLESS via the supported `detour`/dialer chain mechanism. Validate TCP and UDP independently; do not advertise UDP until packet semantics are implemented and tested.
- Keep WARP registration/account state separate from node share links and never commit credentials/private keys.

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

The current node store persists a per-node `warp` or `direct` preference and the activity displays a node-management preview. The current Go bridge exposes WARP tunnel lifecycle methods; it is not a registered sing-box outbound. Therefore the chain is **not implemented yet** and no APK should be described as supporting VLESS -> WARP until the acceptance tests above pass.
