# ADR-0012 — Integration Foundation

| Field | Value |
| --- | --- |
| ID | ADR-0012 |
| Title | Integration Foundation |
| Status | Approved v1.0 |
| Date | 2026-07-07 |
| Authority | [GAR-0018](../../GAR-0018.md) — External Capability Expansion Constitutional Extension |
| Epoch | External Capability Expansion |
| Depends on | ADR-0011, ADR-0002 |
| Supersedes | None |

---

## Decision

Project Garuda shall establish an **Integration Foundation** as the architectural realization of
**External Integration** authorized by GAR-0018.

The Integration Foundation shall govern the architectural description of how External Systems
participate as governed integration participants **through** the Constitutional Membrane — without
runtime execution, transport, orchestration, or provider implementation.

The Integration Foundation is an architectural layer. It is not:

- a transport layer,
- a runtime or orchestration engine,
- a provider implementation,
- a substitute for the Interface Foundation or Constitutional Membrane,
- or an operational integration execution system.

All integration architecture SHALL traverse the Interface Foundation. No integration pathway SHALL
bypass the Constitutional Membrane.

---

## Context

GAR-0018 ratified the first external-capability expansion beyond the completed Interface Foundation.

GAR-0017 established the Constitutional Membrane and authorized the Interface Foundation as its
exclusive realization (ADR-0011). The Interface Foundation governs **communication across** the
membrane — canonical contracts, inbound translation, validation, and descriptive interface registry
semantics.

GAR-0018 derived **Integration** as the only admissible first external-capability domain. The
constitutional gap addressed by this ADR is **integration architecture** — how External Systems are
described, classified, related, and governed as integration participants through the membrane,
without operational behavior.

This ADR records the architectural decision subordinate to GAR-0018. It does not create
constitutional authority. Sprint specifications and implementation remain downstream.

---

## Architectural Decision

The Integration Foundation shall realize External Integration through the following architectural
principles.

**ADR-0012-P01 — Membrane Traversal**  
All integration architecture SHALL occur through the Interface Foundation. External Systems SHALL NOT
be integrated into Garuda by bypassing, duplicating, or weakening the Constitutional Membrane.

**ADR-0012-P02 — Subordination to Canonical Interface Contracts**  
Integration contracts, classifications, and relationship semantics SHALL be subordinate to canonical
interface contracts established by the Interface Foundation. Integration architecture SHALL NOT
supersede or replace membrane communication semantics.

**ADR-0012-P03 — Descriptive Integration Model**  
The Integration Foundation SHALL govern architectural **description** only — participant
classification, relationship semantics, integration contract governance, lifecycle and boundary
metadata, and descriptive catalog semantics. It SHALL NOT perform operational integration execution,
connectivity, message delivery, or provider invocation.

**ADR-0012-P04 — Technology Neutrality**  
The Integration Foundation SHALL remain independent of all external technologies. No architectural
decision within the Integration Foundation SHALL require a specific protocol, provider,
infrastructure component, or runtime environment.

**ADR-0012-P05 — Participant Classification**  
External Systems participating in Garuda integration SHALL be represented through deterministic,
technology-neutral classification semantics governed by the Integration Foundation. Classification
SHALL be descriptive and SHALL NOT embed provider-specific identity or operational credentials.

**ADR-0012-P06 — Cognitive Independence**  
The Internal Cognitive Foundations SHALL remain unaware of External Systems and integration
participants. Integration architecture SHALL NOT introduce cognitive dependencies or external
knowledge into Phase I foundations.

**ADR-0012-P07 — Variability Termination**  
Architectural variability introduced by External Systems and integration participants SHALL
terminate at the Integration Foundation (and upstream at the Interface Foundation). No integration
variability SHALL propagate into Internal Cognitive Foundations.

**ADR-0012-P08 — Platform Core Inheritance**  
Every integration artifact authorized by this ADR SHALL derive from the Platform Core object model
established by ADR-0002. The Integration Foundation SHALL NOT establish an independent object
hierarchy.

