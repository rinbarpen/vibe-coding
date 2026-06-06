# Rust Language Specification

## Overview
Systems programming language focused on safety, speed, and concurrency. Memory safety without garbage collection enforced at compile time through ownership and borrowing. Zero-cost abstractions with a rich type system.

## Strengths
- Memory safety without GC (ownership + borrowing guarantees no use-after-free, double-free, data races)
- Zero-cost abstractions (high-level constructs compile down to efficient machine code)
- Excellent performance (comparable to C/C++)
- Rich type system (algebraic data types, pattern matching, traits with generics, enums with payloads)
- Best-in-class tooling (cargo build/test/doc/clippy/fmt, crates.io, rustup for toolchain management)
- Fearless concurrency (Send + Sync traits enforce thread-safety at compile time)
- WebAssembly as a first-class compilation target

## Weaknesses
- Steep learning curve (borrow checker, lifetimes, ownership model requires mental shift)
- Long compile times (mitigated by incremental compilation, sccache, mold linker)
- Async runtime fragmentation (tokio vs async-std vs smol — tokio is the defacto standard)
- Smaller ecosystem than Go or Python for web service libraries
- Overkill for simple CRUD services (Go or Python would be faster to develop)
- Binary size can be large (mitigated by `strip` and LTO)

## Best For
- Systems programming (OS kernels, device drivers, embedded systems)
- Performance-critical services (databases, message brokers, proxies, load balancers)
- WebAssembly (compiling to WASM for browser or server-side)
- CLI tools where performance matters (bat, ripgrep, fd, delta — all written in Rust)
- Cryptography and security-critical software (no memory safety vulnerabilities)
- Network services requiring low latency and predictable performance (no GC pauses)
- Embedded systems and IoT (no_std support)

## Not Ideal For
- Rapid prototyping (borrow checker slows iteration — use Python/TypeScript)
- Simple CRUD backends (Go or Python are faster to develop)
- Data science / ML training (use Python — though Rust is gaining ground via burn, candle)
- Teams new to systems programming (learning curve impacts velocity)
- Projects where compile speed matters (C++ or Go compile faster)

## Testing
- Framework: Built-in `#[test]` attribute with `#[cfg(test)]` modules
- Parameterized: `rstest` crate for test case matrices
- Property-based: `proptest` or `quickcheck` for randomized testing
- Mocking: `mockall` for trait-based mocking (generate mock implementations from trait definitions)
- Async: `tokio::test` for testing async code
- Doc-tests: `/// ``` ` code blocks in documentation (tested by `cargo test`)
- Coverage: `cargo-llvm-cov` (LLVM-based coverage instrumentation)
- Lint: `cargo clippy -- -D warnings`
- Fuzzing: `cargo-fuzz` (libFuzzer integration)
- Skills: `rust-testing`, `rust-patterns`

## Key Libraries
- Async runtime: `tokio` (defacto standard), `hyper` (HTTP), `axum` or `actix-web` (web framework)
- Serialization: `serde` with `serde_json`, `serde_yaml` (derive-based, zero-config)
- Database: `sqlx` (compile-time checked SQL) or `diesel` (ORM-like, schema-first)
- CLI: `clap` (derive-based argument parsing) or `structopt` (merged into clap v3)
- Error handling: `thiserror` (library errors), `anyhow` (application errors)
- Logging: `tracing` (structured, async-aware, with spans)
- HTTP client: `reqwest`
- Date/time: `chrono`

## Ownership Model
- Every value in Rust has exactly **one owner** at any time
- `let x = vec![1, 2, 3]; let y = x;` — ownership of the Vec moves to y, x is invalidated
- **Borrowing**: `&T` (immutable reference), `&mut T` (mutable reference, exclusive)
- Rule: at any time, you can have either one mutable reference OR any number of immutable references
- References must never outlive their referents (lifetime checking)
- `Rc<T>` / `Arc<T>` for shared ownership (reference-counted, Arc is thread-safe)
- `Cow<T>` for copy-on-write (borrowed or owned depending on mutation)

## References
- Skills: `rust-patterns`, `rust-testing`
- Agents: `rust-reviewer`, `rust-build-resolver`
- Rules: `~/.claude/rules/rust/`
