# ADR-0013 — Runtime Foundation

| Field | Value |
| --- | --- |
| ID | ADR-0013 |
| Title | Runtime Foundation |
| Status | Draft — Pending Architectural Review |
| Date | 2026-07-07 |
| Authority | [GAR-0019](../../GAR-0019.md) — External Capability Expansion Constitutional Extension — Second Derivation |
| Epoch | External Capability Expansion (continued) |
| Depends on | ADR-0012, ADR-0011, ADR-0002 |
| Supersedes | None |

---

## Decision

Project Garuda shall establish a **Runtime Foundation** as the architectural realization of
**External Runtime Governance** authorized by GAR-0019.

The Runtime Foundation shall govern the architectural description of how external-facing runtime
contexts are classified, bounded, contractually governed, and related as runtime participants
**through** the Integration Foundation and Constitutional Membrane — without Operational Runtime,
transport, orchestration, or provider implementation.

The Runtime Foundation is an architectural layer. It is not:

- a runtime execution engine,
- an orchestration engine,
- a transport layer,
- a provider implementation,
- a substitute for the Interface Foundation, Constitutional Membrane, or Integration Foundation,
- an integration participant classifier,
- a scheduling system,
- a cognitive foundation,
- or the Universal Execution Foundation.

All runtime architecture SHALL traverse the Integration Foundation and Interface Foundation. No
runtime pathway SHALL bypass the lawful external-capability stack.

---

## Context

GAR-0019 ratified the second external-capability expansion following completion of the Integration
Foundation at release `v0.11.0-alpha`.

GAR-0018 authorized the Integration Foundation as the first external-capability expansion beyond the
Interface Foundation (ADR-0012). The Integration Foundation governs **External Integration** — how
External Systems are described, classified, related, and governed as integration participants through
the membrane, without operational behavior.

GAR-0019 derived **External Runtime Governance** as the only admissible second external-capability
domain. The constitutional gap addressed by this ADR is **runtime context architecture** — how
external-facing runtime contexts are described, bounded, and governed as runtime participants through
the Integration and Interface stack, without Operational Runtime.

This ADR records the architectural decision subordinate to GAR-0019. It does not create
constitutional authority. Sprint specifications and implementation remain downstream.

### Constitutional Tripartite Distinction

This ADR preserves the constitutionally required distinction among three concepts that SHALL NOT be
conflated in architecture, sprint specifications, or implementation:

| Concept | Layer | Meaning |
| --- | --- | --- |
| **External Runtime Governance** | External-capability (Phase II stack) | Descriptive runtime context architecture authorized by GAR-0019 and realized by this ADR |
| **Operational Runtime** | Not authorized | Execution engines, invocation, scheduling, operational state transitions — explicitly outside constitutional authority |
| **Universal Execution Foundation** | Phase I cognitive | Internal cognitive execution descriptions under ADR authority for `packages.execution` — constitutionally distinct from External Runtime Governance |

Every architectural principle in this ADR applies only to **External Runtime Governance**.

---

## Architectural Decision

The Runtime Foundation shall realize External Runtime Governance through the following architectural
principles.

**ADR-0013-P01 — Stack Traversal**  
All runtime architecture SHALL occur through the Integration Foundation and Interface Foundation.
External-facing runtime contexts SHALL NOT be modeled by bypassing, duplicating, or weakening the
Integration Foundation, Interface Foundation, or Constitutional Membrane.

**ADR-0013-P02 — Subordination to Integration and Interface Contracts**  
Runtime contracts, classifications, and boundary semantics SHALL be subordinate to integration
contracts and canonical interface contracts established by the Integration and Interface Foundations.
Runtime architecture SHALL NOT supersede or replace integration participant semantics or membrane
communication semantics.

**ADR-0013-P03 — Descriptive Runtime Model**  
The Runtime Foundation SHALL govern architectural **description** only — runtime context
classification, boundary semantics, runtime contract governance, lifecycle and boundary metadata,
and descriptive catalog semantics. It SHALL NOT perform Operational Runtime execution, runtime
invocation, scheduling, operational state transitions, connectivity, message delivery, or provider
invocation.

**ADR-0013-P04 — Technology Neutrality**  
The Runtime Foundation SHALL remain independent of all external technologies. No architectural
decision within the Runtime Foundation SHALL require a specific protocol, provider, infrastructure
component, runtime environment, or execution engine.