**ADR-0012-P09 — Interface Foundation Dependency**  
The Integration Foundation SHALL depend upon the Interface Foundation. It SHALL consume canonical
interface contracts and membrane semantics. It SHALL NOT modify the Interface Foundation.

---

## Rationale

This architecture preserves the constitutional derivation established by GAR-0018 while maintaining
the membrane supremacy, cognitive independence, and additive evolution guarantees of GAR-0017 and
ADR-0011.

By governing integration architecture descriptively and subordinately to canonical interface
contracts, Garuda ensures that external participation can be modeled, certified, and evolved without
introducing operational runtime, transport, or provider coupling into the cognitive core or membrane
layer.

The Integration Foundation extends external-capability governance without redefining the Interface
Foundation or any Internal Cognitive Foundation.

---

## Alternatives Considered

| Alternative | Description |
| --- | --- |
| Operational integration layer | Rejected |
| Provider-specific integration architecture | Rejected |
| Integration bypassing Interface Foundation | Rejected |
| Merging integration into Interface Foundation | Rejected |
| Independent Integration object hierarchy | Rejected |

### Why Rejected

**Operational integration layer** — Violates GAR-0018 Principle Descriptive Before Operational and
Article VI prohibited capabilities.

**Provider-specific integration** — Violates GAR-0018 technology neutrality and ADR-0011 rejected
provider-specific patterns.

**Bypassing Interface Foundation** — Violates GAR-0018 Membrane Supremacy and ADR-0011 exclusive
boundary.

**Merging into Interface Foundation** — Violates GAR-0018 derivation; Interface Foundation is complete
and immutable; integration is a distinct external-capability class.

**Independent object hierarchy** — Violates Platform Core inheritance (ADR-0002, ADR-0011 Principle 8).

---

## Consequences

### Positive

- Realizes GAR-0018 External Integration authorization architecturally
- Preserves membrane exclusivity and cognitive independence
- Maintains technology neutrality and additive evolution
- Establishes descriptive integration governance subordinate to interface contracts
- Enables sprint-level specification without constitutional ambiguity

### Negative

- Every external integration participant requires architectural normalization through Interface and
  Integration layers
- Operational integration, transport, and orchestration remain deferred to future constitutional
  authority
- Integration artifacts must conform to Platform Core and Interface Foundation constraints

---

## Architectural Invariants

The following invariants are established by this ADR:

1. Integration architecture traverses the Interface Foundation exclusively.
2. Integration contracts are subordinate to canonical interface contracts.
3. Integration artifacts inherit Platform Core.
4. Internal Cognitive Foundations remain unaware of integration participants.
5. Integration variability terminates at the Integration Foundation.
6. Integration Foundation introduces no provider-specific or operational behavior.
7. The Integration Foundation remains additive and does not modify Phase I or Interface foundations.
8. The Integration Foundation depends upon the Interface Foundation.

---

## Deferred Decisions

The following are intentionally deferred to GAR-SPRINT-0011 and its mission specifications:

- Integration participant model design
- Integration contract architecture
- Classification taxonomy
- Relationship semantics
- Integration lifecycle and boundary model
- Integration registry or catalog architecture
- Certification scenarios
- Repository layout and package structure
- Sprint mission decomposition
- Testing strategy
- Implementation details

These topics belong to the approved sprint specification, not to this ADR.

---

## Constitutional Traceability

Every architectural decision in this ADR derives from ratified GAR-0018. This appendix provides the
constitutional audit trail from law to architecture. No ADR provision creates constitutional authority.

### Decision statement

| ADR provision | Constitutional source |
| --- | --- |
| Establish Integration Foundation | GAR-0018 Article IX §2 — Foundation Authorization |
| External Integration definition | GAR-0018 Article IX §1 — External Integration |
| Govern integration participants through membrane | GAR-0018 Article VI §4; Article IX §3 |
| Without runtime, transport, orchestration, provider | GAR-0018 Article V §3; Article VI §2; Article VIII §2 |
| Not a transport layer | GAR-0018 Article IX §5; Article VI §2 |
| Not runtime or orchestration engine | GAR-0018 Article IX §5; Article VI §2 |
| Not provider implementation | GAR-0018 Article IX §5; Article VI §2 |
| Not substitute membrane | GAR-0018 Article V §1; Article IX §5 |
| Not operational integration execution | GAR-0018 Article V §3; Article VIII §2 |
| All integration through Interface Foundation | GAR-0018 Article V §1; Article VI §4; Article X §4 |

