# CLAUDE.md — Desktop Flutter Scenario

## Architecture

- **Framework**: Flutter (Dart) + Material 3 / Cupertino
- **State**: Riverpod / Bloc / Provider
- **Packaging**: flutter_distributor / MSIX / DMG
- **Auto-update**: shorebird / sparkle_flutter

## Commands

| Command | Description |
|---------|-------------|
| `flutter run -d macos` | Run on macOS |
| `flutter run -d windows` | Run on Windows |
| `flutter run -d linux` | Run on Linux |
| `flutter test` | Run Dart tests |
| `flutter build macos` | Build macOS release |
| `flutter build windows` | Build Windows release |
| `flutter build linux` | Build Linux release |
| `/desktop-build` | Cross-platform build & package |

## Development Standards

- Platform adaptation: Material 3 (cross-platform) + Cupertino (macOS/iOS polish).
- Responsive layout: `LayoutBuilder` + breakpoints for window resizing.
- Persistence: `shared_preferences` / `drift` (SQLite) / `Isar`.
- Platform channels: `MethodChannel` / `Pigeon` for native OS interaction.

## Key Directories

- `lib/` — Dart source code
- `lib/screens/` — Full-page screens
- `lib/widgets/` — Reusable UI components
- `lib/services/` — Platform service abstractions
- `test/` — Dart unit and widget tests
- `linux/`, `macos/`, `windows/` — Platform-specific native wrappers
