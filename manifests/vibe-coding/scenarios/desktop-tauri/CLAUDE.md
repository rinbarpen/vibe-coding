# CLAUDE.md — Desktop Tauri Scenario

## Architecture

- **UI**: React / Vue / Svelte + Vite
- **Backend**: Rust (Tauri API + custom commands)
- **Packaging**: Tauri Bundler (.dmg / .msi / .deb)
- **Auto-update**: @tauri-apps/plugin-updater

## Commands

| Command | Description |
|---------|-------------|
| `pnpm tauri dev` | Start Tauri dev (Vite + Rust) |
| `pnpm tauri build` | Production build + package all platforms |
| `cargo test` | Run Rust backend tests |
| `pnpm lint` | Lint web frontend |
| `cargo clippy` | Lint Rust backend |
| `/desktop-build` | Cross-platform build & package |

## Development Standards

- Rust safety: no `unsafe` unless reviewed and documented.
- IPC: frontend `invoke` → Rust command handlers. No direct FS/OS from UI.
- File system: scoped to `app_data_dir` and `app_config_dir`.
- Permissions: `tauri.conf.json > capabilities` — minimum required per window.

## Key Directories

- `src/` — Web UI frontend
- `src-tauri/src/` — Rust Tauri commands and logic
- `src-tauri/tauri.conf.json` — App config, windows, bundle settings
- `src-tauri/icons/` — Platform app icons
- `src-tauri/capabilities/` — Permission capabilities