**ADR-0013-P05 — Runtime Context Classification**  
External-facing runtime contexts participating in Garuda runtime architecture SHALL be represented
through deterministic, technology-neutral classification semantics governed by the Runtime
Foundation. Classification SHALL be descriptive and SHALL NOT embed provider-specific identity,
operational credentials, or execution engine bindings.

**ADR-0013-P06 — Cognitive Independence**  
The Internal Cognitive Foundations SHALL remain unaware of External Systems, integration
participants, and external-facing runtime contexts. Runtime architecture SHALL NOT introduce
cognitive dependencies or external knowledge into Phase I foundations.

**ADR-0013-P07 — Variability Termination**  
Architectural variability introduced by External Systems, integration participants, and
external-facing runtime contexts SHALL terminate at the Runtime Foundation (and upstream at the
Integration and Interface Foundations). No runtime variability SHALL propagate into Internal Cognitive
Foundations.

**ADR-0013-P08 — Platform Core Inheritance**  
Every runtime artifact authorized by this ADR SHALL derive from the Platform Core object model
established by ADR-0002. The Runtime Foundation SHALL NOT establish an independent object hierarchy.

**ADR-0013-P09 — Integration Foundation Dependency**  
The Runtime Foundation SHALL depend upon the Integration Foundation. It SHALL consume integration
participant semantics, integration contracts, and lawful stack context. It SHALL NOT modify the
Integration Foundation.

**ADR-0013-P10 — Interface Foundation Dependency**  
The Runtime Foundation SHALL depend upon the Interface Foundation through lawful stack traversal. It
SHALL respect canonical interface contracts and membrane semantics. It SHALL NOT modify the Interface
Foundation.

**ADR-0013-P11 — Universal Execution Foundation Separation**  
The Runtime Foundation SHALL NOT conflate External Runtime Governance with the Phase I Universal
Execution Foundation. Cognitive execution descriptions remain exclusively within Phase I execution
semantics. External-facing runtime context descriptions remain exclusively within Runtime Foundation
semantics. No runtime artifact SHALL substitute for, extend, or reclassify Universal Execution
Foundation objects.

**ADR-0013-P12 — Operational Runtime Exclusion**  
The Runtime Foundation SHALL NOT implement, simulate, or architecturally imply Operational Runtime.
Descriptive runtime governance is the sole authorized scope. Execution engines, scheduling systems,
runtime invocation semantics, and operational state transition engines remain outside architectural
authority until separately authorized by future constitutional law.

---

## Rationale

This architecture preserves the constitutional derivation established by GAR-0019 while maintaining
membrane supremacy, stack traversal, cognitive independence, and additive evolution guarantees of
GAR-0018, GAR-0017, ADR-0012, and ADR-0011.

By governing external-facing runtime contexts descriptively and subordinately to integration and
interface contracts, Garuda ensures that runtime context architecture can be modeled, certified, and
evolved without introducing Operational Runtime, transport, or provider coupling into the
external-capability stack or cognitive core.

The Runtime Foundation extends external-capability governance without redefining the Integration
Foundation, Interface Foundation, Universal Execution Foundation, or any other Internal Cognitive
Foundation.

---

## Alternatives Considered

| Alternative | Description |
| --- | --- |
| Operational runtime layer | Rejected |
| Orchestration layer at Runtime Foundation | Rejected |
| Conflation with Universal Execution Foundation | Rejected |
| Provider-specific runtime architecture | Rejected |
| Runtime bypassing Integration Foundation | Rejected |
| Merging runtime into Integration Foundation | Rejected |
| Independent Runtime object hierarchy | Rejected |

### Why Rejected

**Operational runtime layer** — Violates GAR-0019 Principle Descriptive Before Operational (Article V
§3), Article VI §2, and Article IX §5. Operational Runtime is explicitly excluded from constitutional
authority.

**Orchestration layer at Runtime Foundation** — Violates GAR-0019 Article VI §2 and Article IX §5.
Orchestration remains deferred to future independent constitutional authority.

**Conflation with Universal Execution Foundation** — Violates GAR-0019 Article V §11, Article VIII
§2, and Article IX §5. Phase I cognitive execution and external runtime governance are
constitutionally distinct domains.

**Provider-specific runtime** — Violates GAR-0019 technology neutrality (Article V §4) and Article VI
§2. ADR-0012 and ADR-0011 rejected provider-specific patterns.

