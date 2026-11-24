# Android release signing

The release workflow intentionally refuses to build a release APK unless all four GitHub Actions secrets are present. Do not commit a keystore or send its passwords in chat.

## 1. Create a long-lived upload/release keystore locally

Use a secure workstation and keep an offline backup. Losing this key prevents future in-place updates signed with the same application ID.

```bash
keytool -genkeypair -v \
  -keystore hide-wifi-release.jks \
  -alias hide-wifi \
  -keyalg RSA -keysize 4096 -validity 10000
```

Choose strong, unique passwords. Keep the keystore and passwords private.

## 2. Encode the keystore

Linux/macOS:

```bash
base64 -w 0 hide-wifi-release.jks
```

On macOS, use `base64 < hide-wifi-release.jks | tr -d '\\n'`.

## 3. Add repository Actions secrets

Open **Settings → Secrets and variables → Actions → New repository secret** and add:

- `ANDROID_KEYSTORE_BASE64`: the base64 output from step 2
- `ANDROID_KEYSTORE_PASSWORD`: the keystore password
- `ANDROID_KEY_ALIAS`: `hide-wifi` (or the alias chosen above)
- `ANDROID_KEY_PASSWORD`: the key password

Never put these values in GitHub Variables, source code, workflow logs, issues, or chat messages.

## 4. Build and verify

The workflow decodes the key only into the ephemeral GitHub runner's temporary directory, builds `assembleRelease`, checks APK alignment, verifies the APK signature with `apksigner`, confirms ARM64 and ARM32 native libraries, and publishes the APK plus SHA-256 file for a version tag.

A release tag must not be created until the DNS-over-HTTPS implementation and its fail-closed / WARP-routing tests have passed. The signing setup alone does not make an APK ready for release.