### Architectural principles

| ADR principle | Constitutional source |
| --- | --- |
| ADR-0012-P01 — Membrane Traversal | GAR-0018 Article V §1 (Membrane Supremacy); Article VI §4 (Membrane Exclusivity Preservation); Article X §4 |
| ADR-0012-P02 — Subordination to Canonical Interface Contracts | GAR-0018 Article VIII §1 (integration contract governance subordinate to canonical interface contracts); Article V §1 |
| ADR-0012-P03 — Descriptive Integration Model | GAR-0018 Article V §3 (Descriptive Before Operational); Article VIII §1–§2; Article IX §5 |
| ADR-0012-P04 — Technology Neutrality | GAR-0018 Article V §4 (Technology Neutrality Continuation); Article VI §2 |
| ADR-0012-P05 — Participant Classification | GAR-0018 Article VIII §1 (integration participant classification and relationship semantics); Article V §4 |
| ADR-0012-P06 — Cognitive Independence | GAR-0018 Article V §6 (Cognitive Separation Continuation); Article X §2 |
| ADR-0012-P07 — Variability Termination | GAR-0018 Article V §7 (Variability Containment Extension); Article IX §4 |
| ADR-0012-P08 — Platform Core Inheritance | GAR-0018 Article IX §4 (Platform Core object model obligations through ADR authority); Article VI §1 |
| ADR-0012-P09 — Interface Foundation Dependency | GAR-0018 Article X §3–§4; Article VI §1 (Interface Foundation immutable); Article IX §4 |

### Architectural invariants

| ADR invariant | Constitutional source |
| --- | --- |
| 1 — Traverses Interface Foundation exclusively | GAR-0018 Article V §1; Article VI §4 |
| 2 — Subordinate to canonical interface contracts | GAR-0018 Article VIII §1 |
| 3 — Platform Core inheritance | GAR-0018 Article IX §4 |
| 4 — Cognitive foundations unaware of participants | GAR-0018 Article V §6; Article X §2 |
| 5 — Variability terminates at Integration Foundation | GAR-0018 Article V §7 |
| 6 — No provider-specific or operational behavior | GAR-0018 Article V §3–§4; Article VI §2; Article IX §5 |
| 7 — Additive; no Phase I or Interface modification | GAR-0018 Article V §5; Article VI §1 |
| 8 — Depends upon Interface Foundation | GAR-0018 Article X §3–§4 |

### Rejected alternatives

| Rejected alternative | Constitutional source |
| --- | --- |
| Operational integration layer | GAR-0018 Article V §3; Article VI §2; Article VII §2 Candidate A |
| Provider-specific integration | GAR-0018 Article V §4; Article VI §2; Article VI §6; Article VII §2 Candidate F |
| Bypassing Interface Foundation | GAR-0018 Article V §1; Article VI §4; Article VII §2 Candidates E, K |
| Merging into Interface Foundation | GAR-0018 Article VI §1; Article VII §4 (Extend Interface instead of new domain) |
| Independent object hierarchy | GAR-0018 Article IX §4; Article VI §1 (Platform Core law) |

---

## Compliance

All future Integration Foundation architecture, sprint specifications, implementations, reviews, and
certifications SHALL conform to:

- [GAR-0018](../../GAR-0018.md) — External Capability Expansion Constitutional Extension
- [GAR-0017](../../GAR-0017.md) — Phase II Constitutional Extension
- [ADR-0011](ADR-0011-interface-foundation.md) — Interface Foundation
- ADR-0002 — Platform Core

---

End of ADR-0012
