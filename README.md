# JianxianAPP Warp

JianxianAPP Warp：简体中文 Android 客户端，基于非官方 Cloudflare WARP / MASQUE 实现。

## 构建目标

- APK
- 最低 Android：8.0（API 26）
- ABI：`arm64-v8a` + `armeabi-v7a`
- VPN：Android `VpnService`，由 Go MASQUE 核心承载 TUN 数据面
- CI：GitHub Actions 自动构建并上传 APK

## 下载 APK

打开本仓库的 **Actions → Android APK → Artifacts** 下载最近一次构建产物。发布版本则从 **Releases** 下载。

> 首次构建完成前不会有 APK。CI 产物是使用 GitHub Actions 临时 debug 签名密钥签名的测试 APK；后续正式分发应配置由项目维护者长期保管的 Android release keystore。不要把 keystore 或 WARP 的 `config.json` 提交到仓库。

## 使用

1. 安装 APK。
2. 首次连接时允许 Android VPN 权限。
3. 应用首次启动 VPN 时会注册 WARP 设备并在应用私有目录保存配置。
4. 在应用中点击 Connect。连接状态以应用实际握手状态为准。

请勿分享 `config.json`，其中包含设备密钥和账户凭据。

## Hide Wi-Fi 局域网 HTTP 代理

- 先连接应用内的 WARP VPN，再启动 HTTP 代理；默认监听 TCP 端口 `6668`。
- 账号和密码可在应用内手动编辑；认证默认开启，也可在可信局域网内按需关闭。
- 其他设备需手动将 HTTP 代理设置为手机的局域网 IP 和端口 `6668`。普通无 Root Android 不保证自动透明接管热点客户端流量。
- 代理仅允许回环、私有网段和链路本地地址作为客户端来源，不面向公网开放。
- 代理支持 HTTP 请求与 HTTPS CONNECT（TCP）；不转发 UDP / QUIC，不能单靠此代理防止 WebRTC 泄漏。需要完整 UDP 防绕过时，客户端设备应使用自己的 VPN/TUN。

## 源码与上游

Android 应用与 Go MASQUE 核心通过 Git submodule 引入：

- 上游：[`Abobo7/usque-android`](https://github.com/Abobo7/usque-android)
- 固定版本：`1bc50c004b99e6df42fc17f4f93320d782020dde`
- 上游许可证：MIT，见子模块中的 `LICENSE.md`

本仓库维护独立的构建入口、Android 8.0 最低版本约束、双 ABI 检查和 APK 发布工作流。上游源码保留在 `upstream/usque-android`，并通过固定 commit 锁定，避免构建时自动漂移。

## 本地构建

需要 JDK 17、Go（版本以子模块 `go.mod` 为准）、Android SDK/NDK。

```bash
git clone --recurse-submodules https://github.com/mengxianbo/WARP-MASQUE-Android.git
cd WARP-MASQUE-Android
export ANDROID_HOME="$HOME/Android/Sdk"
export ANDROID_NDK_HOME="$ANDROID_HOME/ndk/26.3.11579264"

cd upstream/usque-android/android
make init
make android
mkdir -p ../usque-vpn/app/libs
cp usque.aar ../usque-vpn/app/libs/usque.aar
cd ../usque-vpn
sed -i 's/minSdk = 24/minSdk = 26/' app/build.gradle.kts
./gradlew clean assembleDebug
```

APK 输出路径：`app/build/outputs/apk/debug/app-debug.apk`。

## 自动构建

- Push 到 `main`：构建 Debug APK 并上传 Actions Artifact。
- 手动触发：Actions → Android APK → Run workflow。
- 推送 `v*` 标签：构建 APK 并创建 GitHub Release。

工作流会检查 APK 中同时存在 `arm64-v8a` 与 `armeabi-v7a` 两种 native ABI。

## 免责声明

本项目是社区项目，与 Cloudflare, Inc. 无隶属、赞助或背书关系。WARP、Cloudflare 及相关商标归其各自所有者所有。MASQUE 核心是非官方实现，按原样提供；使用者应自行遵守当地法律及 Cloudflare 服务条款。CI 成功不代表已在所有 Android 设备/网络环境完成实机验证。

## License

Hide Wi-Fi project code maintained in this repository is licensed under the GNU General Public License v3.0 only; see [LICENSE](LICENSE). Third-party components retain their own licenses and notices. In particular, the pinned `usque-android` submodule remains under its upstream MIT license. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Before distributing a build containing sing-box/libbox, the exact libbox source revision, corresponding source, transitive notices and any upstream additional terms must also be included.
