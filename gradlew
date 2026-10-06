#!/bin/sh
set -eu

APP_HOME=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
WRAPPER_DIR="$APP_HOME/gradle/wrapper"
WRAPPER_JAR="$WRAPPER_DIR/gradle-wrapper.jar"
WRAPPER_URL="https://raw.githubusercontent.com/gradle/gradle/v8.7.0/gradle/wrapper/gradle-wrapper.jar"
WRAPPER_SHA256="cb0da6751c2b753a16ac168bb354870ebb1e162e9083f116729cec9c781156b8"

checksum() {
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum "$1" | awk '{print $1}'
    elif command -v shasum >/dev/null 2>&1; then
        shasum -a 256 "$1" | awk '{print $1}'
    else
        echo "ERROR: sha256sum or shasum is required to verify the Gradle wrapper." >&2
        exit 1
    fi
}

bootstrap_wrapper() {
    mkdir -p "$WRAPPER_DIR"
    tmp="$WRAPPER_JAR.tmp.$$"
    trap 'rm -f "$tmp"' EXIT HUP INT TERM

    if command -v curl >/dev/null 2>&1; then
        curl --fail --location --silent --show-error "$WRAPPER_URL" --output "$tmp"
    elif command -v wget >/dev/null 2>&1; then
        wget -q "$WRAPPER_URL" -O "$tmp"
    else
        echo "ERROR: curl or wget is required to download the Gradle wrapper." >&2
        exit 1
    fi

    actual=$(checksum "$tmp")
    if [ "$actual" != "$WRAPPER_SHA256" ]; then
        echo "ERROR: Gradle wrapper checksum mismatch: $actual" >&2
        exit 1
    fi

    mv "$tmp" "$WRAPPER_JAR"
    trap - EXIT HUP INT TERM
}

if [ ! -f "$WRAPPER_JAR" ] || [ "$(checksum "$WRAPPER_JAR")" != "$WRAPPER_SHA256" ]; then
    bootstrap_wrapper
fi

if [ -n "${JAVA_HOME:-}" ]; then
    JAVACMD="$JAVA_HOME/bin/java"
else
    JAVACMD=java
fi

if ! command -v "$JAVACMD" >/dev/null 2>&1 && [ ! -x "$JAVACMD" ]; then
    echo "ERROR: Java was not found. Set JAVA_HOME or add java to PATH." >&2
    exit 1
fi

exec "$JAVACMD" ${JAVA_OPTS:-} ${GRADLE_OPTS:-} \
    -Dorg.gradle.appname=gradlew \
    -classpath "$WRAPPER_JAR" \
    org.gradle.wrapper.GradleWrapperMain "$@"
