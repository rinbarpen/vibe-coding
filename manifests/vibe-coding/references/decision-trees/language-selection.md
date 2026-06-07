# Language Selection Decision Tree

Walk through these questions in order. Each answer narrows the options.

---

**Q1: Does it need to run in a browser (client-side)?**
```
Yes ──► TypeScript (the only browser-native option)
No  ──► Continue to Q2
```

**Q2: Is it performance-critical (microsecond latency, high throughput, or CPU-bound)?**
```
Yes ──► Continue to Q3
No  ──► Skip to Q4
```

**Q3: Is memory safety critical (no GC pauses, no use-after-free)?**
```
Yes ──► Rust
No  ──► Go (fast enough for most production workloads)
```

**Q4: Is it data science, ML/AI, or scientific computing?**
```
Yes ──► Python (dominant ecosystem, no real alternative)
No  ──► Continue to Q5
```

**Q5: Is it enterprise software with existing Java infrastructure?**
```
Yes ──► Java (Spring Boot, existing investments, talent pool)
No  ──► Continue to Q6
```

**Q6: What kind of application?**
```
Web / API backend:
  Go (preferred — fast, simple, great stdlib)
  TypeScript (if full-stack same-language team)
  Python (if ML-serving or rapid prototyping)
  Java (if existing enterprise investment)

CLI / dev tool:
  Go (fast compile, single binary, cross-compile)
  Rust (if maximum performance needed)
  TypeScript (if npm ecosystem integration)

Mobile:
  Kotlin/Swift (native) or TypeScript (React Native/Expo)
  (Go/Rust/Python/Java are not recommended for mobile UI)

	Desktop:
	  Electron (TypeScript) — if web UI and full Node.js access needed
	  Tauri (TypeScript + Rust) — if minimal binary + best performance
	  Flutter Desktop (Dart) — if mobile codebase sharing
	  .NET MAUI (C#) — if Windows-only or existing .NET team
```

**Q7: Team expertise and project constraints**
```
Match the language to team strength, BUT:
- Don't use Python for a high-throughput API when Go is clearly better
- Don't use Rust for a simple CRUD when Go is faster to develop
- Don't use Java for a CLI tool when Go produces a smaller binary
- Don't use TypeScript for CPU-heavy backend processing
After all the technical analysis, the best language is the one your team can ship reliably.
```

---

## Quick Reference Matrix

| Requirement | Go | Rust | Python | TypeScript | Java |
|-------------|:--:|:----:|:------:|:----------:|:----:|
| Web Backend | ★★★ | ★★ | ★★ | ★★★ | ★★★ |
| Web Frontend | — | — | — | ★★★ | — |
| CLI Tool | ★★★ | ★★★ | ★ | ★★ | ★ |
| Systems Programming | ★ | ★★★ | — | — | — |
| ML/AI / Data Science | — | ★ | ★★★ | ★ | ★ |
| Enterprise Large-Scale | ★ | — | — | — | ★★★ |
| Microservices | ★★★ | ★★ | ★ | ★★ | ★★★ |
| Rapid Prototyping | ★ | — | ★★★ | ★★★ | — |
| Mobile (cross-platform) | — | — | — | ★★★ | ★★ |
| Cloud / Serverless | ★★★ | ★ | ★★ | ★★★ | ★ |
| Real-time / WebSocket | ★★★ | ★★★ | ★ | ★★★ | ★★ |
| Game Development | ★ | ★★★ | ★ | ★★ | ★★ |
| Desktop App | ★ | ★★ | — | ★★ | ★ |

★★★ = excellent fit, ★★ = good fit, ★ = possible, — = not recommended

---

## Multi-Language Project Guidance

When the same project uses multiple languages, use this pattern:

| Component | Recommended Language | Why |
|-----------|---------------------|-----|
| Web frontend | TypeScript | Only browser option |
| BFF (Backend for Frontend) | TypeScript | Same-language service layer |
| Core API services | Go | Fast, reliable, easy to operate |
| Performance-critical services | Rust | Zero-cost abstractions, no GC |
| ML inference serving | Python | ML ecosystem, model loading |
| Batch data processing | Python or Go | pandas for analysis, Go for throughput |
| CLI tooling | Go | Single binary distribution |
| Infrastructure / operators | Go | CNCF ecosystem standard |
| Data pipeline orchestration | Python | Airflow, Prefect, Dagster |
| Enterprise integration layer | Java | Existing middleware ecosystem |
| Desktop app (Electron) | TypeScript | Mature web UI + Node.js ecosystem |
| Desktop app (Tauri) | TypeScript + Rust | Minimal binary, best performance |
| Desktop app (Flutter) | Dart | Shared mobile+desktop Dart code |
