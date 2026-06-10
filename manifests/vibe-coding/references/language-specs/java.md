# Java Language Specification

## Overview
Statically typed, object-oriented language running on the Java Virtual Machine (JVM). The backbone of enterprise software for over two decades, Java combines mature ecosystem stability with modern language features through rapid release cadence (Java 21+).

## Strengths
- Battle-tested JVM with excellent runtime performance (JIT compilation, adaptive optimization, tiered compilation)
- Huge mature ecosystem (Spring, Hibernate, Apache projects, Micronaut, Quarkus)
- Strong typing and excellent IDE support (IntelliJ IDEA is the gold standard for refactoring)
- Virtual threads (Project Loom, Java 21+) — lightweight, millions of concurrent threads
- Backward compatibility is a first-class concern (Java 21 can run code written for Java 8)
- Rich observability (JMX, JFR, JMC, OpenTelemetry integration)
- GraalVM native-image for fast startup and low memory (good fit for serverless)
- Massive talent pool and enterprise adoption

## Weaknesses
- Verbose syntax compared to Go, Rust, Python (mitigated by records, Lombok, and modern features)
- High memory footprint (JVM base overhead 64-128MB, heap grows aggressively)
- Slow startup time (seconds vs milliseconds for Go — mitigated by GraalVM native-image)
- Heavy framework culture (Spring Boot can be overbearing for small projects)
- Old-style patterns still common in the ecosystem (XML config, checked exceptions, heavy inheritance)
- Package management less modern than cargo/go mod (Maven is XML-heavy; Gradle is better but complex)
- Java-to-JavaScript interop is not seamless (compared to TypeScript)

## Best For
- Enterprise backend services (banks, insurance, government, healthcare)
- Large-scale distributed systems (Kafka, Elasticsearch, Cassandra, Hadoop — all JVM-based)
- Android application development (Android SDK uses Java/Kotlin)
- Systems requiring proven stability and long-term support (decade+ maintenance)
- Microservices with Spring Boot (industry-standard enterprise patterns)
- Big data processing (Apache Spark, Flink, Hadoop ecosystem)
- High-throughput, latency-tolerant services with established infrastructure

## Not Ideal For
- Rapid prototyping (verbosity slows iteration — use Python or TypeScript)
- CLI tools (Go produces smaller binaries faster)
- Frontend web development (use TypeScript — Java applets are dead)
- Systems programming (use Rust or C++)
- Small, simple services where startup time matters (Go or TypeScript)
- Projects where minimal memory footprint is critical (Rust or C)

## Testing
- Unit: `JUnit 5` (Jupiter) with `@Test`, `@ParameterizedTest`, `@RepeatedTest`
- Mocking: `Mockito` (industry standard, with MockitoExtension for JUnit 5)
- Integration: `TestContainers` (Docker-based, throwaway instances of databases/middleware)
- Assertions: `AssertJ` (fluent assertions, rich error messages)
- Coverage: `JaCoCo` (integrated with Maven/Gradle, 80%+ threshold via `jacoco-maven-plugin`)
- BDD: `Cucumber` (Gherkin syntax, used in enterprise)
- ArchUnit: `com.tngtech.archunit` (enforce architectural rules programmatically)
- Performance: JUnit 5 + JFR (Java Flight Recorder) for profiling in tests
- Lint: `SpotBugs` (findbugs successor), `PMD`, `checkstyle`
- Build: `Maven` (XML, conventional) or `Gradle` (Groovy/Kotlin DSL, more flexible)
- Skills: Java standards in `java-coding-standards`

## Key Libraries
- Web framework: `Spring Boot 3+` (industry standard, auto-configuration, massive ecosystem)
- Lighter alternatives: `Micronaut` (compile-time DI, fast startup), `Quarkus` (Kubernetes-native)
- ORM: `JPA` / `Hibernate` (standard ORM, cache, lazy-loading, schema generation)
- Database migration: `Flyway` or `Liquibase` (version-controlled SQL migrations)
- DTO mapping: `MapStruct` (compile-time code generation, no reflection)
- JSON: `Jackson` or `JSON-B` (serialization/deserialization)
- Validation: `Jakarta Bean Validation` with Hibernate Validator
- Reactive: `Project Reactor` (reactive streams, used with WebFlux)
- Testing: `JUnit 5`, `Mockito`, `AssertJ`, `TestContainers`
- Build: `Maven` or `Gradle`

## Modern Java Features (Java 17+)

| Feature | What It Replaces | Motivation |
|---------|------------------|------------|
| `record` Foo(...) | Boilerplate POJO | Concise data carriers, equals/hashCode/toString auto-generated |
| `sealed` class | Restrictive inheritance | Exhaustive pattern matching, closed hierarchies |
| `switch` expression | `if-else` chains | Exhaustive, returns value, no fall-through |
| Pattern matching `instanceof` | Cast + instanceof | Destructuring without manual casting |
| Text blocks `"""` | String concatenation | Multi-line strings without escaping |
| Virtual threads (21+) | Platform threads | Million+ threads, simple synchronous code |
| `StringTemplate` (21+) | String.format() | Safe interpolation (preview) |
| Sequenced collections (21+) | Sorted/linked quirks | Unified first/last/reversed access |

Prefer these modern constructs over legacy Java patterns. If the project requires Java 8 compatibility (Android, legacy enterprise), note which features are unavailable.

## References
- Skills: `java-coding-standards`, `jpa-patterns`
- Agents: `java-reviewer`, `java-build-resolver`
- Rules: `~/.claude/rules/java/`
