#!/usr/bin/env python3
"""Prepare the pinned official sing-box libbox AAR for the Android app."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "upstream/usque-android/android/usque-vpn/app"
AAR = APP / "libs/libbox.aar"
GRADLE = APP / "build.gradle.kts"
if not AAR.is_file() or AAR.stat().st_size < 100_000_000:
    raise SystemExit("Missing or incomplete libbox.aar; run the pinned download step first")
text = GRADLE.read_text(encoding="utf-8")
dep = 'implementation(files("libs/libbox.aar"))'
if dep not in text:
    text = text.replace('implementation(files("libs/usque.aar"))',
                        'implementation(files("libs/usque.aar"))\n    // Official sing-box Android core (GPL-3.0-or-later)\n    ' + dep)
GRADLE.write_text(text, encoding="utf-8")
print("Prepared official sing-box libbox AAR dependency")
