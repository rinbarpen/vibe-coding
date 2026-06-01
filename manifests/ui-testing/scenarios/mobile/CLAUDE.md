# Mobile UI Testing Scenario

## Context

You are writing mobile UI tests for native or hybrid mobile applications. These tests run on physical devices, emulators, or simulators.

## Key Conventions

- **Framework**: Detox (React Native) or Appium (cross-platform)
- **Device management**: Tests run against a single device type per shard
- **Gestures**: Swipe, scroll, long-press — use framework gesture APIs
- **Test data**: Pre-seeded through API or database

## Commands

```bash
# Detox
detox test --configuration ios.sim.release   # iOS simulator
detox test --configuration android.emu.release # Android emulator

# Appium
appium --address 0.0.0.0 --port 4723          # Start Appium server
```

## Rules

See `rules/ui-testing-mobile.mdc` for detailed rules.
