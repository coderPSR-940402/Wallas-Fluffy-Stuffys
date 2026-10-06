# Walla's Fluffy Stuffy's

Android icon-pack source for package `com.wallathemes.fluffystuffys`.

## Reproducible build

The repository contains four split icon-asset archive parts. Gradle reconstructs them, verifies the archive SHA-256, and generates the 349 WebP icon resources plus icon-pack XML under `app/build/generated/walla/res` before every build.

```sh
./gradlew :app:assembleDebug
./gradlew :app:assembleRelease
```

The launcher bootstraps the official Gradle 8.7 wrapper JAR from Gradle's pinned `v8.7.0` GitHub tag when needed and verifies its published SHA-256 before execution. The Gradle 8.7 distribution is also pinned by SHA-256 in `gradle/wrapper/gradle-wrapper.properties`.

## Release signing

CI never generates a disposable signing key. To produce an update-compatible install-ready APK, configure these GitHub Actions repository secrets from one permanent Android release keystore:

- `WALLA_RELEASE_KEYSTORE_BASE64`
- `WALLA_RELEASE_KEYSTORE_PASSWORD`
- `WALLA_RELEASE_KEY_ALIAS`
- `WALLA_RELEASE_KEY_PASSWORD`

If none are configured, CI still validates the complete release build but uploads it explicitly as an unsigned validation APK. Partial signing configuration fails the workflow.
