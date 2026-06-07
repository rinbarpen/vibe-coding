# /desktop-build

Build, package, sign, and distribute a desktop application.

## Usage

```
/desktop-build <framework> <platform> [options]
```

### Framework

| Framework | CLI |
|-----------|-----|
| `electron` | electron-builder / electron-forge |
| `tauri` | Tauri Bundler |
| `flutter` | flutter build + flutter_distributor |

### Platform

| Platform | Target |
|----------|--------|
| `mac` | macOS (.dmg / .app) |
| `win` | Windows (.exe / .msi) |
| `linux` | Linux (.deb / .rpm / .AppImage) |
| `all` | All platforms (CI matrix) |

## Execution

1. Verify quality gates passed (lint + test + build check)
2. Run framework-specific build command
3. Package platform-specific artifacts
4. Code sign + notarize (macOS) or sign (Windows)
5. Generate update manifest/metadata
6. Output distribution paths

## Build Commands by Framework

| Framework | macOS | Windows | Linux |
|-----------|-------|---------|-------|
| Electron | `pnpm build:mac` | `pnpm build:win` | `pnpm build:linux` |
| Tauri | `pnpm tauri build --target universal-apple-darwin` | `pnpm tauri build --target x86_64-pc-windows-msvc` | `pnpm tauri build --target x86_64-unknown-linux-gnu` |
| Flutter | `flutter build macos` | `flutter build windows` | `flutter build linux` |

## Signing & Notarization

### macOS
- `codesign --deep --force --verify --verbose --sign "Developer ID Application" MyApp.app`
- `xcrun notarytool submit MyApp.dmg --apple-id $APPLE_ID --team-id $TEAM_ID --wait`
- `xcrun stapler staple MyApp.dmg`
- Certificates from GitHub Secrets: `APPLE_DEVELOPER_CERTIFICATE_BASE64`, `APPLE_NOTARY_KEY`

### Windows
- `signtool sign /fd SHA256 /a /f certificate.pfx /p $CERT_PASSWORD MyApp.exe`
- Certificate from GitHub Secrets: `WINDOWS_CERTIFICATE_BASE64`, `WINDOWS_CERT_PASSWORD`

### Linux
- Flatpak: `flatpak-builder build-dir org.myapp.yml --gpg-sign=$GPG_KEY`

## Exit Criteria

- [ ] Build: zero errors for target platform
- [ ] Tests: all pass
- [ ] Signed: verified for target platform
- [ ] Artifacts: generated and ready for distribution
- [ ] Update manifest: generated (JSON with version + hash + download URL)
