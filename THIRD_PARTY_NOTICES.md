# Third-party notices

Hide Wi-Fi project code maintained in this repository is licensed under GNU GPL version 3.0 only. The complete license text is in [LICENSE](LICENSE).

## Bundled and upstream components

### usque-android (WARP MASQUE engine)
- Upstream: https://github.com/Abobo7/usque-android
- Pinned commit: `1bc50c004b99e6df42fc17f4f93320d782020dde`
- License: MIT
- The upstream license and copyright notice are retained in the upstream submodule at `upstream/usque-android/LICENSE.md`. The GPL-3.0 license for this repository does not remove or replace that separate MIT notice.

### sing-box / libbox (source-bound into the combined Android AAR)
- Upstream Android binding API: https://github.com/singbox-android/libbox
- Upstream project: https://github.com/SagerNet/sing-box
- Version: 1.14.4 (release tag `1.14.4`, published 2026-10-25).
- The Android bindings are generated from the pinned `SagerNet/sing-box` source in the same `gomobile bind` invocation as the WARP engine, producing one AAR and one Go JNI runtime. This avoids duplicate `go.Seq` classes and competing `libgojni.so` files from separately-built Go AARs.
- License: GPL-3.0-or-later. The project pins this upstream release; preserve the upstream license and notices.
- The exact source tag and build tool version are pinned in `scripts/build-combined-android-aar.sh`; record the resolved source commit, complete corresponding source, transitive dependency licenses, and any upstream additional terms before distributing an APK containing sing-box.
- Do not imply that Hide Wi-Fi is an official sing-box or SagerNet application.

## Trademarks
Cloudflare, WARP, sing-box and other product names are trademarks of their respective owners. Hide Wi-Fi is an independent community project and is not endorsed by Cloudflare or SagerNet.
