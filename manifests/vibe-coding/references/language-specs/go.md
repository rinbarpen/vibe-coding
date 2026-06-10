# Go Language Specification

## Overview
Compiled, statically typed language with first-class concurrency. Designed by Google for network services and cloud infrastructure. Fast compilation, single-binary deployment, excellent standard library.

## Strengths
- Fast compilation and startup (single binary, no runtime dependency)
- Built-in concurrency (goroutines are lightweight, channels for CSP-style communication)
- Rich standard library (HTTP server, crypto, JSON, SQL database/sql)
- Excellent tooling (gofmt, go vet, staticcheck, race detector, pprof)
- Cross-compilation is trivial (GOOS/GOARCH environment variables)
- Strong backward compatibility guarantee

## Weaknesses
- Verbose error handling (`if err != nil` pattern required everywhere)
- Limited generics (Go 1.18+ improved this but ergonomics still evolving)
- No sum types or pattern matching
- GC pauses matter in latency-sensitive workloads (< 1ms typical but unpredictable)
- Smaller ecosystem for ML/data science compared to Python
- No built-in dependency injection (rely on constructor functions or wire)

## Best For
- Backend microservices and API servers (HTTP/gRPC)
- CLI tools and DevOps tooling (single binary, fast startup)
- Network proxies, gateways, load balancers
- Concurrent data processing pipelines
- Cloud-native infrastructure (Kubernetes operators, CNCF ecosystem)
- Database proxies and caching layers

## Not Ideal For
- Complex GUI applications (no mature native GUI framework)
- Game engines or real-time graphics (GC overhead)
- Data science / ML training pipelines (use Python)
- Memory-unsafe low-level systems (use Rust — no `unsafe` footguns)
- Rapid prototyping with dynamic typing (use Python/TypeScript)

## Testing
- Framework: `go test` (built-in, no external test framework needed)
- Style: Table-driven tests (define test cases as struct slices)
- Assertions: `testify/assert` or `testify/require` for richer assertions
- HTTP: `httptest` package for handler/server testing
- Race detection: `go test -race` (mandatory for concurrent code)
- Coverage: `go test -coverprofile=coverage.out && go tool cover -html=coverage.out`
- Fuzzing: Built-in `go test -fuzz` (Go 1.18+)
- Mocking: `mockgen` from uber-go/mock or testify/mock
- Skills: `golang-testing`, `golang-patterns`

## Key Libraries
- Standard library is extensive (http, json, crypto, sql, net, os, io, context)
- Routing: `chi` (lightweight, idiomatic) or standard `net/http` (Go 1.22+ with method patterns)
- Database: `sqlc` (type-safe SQL generation) or `sqlx` (ergonomic SQL extensions)
- CLI: `cobra` + `viper` (CLI framework + config management)
- Dependency injection: `wire` (compile-time DI)
- Logging: `slog` (built-in, structured, leveled)
- Task coordination: `errgroup` (from golang.org/x/sync)
- Testing: `testify`, `gomock`

## Concurrency Model
- **Goroutines**: Lightweight threads (2-4KB stack, millions possible per process)
- **Channels**: Typed conduits for CSP-style communication (`chan T`, `chan<- T`, `<-chan T`)
- **Context**: Carry deadlines, cancellation signals, and request-scoped values
- **sync.WaitGroup**: Coordinate goroutine completion
- **errgroup**: Propagate errors across goroutines
- **sync.Pool**: Object pooling for high-throughput allocation-heavy workloads
- Rule: "Do not communicate by sharing memory; instead, share memory by communicating."

## References
- Skills: `golang-patterns`, `golang-testing`
- Agents: `go-reviewer`, `go-build-resolver`
- Rules: `~/.claude/rules/golang/`
- Agents: `go-reviewer`, `go-build-resolver`
