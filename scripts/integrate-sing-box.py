#!/usr/bin/env python3
"""Install the pinned libbox AAR and first-party Kotlin integration sources."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "upstream/usque-android/android/usque-vpn/app"
AAR = APP / "libs/libbox.aar"
GRADLE = APP / "build.gradle.kts"
MANIFEST = APP / "src/main/AndroidManifest.xml"
if not AAR.is_file() or AAR.stat().st_size < 100_000_000:
    raise SystemExit("Missing/incomplete libbox.aar; download step did not complete")
gradle = GRADLE.read_text(encoding="utf-8")
dep = 'implementation(files("libs/libbox.aar"))'
if dep not in gradle:
    marker = 'implementation(files("libs/usque.aar"))'
    if marker not in gradle:
        raise SystemExit("Could not locate existing usque AAR dependency")
    gradle = gradle.replace(marker, marker + '\n    // Official sing-box Android core\n    ' + dep)
    GRADLE.write_text(gradle, encoding="utf-8")

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
print("Installed sing-box AAR, version bridge, local node store and profile activity")
