---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-java-patterns
  name: java-patterns
  version: "1.1.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Modern Java 17+ — records, sealed types, pattern matching, streams, Spring Boot."
  category: language
  layer: null
  when_to_use: "Use when writing or reviewing Java 17+ code, modernizing legacy Java, or working in Spring Boot services."
---

# Java Patterns

## Level 1 — Intro

Modern Java leans on records, sealed types, pattern matching, and
streams. Prefer immutable data carriers, exhaustive switches, and
constructor injection over the Java-EE-era boilerplate.

## Level 2 — Overview

### Language features (17+)

Use `record` for immutable data carriers — you get `equals`,
`hashCode`, `toString` for free. Use `sealed` interfaces to restrict
hierarchies and unlock exhaustive `switch`. Use pattern matching
with `instanceof` to skip casts. Use text blocks (`"""..."""`) for
multi-line strings. Prefer `var` for locals when the right-hand
side makes the type obvious.

### Records and sealed classes

Records replace boilerplate DTOs. Validate in the compact
constructor:

```java
record Age(int value) {
    Age {
        if (value < 0) throw new IllegalArgumentException();
    }
}
```

Sealed hierarchies plus records create algebraic data types:

```java
sealed interface Result<T> permits Success, Failure {}
record Success<T>(T value) implements Result<T> {}
record Failure<T>(String error) implements Result<T> {}
```

Combined with pattern-matching `switch`, the compiler enforces
exhaustiveness — adding a variant breaks the build at every
consumer.

### Stream API

Use streams for transformations, not side effects. Prefer `toList()`
(Java 16+) over `Collectors.toList()`. The common pipeline is
`filter → map → collect`. Use `flatMap` to flatten nested
collections and `groupingBy`/`partitioningBy` for aggregation. Drop
back to a `for` loop when it reads more clearly than a stream.

### Optional

Return `Optional<T>` from methods that may not produce a result.
Never use `Optional` as a field or parameter type. Chain with `map`,
`flatMap`, and `filter` rather than `isPresent()` + `get()`. Use
`orElseThrow(() -> new NotFoundException(...))` for required values
and `Optional.empty()` instead of returning `null`.

### Spring Boot conventions

Use constructor injection, not field injection with `@Autowired`.
Keep controllers thin — validate input, delegate to service, return
a response. Put `@Transactional` on the service layer, not the
controller. Configure via `application.yml` with typed
`@ConfigurationProperties` classes and environment-specific
profiles. Return `ResponseEntity<T>` for explicit status codes and
centralize error handling in `@RestControllerAdvice`.

### Testing

Use JUnit 5 with `@DisplayName` for readable output. Use
`@ParameterizedTest` with `@CsvSource` or `@MethodSource` for
data-driven cases. Mock with `@Mock` and `@ExtendWith(MockitoExtension.class)`
rather than the legacy runner. Use AssertJ's fluent assertions
(`assertThat(result).isEqualTo(expected)`). Use Spring test slices
— `@WebMvcTest` for controllers, `@DataJpaTest` for repositories —
to keep tests fast.

## Level 3 — Full reference

### Dependency injection

Prefer constructor injection — it makes dependencies explicit and
enables testing without Spring. Inject interfaces, not concrete
implementations. Use `@Qualifier` or custom annotations to
disambiguate multiple beans. If a constructor has more than ~5
parameters, the class is probably doing too much — split it.

### Code organization

Package by feature (`com.app.order`, `com.app.user`), not by layer
(`com.app.controllers`, `com.app.services`). Keep one primary
responsibility per class. Mark classes and fields `final` when you
mean them to be immutable. Prefer composition and interfaces over
deep inheritance. For larger systems, use `module-info.java` to
enforce explicit module boundaries.

### Pattern matching switch

```java
String describe(Shape s) {
    return switch (s) {
        case Circle c    -> "circle r=" + c.radius();
        case Rectangle r -> "rect " + r.width() + "x" + r.height();
    };
}
```

With a sealed hierarchy, the compiler requires every permitted
type to be handled — no `default` branch needed.

### Anti-patterns

- Field injection with `@Autowired` — hides dependencies and
  requires reflection to test.
- `Optional` parameters or fields — use overloads or nullable with
  documentation instead.
- `.get()` on `Optional` without checking presence — use
  `orElseThrow`.
- Streams for trivial iteration where a `for` loop is clearer.
- Deep inheritance hierarchies of abstract classes — prefer
  composition and interfaces.
- Wide `@Transactional` annotations on controllers that cross
  business operations.
- `Collectors.toList()` on Java 16+ — use `toList()`.

### Common migrations

- POJO with getters/setters and equals/hashCode → `record`.
- Visitor pattern over an open hierarchy → sealed interface +
  pattern-matching switch.
- `if/else if` instanceof chains → pattern matching instanceof.
- Manual null-checks → `Optional` chains.
- Reflection-based DTO mappers between layers → records with
  explicit conversion methods.
