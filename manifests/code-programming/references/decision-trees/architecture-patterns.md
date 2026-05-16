# Architecture Patterns

## Monolith

A single deployable unit containing all application logic.

- **When to use**: Small team, early-stage product, low operational complexity
- **When not to use**: Team > 10, independent deployability needed, different scaling requirements per component
- **Best languages**: Go (simple HTTP server), Python (FastAPI), TypeScript (Next.js full-stack), Java (Spring Boot)
- **Gotchas**: Resist the urge to microservice too early. A well-structured monolith (with clear module boundaries) can be extracted into services later.

## Microservices

Independent services communicating over the network, each owning its data.

- **When to use**: Large team, independent deployability, polyglot requirements, different scaling needs
- **When not to use**: Small team, simple CRUD, no independent deployability need
- **Best languages**: Go (preferred for new services), Java (existing enterprise), Rust (perf-critical services)
- **Service mesh**: Consider Istio or Linkerd for observability, traffic management, and security
- **Gotchas**: Network latency, distributed transactions, eventual consistency complexity, operational overhead

## Event-Driven Architecture

Services communicate through asynchronous events via a message broker.

- **When to use**: Loose coupling, async processing, audit trails, multi-system propagation
- **When not to use**: Simple request-reply patterns, strong consistency requirements (without compensating actions)
- **Best languages**: Go with NATS/Kafka, Python with Kafka/RabbitMQ, TypeScript with RabbitMQ
- **Broker options**: Kafka (high throughput, replay), NATS (low latency, simple), RabbitMQ (flexible routing), Redpanda (Kafka-compatible, faster)
- **Patterns**: Event sourcing, CQRS, saga (choreography or orchestration)
- **Gotchas**: Exactly-once semantics are hard, event schema evolution, debugging async flows

## Layered Architecture (N-Tier)

Separation into layers: presentation → business logic → data access.

- **When to use**: Standard CRUD applications, enterprise line-of-business apps
- **When not to use**: Complex domains where the "business logic layer" becomes a god object
- **Best languages**: Any, but Java/Spring Boot and Python/Django are most common
- **Gotchas**: The "sinkhole anti-pattern" (layers that just pass data through without transformation). If every layer is just forwarding, the layers are unnecessary.

## Hexagonal Architecture (Ports & Adapters)

Core business logic is isolated from external concerns (database, API, UI) through ports (interfaces) and adapters (implementations).

- **When to use**: Complex business logic, high testability requirement, DDD, need to swap infrastructure
- **When not to use**: Simple CRUD (overkill — the abstraction overhead isn't justified)
- **Best languages**: Java (Spring + hexagonal is well-established), Go (interface-driven design), Rust (trait-based)
- **Gotchas**: More code (interfaces + implementations + wiring), can tempt premature abstraction

## CQRS (Command Query Responsibility Segregation)

Separate read models from write models. Queries go through optimized read stores; commands go through the write store.

- **When to use**: Read-write disparity (many more reads than writes, or complex read queries), different data shapes for reads vs writes
- **When not to use**: CRUD where read and write models are identical (you're just adding layers)
- **Best languages**: Go or Java for the command side; TypeScript or Rust for optimized read APIs
- **Gotchas**: Eventual consistency (read store lags write store), operational complexity of maintaining two stores

## Event Sourcing

Store state as a sequence of events. Current state is derived by replaying events.

- **When to use**: Audit trails, temporal queries, complex state transitions, undo/redo
- **When not to use**: Simple CRUD, high query performance needs without snapshot optimization
- **Best languages**: Go (event processing at scale), Java (Axon Framework), Rust (low-latency event processing)
- **Gotchas**: Schema evolution of events over time, replay performance, event store operational complexity

---

## Language Suitability Per Pattern

| Pattern | Go | Rust | Python | TypeScript | Java |
|---------|:--:|:----:|:------:|:----------:|:----:|
| Monolith | ★★★ | ★★ | ★★★ | ★★★ | ★★★ |
| Microservices | ★★★ | ★★★ | ★★ | ★★★ | ★★★ |
| Event-Driven | ★★★ | ★★★ | ★★ | ★★ | ★★★ |
| Layered (N-Tier) | ★★ | ★ | ★★★ | ★★★ | ★★★ |
| Hexagonal | ★★★ | ★★★ | ★ | ★★ | ★★★ |
| CQRS | ★★★ | ★★★ | ★ | ★ | ★★★ |
| Event Sourcing | ★★★ | ★★★ | ★ | ★ | ★★★ |

## Decision Flow

```
How many developers?
├── 1-5 developers ──► Monolith (extract to services later as team grows)
├── 5-20 developers ──► Microservices or Modular Monolith
│                        ├── Clear service boundaries? ──► Microservices
│                        └── Still exploring ──► Modular Monolith
└── 20+ developers ──► Microservices (enforced by org structure / Conway's Law)

How complex is the domain?
├── Simple CRUD ──► Layered (N-Tier) is fine
├── Complex business logic ──► Hexagonal + DDD
└── Complex state + audit trail ──► Event Sourcing + CQRS

Do reads and writes have different characteristics?
├── Same shape + volume ──► Standard pattern is fine
├── Different shape or volume ──► Consider CQRS (can be introduced per-use-case, not globally)
└── Need full audit trail ──► Event Sourcing + CQRS

What are the consistency requirements?
├── Strong consistency needed everywhere ──► Avoid event-driven; prefer sync patterns
├── Some eventual consistency acceptable ──► Event-driven is flexible
└── Mixed ──► CQRS with strong consistency on writes, eventual on reads
```
