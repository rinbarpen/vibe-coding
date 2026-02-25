# CLAUDE.md

## Architecture
- Shared Logic: `src/shared`
- Web: React/Next.js
- Mobile: Flutter/React Native
- API: OpenAPI/Swagger defined

## Cross-Platform Commands
| Command | Description |
|---------|-------------|
| `vibe-sync-types` | Sync types across platforms |
| `flutter run` | Run mobile app |
| `pnpm dev` | Run web app |

## API Consistency
- Use generated SDKs for all platforms.
- Unified response format.
