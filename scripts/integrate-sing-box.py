#!/usr/bin/env python3
"""Install the pinned libbox AAR and first-party Kotlin integration sources."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "upstream/usque-android/android/usque-vpn/app"
GRADLE = APP / "build.gradle.kts"
MANIFEST = APP / "src/main/AndroidManifest.xml"
gradle = GRADLE.read_text(encoding="utf-8")
marker = 'implementation(files("libs/usque.aar"))'
if marker not in gradle:
    raise SystemExit("Could not locate combined WARP + sing-box AAR dependency")

source_root = ROOT / "integration/src/main/kotlin/com/abobo/usquevpn"
target_root = APP / "src/main/kotlin/com/abobo/usquevpn"
target_root.mkdir(parents=True, exist_ok=True)
for name in ("SingBoxCoreInfo.kt", "SingBoxNodeStore.kt", "NodeProfilesActivity.kt"):
    (target_root / name).write_text((source_root / name).read_text(encoding="utf-8"), encoding="utf-8")

manifest = MANIFEST.read_text(encoding="utf-8")
entry = '''        <activity
            android:name=".NodeProfilesActivity"
            android:exported="false"
            android:label="sing-box 节点管理" />'''
if ".NodeProfilesActivity" not in manifest:
    manifest = manifest.replace("    </application>", entry + "\n\n    </application>")
    MANIFEST.write_text(manifest, encoding="utf-8")
main_activity = target_root / "MainActivity.kt"
if main_activity.exists():
    main_text = main_activity.read_text(encoding="utf-8")
    old_menu = '''.setItems(arrayOf("后台保护", "关于")) { _, which ->
                if (which == 0) showBackgroundProtection() else showAbout()
            }'''
    new_menu = '''.setItems(arrayOf("sing-box 节点管理", "后台保护", "关于")) { _, which ->
                when (which) {
                    0 -> startActivity(Intent(this, NodeProfilesActivity::class.java))
                    1 -> showBackgroundProtection()
                    else -> showAbout()
                }
            }'''
    if old_menu in main_text:
        main_text = main_text.replace(old_menu, new_menu)
    elif "NodeProfilesActivity::class.java" not in main_text:
        raise SystemExit("Could not safely add node manager to the existing app menu")
    main_activity.write_text(main_text, encoding="utf-8")
print("Installed combined WARP + sing-box bindings, local node store and profile activity")
