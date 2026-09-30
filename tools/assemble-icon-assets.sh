#!/usr/bin/env bash
set -euo pipefail
cat Wallas-assets.part01 Wallas-assets.part02 Wallas-assets.part03 Wallas-assets.part04 > Wallas-Fluffy-Stuffys-v1.0.0-ICON-ASSETS.zip
sha256sum -c - <<'EOF'
2c00f3c617ab27633f79f8b68d42e3acda614f7621387a2f7da7bc93385a2b9d  Wallas-Fluffy-Stuffys-v1.0.0-ICON-ASSETS.zip
EOF