**Runtime bypassing Integration Foundation** — Violates GAR-0019 stack traversal (Article V §9),
membrane supremacy (Article V §1), and Article X §4.

**Merging into Integration Foundation** — Violates GAR-0019 derivation; Integration Foundation is
complete and immutable; External Runtime Governance is a distinct external-capability class derived
in Article VII §3.

**Independent object hierarchy** — Violates Platform Core inheritance (ADR-0002, ADR-0012-P08).

---

## Consequences

### Positive

- Realizes GAR-0019 External Runtime Governance authorization architecturally
- Preserves lawful external-capability stack order (Interface → Integration → Runtime)
- Maintains technology neutrality and additive evolution
- Establishes descriptive runtime governance subordinate to integration and interface contracts
- Preserves tripartite distinction among External Runtime Governance, Operational Runtime, and
  Universal Execution Foundation
- Enables sprint-level specification without constitutional ambiguity

### Negative

- Every external-facing runtime context requires architectural normalization through Interface,
  Integration, and Runtime layers
- Operational Runtime, orchestration, transport, and provider implementation remain deferred to
  future constitutional authority
- Runtime artifacts must conform to Platform Core, Interface Foundation, and Integration Foundation
  constraints
- Engineers must maintain explicit separation from Universal Execution Foundation semantics

---

## Architectural Invariants

The following invariants are established by this ADR:

1. Runtime architecture traverses the Integration Foundation and Interface Foundation exclusively.
2. Runtime contracts are subordinate to integration contracts and canonical interface contracts.
3. Runtime artifacts inherit Platform Core.
4. Internal Cognitive Foundations remain unaware of external-facing runtime contexts.
5. Runtime variability terminates at the Runtime Foundation.
6. Runtime Foundation introduces no provider-specific or Operational Runtime behavior.
7. The Runtime Foundation remains additive and does not modify Phase I, Interface, or Integration
   foundations.
8. The Runtime Foundation depends upon the Integration Foundation and Interface Foundation.
9. External Runtime Governance SHALL NOT be conflated with Universal Execution Foundation.
10. Operational Runtime SHALL NOT be introduced, simulated, or implied by Runtime Foundation
    architecture.

---

## Deferred Decisions

The following are intentionally deferred to GAR-SPRINT-0012 and its mission specifications:

- Runtime context model design
- Runtime contract architecture
- Runtime classification taxonomy
- Runtime boundary semantics
- Runtime lifecycle and boundary model
- Runtime registry or catalog architecture
- Certification scenarios
- Runtime certification methodology (Golf) — deferred to GAR-SPRINT-0012 and subsequent certification activities
- Repository layout and package structure
- Sprint mission decomposition
- Testing strategy
- Implementation details

These topics belong to the approved sprint specification, not to this ADR.

---

## Constitutional Traceability

Every architectural decision in this ADR derives from ratified GAR-0019. This appendix provides the
constitutional audit trail from law to architecture. No ADR provision creates constitutional authority.

### Decision statement

| ADR provision | Constitutional source |
| --- | --- |
| Establish Runtime Foundation | GAR-0019 Article IX §2 — Foundation Authorization |
| External Runtime Governance definition | GAR-0019 Article IX §1 — External Runtime Governance |
| Govern runtime contexts through Integration and membrane | GAR-0019 Article V §9; Article VI §4; Article IX §3 |
| Without Operational Runtime, transport, orchestration, provider | GAR-0019 Article V §3; Article VI §2; Article VIII §2 |
| Not a runtime execution engine | GAR-0019 Article IX §5; Article VI §2 |
| Not an orchestration engine | GAR-0019 Article IX §5; Article VI §2 |
| Not a transport layer or provider implementation | GAR-0019 Article IX §5; Article VI §2 |
| Not substitute membrane or integration classifier | GAR-0019 Article IX §5 |
| Not Universal Execution Foundation | GAR-0019 Article V §11; Article VIII §2; Article IX §5 |
| Not operational integration execution | GAR-0019 Article V §3; Article VIII §2 |
| All runtime through Integration and Interface stack | GAR-0019 Article V §1; Article V §9; Article X §4; Article X §7 |

### Architectural principles

