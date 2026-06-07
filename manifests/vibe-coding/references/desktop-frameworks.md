# Desktop Framework Comparison & Selection Guide

## Comparison Matrix

| Criteria | Electron | Tauri | Flutter Desktop |
|----------|----------|-------|-----------------|
| Bundle size | ~150MB | ~5MB | ~20MB |
| Memory usage | ~200MB | ~50MB | ~80MB |
| Startup time | ~2s | ~0.3s | ~0.5s |
| UI technology | HTML/CSS/JS | HTML/CSS/JS | Skia (Dart) |
| Backend language | Node.js | Rust | Dart |
| Ecosystem | Mature (2013) | Growing (2022) | Emerging (2022+ for desktop) |
| Auto-update | electron-updater | Plugin updater | Shorebird / self-built |
| Mac App Store | Yes | Limited | Yes |
| Microsoft Store | Yes (MSIX) | Yes (MSIX) | Yes (MSIX) |
| Linux Flathub | Yes | Yes | Yes |
| Code signing | Native + electron-builder | Tauri bundler | flutter_distributor |
| Notarization | electron-notarize | Manual (rcodesign) | Manual (codesign) |
| IPC | contextBridge + ipcMain | Rust invoke commands | MethodChannel / Pigeon |
| Multi-window | Native | Supported | desktop_multi_window |
| System tray | Native | Plugin | system_tray |

## Decision Tree

**Q1: Do you need full Node.js + Chromium API access within your desktop app?**
→ Yes: **Electron** (mature ecosystem, every Node.js package available)
→ No: Continue

**Q2: Is minimal binary size and low memory usage critical?**
→ Yes: **Tauri** (~5MB base, ~50MB memory)
→ No: Continue

**Q3: Are you sharing a codebase with mobile (iOS/Android)?**
→ Yes: **Flutter Desktop** (shared Dart codebase across mobile + desktop)
→ No: Continue

**Q4: Is your team primarily skilled in Rust?**
→ Yes: **Tauri** (leverage Rust expertise for backend logic)
→ No: **Electron** (better JS/TS ecosystem, lower Rust learning curve)

**Q5: Are you building for Windows-only with an existing .NET team?**
→ Yes: **.NET MAUI** or **WinUI 3** (not covered in depth here — see `dotnet-patterns` skill)
→ No: Choose based on Q1-Q4.

## Language Mapping

| Framework | UI Language | Backend Language | Mobile Sharing |
|-----------|------------|-----------------|----------------|
| Electron | TypeScript/JS | Node.js (TypeScript) | None |
| Tauri | TypeScript/JS | Rust | None |
| Flutter Desktop | Dart | Dart | iOS + Android |
| .NET MAUI | C# (XAML/Blazor) | C# | iOS + Android |
| Qt | C++ (QML) | C++ | Android (limited) |

## When to Use Each

### Electron — Best For:
- Apps that need deep OS integration via Node.js native modules
- Teams with strong frontend (React/Vue) skills
- Rapid prototyping of desktop apps from existing web apps
- Apps that embed web content or need DevTools in production
- Slack, VS Code, Discord, Figma are Electron

### Tauri — Best For:
- Apps where bundle size and memory matter (download/launch speed)
- Teams with Rust skills or willing to learn
- Security-sensitive apps (Rust memory safety, minimal attack surface)
- New projects starting from scratch (no Electron legacy)
- Use when you'd pick Electron but want a smaller, faster app

### Flutter Desktop — Best For:
- Teams already using Flutter for mobile
- Apps needing pixel-perfect, platform-adaptive UI
- When you want one codebase for iOS, Android, macOS, Windows, Linux
- Custom UI that doesn't look like a web page

## References

- Scenario: `scenarios/desktop-electron/`
- Scenario: `scenarios/desktop-tauri/`
- Scenario: `scenarios/desktop-flutter/`
- Rules: `rules/vibe-coding-desktop.mdc`
- Skills: `dart-flutter-patterns`, `dotnet-patterns`, `swiftui-patterns`
