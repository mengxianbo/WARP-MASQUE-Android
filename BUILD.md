# Build notes

The canonical build commands are in `scripts/build-apk.sh`. CI runs the same Go-to-AAR and Gradle pipeline against the pinned upstream submodule, enforces Android API 26, and checks both Android ARM ABIs before uploading the APK.