| ADR principle | Constitutional source |
| --- | --- |
| ADR-0013-P01 — Stack Traversal | GAR-0019 Article V §1 (Membrane Supremacy); Article V §9 (Stack Traversal); Article VI §4; Article X §4; Article X §7 |
| ADR-0013-P02 — Subordination to Integration and Interface Contracts | GAR-0019 Article VIII §1 (runtime contract governance subordinate to integration and interface contracts); Article V §9 |
| ADR-0013-P03 — Descriptive Runtime Model | GAR-0019 Article V §3 (Descriptive Before Operational); Article VIII §1–§2; Article IX §5 |
| ADR-0013-P04 — Technology Neutrality | GAR-0019 Article V §4 (Technology Neutrality Continuation); Article VI §2 |
| ADR-0013-P05 — Runtime Context Classification | GAR-0019 Article VIII §1 (runtime participant classification and boundary semantics); Article V §4 |
| ADR-0013-P06 — Cognitive Independence | GAR-0019 Article V §6 (Cognitive Separation Continuation); Article X §2 |
| ADR-0013-P07 — Variability Termination | GAR-0019 Article V §7 (Variability Containment Extension); Article IX §4 |
| ADR-0013-P08 — Platform Core Inheritance | GAR-0019 Article VI §1 (Platform Core law); Article IX §4 |
| ADR-0013-P09 — Integration Foundation Dependency | GAR-0019 Article X §3–§4; Article VI §1 (Integration Foundation immutable); Article IX §4 |
| ADR-0013-P10 — Interface Foundation Dependency | GAR-0019 Article X §3–§4; Article VI §1 (Interface Foundation immutable); Article V §1 |
| ADR-0013-P11 — Universal Execution Foundation Separation | GAR-0019 Article V §11; Article II (Universal Execution Foundation definition); Article VIII §2 |
| ADR-0013-P12 — Operational Runtime Exclusion | GAR-0019 Article II (Operational Runtime definition); Article V §3; Article VI §2; Article VII §6 |

### Architectural invariants

| ADR invariant | Constitutional source |
| --- | --- |
| 1 — Traverses Integration and Interface stack exclusively | GAR-0019 Article V §9; Article X §7 |
| 2 — Subordinate to integration and interface contracts | GAR-0019 Article VIII §1 |
| 3 — Platform Core inheritance | GAR-0019 Article VI §1 |
| 4 — Cognitive foundations unaware of runtime contexts | GAR-0019 Article V §6; Article X §2 |
| 5 — Variability terminates at Runtime Foundation | GAR-0019 Article V §7 |
| 6 — No provider-specific or Operational Runtime behavior | GAR-0019 Article V §3–§4; Article VI §2; Article IX §5 |
| 7 — Additive; no Phase I, Interface, or Integration modification | GAR-0019 Article V §5; Article VI §1 |
| 8 — Depends upon Integration and Interface Foundations | GAR-0019 Article X §3–§4 |
| 9 — No Universal Execution Foundation conflation | GAR-0019 Article V §11; Article VIII §2 |
| 10 — No Operational Runtime introduction or implication | GAR-0019 Article II; Article V §3; Article VII §6 |

### Rejected alternatives

| Rejected alternative | Constitutional source |
| --- | --- |
| Operational runtime layer | GAR-0019 Article V §3; Article VI §2; Article VII §2 Candidate A |
| Orchestration at Runtime Foundation | GAR-0019 Article VI §2; Article VII §2 Candidate C; Article IX §5 |
| Conflation with Universal Execution Foundation | GAR-0019 Article V §11; Article VII §2 Candidate M; Article VIII §2 |
| Provider-specific runtime | GAR-0019 Article V §4; Article VI §2; Article VI §6 |
| Bypassing Integration Foundation | GAR-0019 Article V §9; Article X §4; Article VII §2 Candidates E, L |
| Merging into Integration Foundation | GAR-0019 Article VI §1; Article VII §2 Candidate D |
| Independent object hierarchy | GAR-0019 Article VI §1; ADR-0002 inheritance obligation |

---

## Compliance

All future Runtime Foundation architecture, sprint specifications, implementations, reviews, and
certifications SHALL conform to:

- [GAR-0019](../../GAR-0019.md) — External Capability Expansion Constitutional Extension — Second Derivation
- [GAR-0018](../../GAR-0018.md) — External Capability Expansion Constitutional Extension
- [GAR-0017](../../GAR-0017.md) — Phase II Constitutional Extension
- [ADR-0012](ADR-0012-integration-foundation.md) — Integration Foundation
- [ADR-0011](ADR-0011-interface-foundation.md) — Interface Foundation
- ADR-0002 — Platform Core

---

End of ADR-0013 (Draft)
