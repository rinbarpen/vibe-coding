# CLAUDE.md — Desktop Electron Scenario

## Architecture

- **UI**: React / Vue / Svelte + Vite
- **Main process**: Electron + TypeScript
- **Packaging**: electron-builder / electron-forge
- **Auto-update**: electron-updater (GitHub Releases)

## Commands

| Command | Description |
|---------|-------------|
| `pnpm dev` | Start Electron dev (Vite + Electron) |
| `pnpm build` | Production build + package for current platform |
| `pnpm build:mac` | Build macOS (.dmg) |
| `pnpm build:win` | Build Windows (.exe/.msi) |
| `pnpm build:linux` | Build Linux (.deb/.AppImage) |
| `pnpm lint` | Lint + type check |
| `pnpm test` | Run tests |
| `/desktop-build` | Cross-platform build & package |

## Development Standards

- `contextIsolation: true`, `sandbox: true`, `nodeIntegration: false` — always.
- IPC: `contextBridge` + `ipcRenderer.invoke` only. No `remote` module.
- CSP headers in production. `webPreferences.preload` for preload-only scripts.
- File system access limited to `app.getPath('userData')`.

## Key Directories

- `src/main/` — Electron main process
- `src/preload/` — Preload scripts (bridge)
- `src/renderer/` — Renderer process UI
- `build/` — Packaging config (electron-builder.yml)
- `resources/` — App icons (.icns, .ico, .png)
