# ADR-0014 — Investment Intelligence Architecture

| Field | Value |
| --- | --- |
| ID | ADR-0014 |
| Title | Investment Intelligence Architecture |
| Status | **Draft v0.6 — Under Architectural Review** |
| Date | 2026-07-09 |
| Authority | [GAR-0021](../../GAR-0021.md) v1.0 — Constitutional Principles for Investment Intelligence |
| Evidence foundation | CEB Edition 1.0 (frozen & published `4dc5ff7`) |
| Drafting authorization | [GOVERNANCE-CYCLE-7-ADR-0014-AUTHORIZATION.md](../governance/GOVERNANCE-CYCLE-7-ADR-0014-AUTHORIZATION.md) (`04372fa`) |
| Architecture class | Domain Architecture |
| Depends on | GAR-0021 v1.0; CEB Edition 1.0; Garuda OS constitutional stack (Book One) |
| Supersedes | None |
| Implementation authority | **None** |

---

## Purpose

This Architectural Decision Record defines the architectural principles governing the
implementation of Investment Intelligence within Project Garuda.

Its purpose is to translate the constitutional authority established by GAR-0021 into an
implementation-independent architectural framework.

ADR-0014 does not establish constitutional authority.
ADR-0014 does not authorize engineering implementation.

Architecture exists solely to faithfully express constitutional law.

---

## Scope

ADR-0014 defines:

- Architectural responsibilities
- Architectural boundaries
- Constitutional enforcement points
- Evidence lineage throughout the system
- Decision architecture
- Explainability architecture
- Refusal architecture
- Traceability architecture
- Component responsibilities
- Information flow between architectural domains

ADR-0014 intentionally excludes implementation decisions.

---

## Architectural Position

Investment Intelligence is a constitutional domain operating within the Garuda Operating System.

Accordingly:

- GAR Constitutions remain the supreme architectural authority
- GAR-0021 governs Investment Intelligence
- ADR-0014 translates GAR-0021 into architecture
- Future implementation shall derive from ADR-0014
- Future engineering shall derive from approved sprint specifications

Authority shall always flow downward.

Implementation shall never redefine architecture.
Architecture shall never redefine constitutional authority.

---

## Architectural Assumptions

The architecture assumes:

1. Investment Intelligence operates under uncertainty
2. Evidence precedes reasoning
3. Reasoning precedes judgment
4. Judgment precedes commitment or refusal
5. Human authority is constitutionally superior to system recommendation
6. Every recommendation must remain constitutionally explainable
7. Refusal is a valid architectural outcome
8. Constitutional traceability shall exist throughout the architecture
9. Evidence integrity is a prerequisite for justified reasoning
10. Architectural components remain replaceable without altering constitutional authority

These assumptions derive exclusively from GAR-0021 and CEB Edition 1.0.

---

## Decision

Project Garuda shall establish an **Investment Intelligence Architecture** as the architectural
realization of GAR-0021 v1.0.

The architecture shall govern how Investment Intelligence responsibilities are separated, bounded,
and related so that future implementations may operate within constitutional authority — without
selecting technologies, defining packages as engineering deliverables, or authorizing sprints.

Draft v0.6 establishes architectural principles, enduring responsibilities, a conceptual
responsibility flow, responsibility allocation principles, Architectural Domains (Article I), the
Architectural Interaction Model (Article II), Constitutional Governance Architecture
(Article III), and the Canonical Investment Intelligence Lifecycle (Article IV). Implementation
components, interfaces, data schemas, runtime contracts, deployment structures, and technology
selections are **not** established in this version.

---

## Architectural Principles

### Principle A — Constitutional Primacy

Every architectural component shall derive its responsibility from constitutional authority.

No component may operate outside GAR-0021.

**Constitutional source:** GAR-0021 Article I; Preamble (Core Axiom).

---

### Principle B — Evidence Integrity

Evidence lineage shall be preserved throughout the architecture.

Architectural boundaries shall never permit evidence corruption without detection.

**Constitutional source:** GAR-0021 Principles 3, 12; Distinction 7; CEB-0000 Evidence Integrity.

---

### Principle C — Separation of Responsibilities

Acquisition, validation, reasoning, judgment, explanation, refusal, and interaction shall remain
architecturally separable responsibilities.

Architectural coupling shall be minimized.

**Constitutional source:** GAR-0021 Distinction 7 (epistemic ladder); Principle 10 (Process over Prediction).

---

### Principle D — Explainability by Design

Explainability is an architectural capability, not a reporting feature.

Every recommendation shall retain an auditable reasoning path.

**Constitutional source:** GAR-0021 Principle 4; Distinction 24.

---

### Principle E — Constitutional Refusal

Refusal shall be represented as a first-class architectural capability.

Architecture shall not require recommendation when constitutional obligations cannot be satisfied.

**Constitutional source:** GAR-0021 Principles 2, 5, 13; Distinction 23.

---

### Principle F — Traceability

Architectural decisions shall remain traceable to:

- GAR Constitutions
- GAR-0021
- CEB Edition 1.0

Future implementation shall inherit this traceability.

**Constitutional source:** GAR-0021 Article VI; Preamble (Recognition Standard).

---

### Principle G — Technology Neutrality

Architecture shall define responsibilities rather than technologies.

No implementation technology is implied by this ADR.

**Constitutional source:** GAR-0021 Drafting Compass; Gate D non-authorization list.

---

### Principle H — Replaceable Implementation

Implementations may evolve.

Architectural responsibilities shall remain stable unless amended through constitutional governance.

**Constitutional source:** GAR-0021 Article VI §4; Principle 11 (Learning Within Bounds).

---

## Architectural Responsibilities

Investment Intelligence architecture is defined first by enduring responsibilities, not by
implementation components.

A responsibility is a constitutionally necessary function that future implementations must satisfy.

Components may change.
Technologies may change.
Deployment models may change.

Architectural responsibilities remain stable unless amended through governance.

---

### Responsibility 1 — Evidence Acquisition

The architecture shall provide a responsibility for acquiring observations from external or
internal sources without prematurely converting them into conclusions.

Evidence Acquisition does not decide.
Evidence Acquisition does not judge.
Evidence Acquisition does not recommend.

Its purpose is to collect candidate information while preserving source identity, acquisition
context, and lineage.

---

### Responsibility 2 — Evidence Validation

The architecture shall provide a responsibility for evaluating acquired information before it is
admitted as evidence.

Evidence Validation shall assess reliability, relevance, completeness, freshness, provenance, and
integrity.

Information that fails validation shall not be silently promoted into evidence.

Where validation is insufficient, the architecture shall preserve uncertainty or trigger
constitutional refusal.

---

### Responsibility 3 — Knowledge Organization

The architecture shall provide a responsibility for organizing validated evidence into structured
knowledge without severing lineage.

Knowledge Organization shall preserve the distinction between information, evidence, knowledge,
judgment, decision, and refusal.

Knowledge Organization does not eliminate uncertainty.
It makes uncertainty usable for later judgment.

---

### Responsibility 4 — Context Integration

The architecture shall provide a responsibility for integrating decision context.

Context may include human objectives, constraints, time horizon, risk tolerance, liquidity needs,
capital availability, locale, tax/regulatory context, portfolio exposure, and prior commitments.

Where material context is missing, the architecture shall not fabricate it.

It shall either proceed with explicit limitation or trigger constitutional refusal.

---

### Responsibility 5 — Judgment Formation

The architecture shall provide a responsibility for forming justified judgments under uncertainty.

Judgment Formation shall weigh supporting evidence, contradictory evidence, assumptions,
limitations, asymmetries, costs, incentives, and relevant tensions.

Judgment Formation shall not collapse uncertainty into false certainty.

---

### Responsibility 6 — Constitutional Compliance

The architecture shall provide a responsibility for enforcing GAR-0021.

Constitutional Compliance shall evaluate whether reasoning, judgment, recommendation, explanation,
or refusal conforms to the constitutional Principles, Distinctions, and Tensions.

No advice or commitment may bypass Constitutional Compliance.

---

### Responsibility 7 — Decision Formation

The architecture shall provide a responsibility for forming an output decision state.

A decision state may include:

- recommendation
- non-recommendation
- conditional recommendation
- request for additional context
- refusal

Decision Formation shall not treat recommendation as the only successful outcome.

---

### Responsibility 8 — Refusal Formation

The architecture shall provide a responsibility for forming constitutional refusal.

Refusal Formation shall activate when the architecture cannot satisfy constitutional obligations
such as evidence integrity, objective clarity, sufficient context, justified confidence, or
explainability.

Refusal shall be treated as a valid architectural output, not as system failure.

---

### Responsibility 9 — Explainability

The architecture shall provide a responsibility for generating justificatory explanations.

Explainability shall expose the reasoning path appropriate to the output decision state.

Explainability shall distinguish between:

- evidence
- assumptions
- uncertainty
- judgment
- limitation
- recommendation
- refusal

A soothing narrative shall not substitute for justification.

---

### Responsibility 10 — Traceability

The architecture shall provide a responsibility for maintaining lineage from constitutional
authority to architectural responsibility, evidence source, reasoning path, decision state, and
explanation.

Traceability shall make it possible to audit how an output was formed.

Traceability is not optional documentation.
It is an architectural obligation.

---

### Responsibility 11 — Learning Governance

The architecture shall provide a responsibility for governing learning and adaptation.

Learning may improve knowledge, models, heuristics, or system behavior.

Learning shall not silently alter constitutional obligations, architectural boundaries, or
authority chains.

Learning outcomes remain subordinate to GAR-0021 and approved architecture.

---

## High-Level Responsibility Flow

ADR-0014 establishes the following conceptual responsibility flow:

```text
External / Internal Inputs
        |
        v
Evidence Acquisition
        |
        v
Evidence Validation
        |
        v
Knowledge Organization
        |
        v
Context Integration
        |
        v
Judgment Formation
        |
        v
Constitutional Compliance
        |
        v
Decision Formation
        |
        +-------------------+
        |                   |
        v                   v
Recommendation        Constitutional Refusal
        |                   |
        +---------+---------+
                  |
                  v
Explainability
                  |
                  v
Traceability
```

This flow is conceptual.

It does not prescribe implementation order, runtime topology, programming model, service
boundaries, or deployment structure.

---

## Responsibility Allocation Principles

### Allocation Principle 1 — Responsibilities Precede Components

Future implementation components shall be justified by the responsibilities they satisfy.

No component shall be introduced merely because it is conventional, fashionable, or technically
convenient.

---

### Allocation Principle 2 — Constitutional Responsibilities May Be Distributed

A single responsibility may be fulfilled by multiple components.

A single component may contribute to multiple responsibilities.

However, no responsibility may disappear because of implementation convenience.

---

### Allocation Principle 3 — Compliance Cannot Be Optional

Constitutional Compliance shall not be implemented as a bypassable advisory layer.

Every decision state must be subject to constitutional evaluation.

---

### Allocation Principle 4 — Refusal Must Be Reachable

Architecture shall ensure that refusal is reachable wherever constitutional obligations cannot be
satisfied.

A system that can only recommend is constitutionally incomplete.

---

### Allocation Principle 5 — Explainability Must Be Preserved Across Boundaries

Architectural boundaries shall not destroy the reasoning path required for justificatory
explainability.

If reasoning cannot be explained, the architecture must preserve that limitation rather than
conceal it.

---

### Allocation Principle 6 — Traceability Must Survive Substitution

Future replacement of models, data sources, tools, services, or interfaces shall not eliminate
traceability.

Replaceable implementation is permitted only where constitutional lineage remains intact.

---

## Article I — Architectural Domains

### Architectural Position

Architectural Domains represent enduring constitutional responsibilities grouped into coherent
areas of responsibility.

Architectural Domains are not software components.
Architectural Domains are not deployment units.
Architectural Domains are not programming modules.

Future implementations may realize these domains using one or more components, provided
constitutional responsibilities remain intact.

Every domain derives its authority from GAR-0021 and the Architectural Responsibilities
established by this ADR.

---

### Domain A — Evidence Domain

#### Constitutional Purpose

Acquire, validate and preserve evidence while maintaining Evidence Integrity.

#### Responsibilities

- Evidence Acquisition
- Evidence Validation
- Source Provenance
- Evidence Lineage
- Freshness Assessment
- Evidence Confidence
- Contradictory Evidence Preservation

#### Constitutional Constraints

The Evidence Domain shall never:

- fabricate evidence
- silently discard contradictory evidence
- remove uncertainty
- promote information into evidence without validation

---

### Domain B — Knowledge Domain

#### Constitutional Purpose

Transform validated evidence into organized knowledge while preserving lineage.

#### Responsibilities

- Knowledge Organization
- Entity Relationships
- Context Preservation
- Historical Memory
- Cross-Evidence Association
- Knowledge Retrieval

#### Constitutional Constraints

Knowledge shall remain distinguishable from:

- Information
- Evidence
- Judgment
- Decision

Knowledge shall never replace constitutional reasoning.

---

### Domain C — Context Domain

#### Constitutional Purpose

Maintain all decision context required for justified reasoning.

#### Responsibilities

- Human Objectives
- Risk Profile
- Time Horizon
- Portfolio Context
- Capital Constraints
- Locale
- Regulatory Context
- User Preferences
- Active Commitments

#### Constitutional Constraints

Missing context shall never be silently assumed.

Insufficient context may constitutionally result in refusal.

---

### Domain D — Judgment Domain

#### Constitutional Purpose

Produce justified judgments under uncertainty.

#### Responsibilities

- Evidence Weighing
- Contradiction Resolution
- Assumption Management
- Scenario Evaluation
- Confidence Assessment
- Opportunity Cost Evaluation
- Risk Assessment
- Constitutional Tension Recognition

#### Constitutional Constraints

Judgment shall never:

- manufacture certainty
- ignore contradictory evidence
- optimize without survivability
- confuse probability with certainty

---

### Domain E — Constitutional Domain

#### Constitutional Purpose

Ensure all architectural activity conforms to GAR-0021.

#### Responsibilities

- Principle Evaluation
- Distinction Enforcement
- Tension Recognition
- Constitutional Refusal
- Compliance Verification
- Constitutional Traceability

#### Constitutional Constraints

No architectural output may bypass constitutional evaluation.

Constitutional authority remains superior to all architectural decisions.

---

### Domain F — Decision Domain

#### Constitutional Purpose

Transform justified judgment into constitutionally valid outcomes.

#### Responsibilities

- Recommendation Formation
- Conditional Recommendation
- Information Request
- Refusal Formation
- Decision State Management

#### Constitutional Constraints

Recommendation is not the default outcome.

Refusal is a constitutionally valid decision state.

---

### Domain G — Explainability Domain

#### Constitutional Purpose

Expose the reasoning necessary to justify every architectural outcome.

#### Responsibilities

- Evidence Narrative
- Judgment Narrative
- Assumption Disclosure
- Limitation Disclosure
- Confidence Communication
- Refusal Explanation

#### Constitutional Constraints

Explanation shall justify.
It shall not persuade.
It shall not conceal uncertainty.

---

### Domain H — Traceability Domain

#### Constitutional Purpose

Maintain complete constitutional lineage across the architecture.

#### Responsibilities

- Evidence Lineage
- Knowledge Lineage
- Judgment Lineage
- Decision Lineage
- Constitutional Lineage
- Audit Support

#### Constitutional Constraints

Every recommendation or refusal shall remain traceable to:

- constitutional authority
- architectural responsibility
- evidence
- reasoning
- explanation

---

### Domain Relationships

The architecture recognizes the following conceptual flow:

```text
Evidence Domain
        │
        ▼
Knowledge Domain
        │
        ▼
Context Domain
        │
        ▼
Judgment Domain
        │
        ▼
Constitutional Domain
        │
        ▼
Decision Domain
       ┌┴┐
       │ │
       ▼ ▼
Advice Refusal
       │
       ▼
Explainability Domain
       │
       ▼
Traceability Domain
```

This flow represents constitutional responsibility.

It does not prescribe runtime execution, deployment topology, software architecture, messaging
patterns, or implementation technologies.

---

### Architectural Integrity

The Architectural Domains collectively satisfy every Architectural Responsibility defined in
ADR-0014.

Future architectural refinement may introduce implementation structures, provided:

- constitutional authority is preserved
- responsibilities remain intact
- traceability is maintained
- constitutional obligations are never bypassed

No implementation decisions are established by this article.

**End of Article I — Architectural Domains**

---

## Article II — Architectural Interaction Model

### Architectural Position

Architectural Domains do not operate independently.

They cooperate through constitutional interactions.

Every interaction shall preserve:

- constitutional authority
- evidence integrity
- explainability
- traceability
- constitutional refusal

Interactions define responsibilities.
They do not prescribe implementation mechanisms.

---

### Constitutional Interaction Principles

#### Principle 1 — Evidence Shall Flow Forward

Evidence may progress through the architecture.

It shall never silently disappear.

Every transformation shall preserve lineage.

---

#### Principle 2 — Context Shall Accumulate

Context may be enriched as reasoning progresses.

Context shall never be silently fabricated.

Unknown context shall remain explicitly unknown.

---

#### Principle 3 — Judgment Shall Remain Reversible

Before commitment or refusal, judgment remains provisional.

Architecture shall permit reconsideration when new evidence becomes available.

---

#### Principle 4 — Constitutional Evaluation Precedes Commitment

No recommendation shall become an architectural outcome until constitutional compliance has been
evaluated.

---

#### Principle 5 — Refusal May Arise Anywhere

Every architectural domain may identify conditions requiring constitutional refusal.

Refusal is not owned exclusively by the Decision Domain.

The Decision Domain formalizes refusal.

The architecture recognizes it throughout.

---

#### Principle 6 — Explainability Emerges from the Entire Interaction

Explainability shall not be generated after the decision.

It shall emerge continuously from every architectural interaction.

---

### Canonical Constitutional Flow

The architecture recognizes the following conceptual interaction:

```text
Evidence
      │
      ▼
Validation
      │
      ▼
Knowledge
      │
      ▼
Context
      │
      ▼
Judgment
      │
      ▼
Constitutional Evaluation
      │
      ├──────────────┐
      ▼              ▼
Recommendation   Refusal
      │              │
      └──────┬───────┘
             ▼
Explainability
             │
             ▼
Traceability
```

This represents constitutional reasoning.

It is not a runtime pipeline.

---

### Architectural Interaction Rules

#### Rule 1

No domain shall bypass Constitutional Evaluation.

---

#### Rule 2

No recommendation shall exist without supporting evidence.

---

#### Rule 3

Every judgment shall preserve uncertainty where appropriate.

---

#### Rule 4

Every recommendation shall remain explainable.

---

#### Rule 5

Every refusal shall remain explainable.

---

#### Rule 6

Every architectural interaction shall remain traceable.

---

#### Rule 7

Future architectural refinements may optimize interactions but shall not violate constitutional
obligations.

---

### Constitutional Failure States

The architecture recognizes several classes of constitutional failure.

Examples include:

- insufficient evidence
- corrupted evidence
- contradictory evidence that cannot be responsibly resolved
- absent objectives
- missing material context
- broken traceability
- inability to justify reasoning
- violation of constitutional distinctions
- unresolved constitutional tensions requiring human judgment

When such conditions arise, the architecture shall preserve constitutional integrity ahead of
functional completion.

Refusal may therefore represent successful constitutional behavior.

---

### Architectural Consequence

Architecture is not optimized for producing recommendations.

Architecture is optimized for producing constitutionally justified outcomes.

A recommendation and a refusal are both valid architectural conclusions when they faithfully
satisfy GAR-0021.

---

### Scope Boundary

This article defines architectural interactions only.

It establishes:

- constitutional cooperation
- interaction discipline
- reasoning flow
- constitutional checkpoints

It does not establish:

- APIs
- message buses
- service calls
- synchronous or asynchronous execution
- orchestration
- deployment
- runtime sequencing

Those belong to future architecture refinement and implementation.

**End of Article II — Architectural Interaction Model**

---

## Article III — Constitutional Governance Architecture

### Architectural Position

Constitutional Governance is an architectural capability.

It is not an external review process.

Every architectural outcome shall remain subject to constitutional governance throughout its
lifecycle.

Constitutional Governance exists to preserve the authority of GAR-0021 within every future
implementation.

---

### Governance Objectives

The Constitutional Governance Architecture shall ensure that:

- constitutional authority remains supreme
- architectural behavior remains traceable
- constitutional obligations remain enforceable
- constitutional distinctions remain preserved
- constitutional tensions remain visible
- future implementations cannot silently drift away from constitutional authority

---

### Governance Responsibilities

#### Responsibility 1 — Constitutional Verification

Every recommendation, refusal, or architectural outcome shall be evaluated against GAR-0021 before
it is considered complete.

---

#### Responsibility 2 — Constitutional Traceability

Every architectural outcome shall remain traceable to:

- constitutional authority
- architectural responsibility
- supporting evidence
- reasoning path
- decision state
- explanation

Loss of traceability shall be treated as constitutional degradation.

---

#### Responsibility 3 — Distinction Protection

The architecture shall preserve every Constitutional Distinction established by GAR-0021.

Future implementations shall not collapse constitutionally distinct concepts into a single
representation merely for implementation convenience.

---

#### Responsibility 4 — Tension Recognition

Architectural decisions shall explicitly recognize applicable Constitutional Tensions.

The architecture shall expose tensions where necessary rather than concealing them behind
deterministic outputs.

---

#### Responsibility 5 — Constitutional Refusal

Where constitutional obligations cannot be satisfied, the architecture shall preserve the ability
to refuse.

No architectural optimization shall eliminate constitutional refusal.

---

#### Responsibility 6 — Explainability Preservation

Architectural evolution shall never reduce the ability to justify recommendations or refusals.

Explainability shall remain an architectural invariant.

---

### Architectural Invariants

The following architectural properties shall remain invariant unless constitutional governance
explicitly amends GAR-0021.

#### Invariant A

Evidence Integrity.

---

#### Invariant B

Human Authority.

---

#### Invariant C

Justificatory Explainability.

---

#### Invariant D

Constitutional Traceability.

---

#### Invariant E

Constitutional Refusal.

---

#### Invariant F

Technology Neutrality.

---

#### Invariant G

Replaceable Implementation.

---

### Architectural Compliance Checkpoints

Architectural refinement shall demonstrate compliance at the following checkpoints:

1. Constitutional Authority
2. Evidence Integrity
3. Responsibility Coverage
4. Domain Integrity
5. Interaction Integrity
6. Explainability
7. Traceability
8. Refusal Capability

Failure at any checkpoint shall require architectural review before implementation may proceed.

---

### Evolution Rules

Future architectural revisions may:

- improve clarity
- improve modularity
- improve maintainability
- improve replaceability

Future revisions shall not:

- weaken constitutional obligations
- bypass constitutional evaluation
- eliminate refusal
- obscure evidence lineage
- reduce explainability
- weaken traceability

Such changes require constitutional governance rather than architectural discretion.

---

### Architectural Consequence

Architecture remains subordinate to constitutional authority.

Implementation remains subordinate to architecture.

Optimization remains subordinate to constitutional integrity.

Architectural excellence shall therefore be measured not only by capability, but by constitutional
fidelity.

---

### Scope Boundary

This article governs architectural integrity only.

It does not define:

- implementation validation
- runtime monitoring
- operational governance
- deployment governance
- infrastructure controls

Those belong to future ADRs and implementation phases following explicit Founder authorization.

**End of Article III — Constitutional Governance Architecture**

---

## Article IV — Canonical Investment Intelligence Lifecycle

### Architectural Position

The Investment Intelligence Architecture recognizes a canonical lifecycle through which every
recommendation, non-recommendation, conditional recommendation, information request, and
constitutional refusal shall pass.

This lifecycle defines constitutional stages of reasoning.

It does not define runtime execution.

Future implementations may realize this lifecycle using different technologies, execution models,
or deployment strategies, provided the constitutional stages remain preserved.

---

### Lifecycle Objectives

The lifecycle exists to ensure that every architectural outcome:

- originates from evidence
- remains constitutionally governed
- preserves uncertainty
- remains explainable
- remains traceable
- respects human authority

---

### Stage 1 — Observation

**Purpose:** Acquire candidate observations from external or internal sources.

Typical observations include:

- market activity
- enterprise information
- macroeconomic information
- portfolio state
- user context
- historical knowledge

Observations are not yet evidence.

---

### Stage 2 — Evidence Validation

**Purpose:** Determine whether observations satisfy constitutional Evidence Integrity.

Validation considers:

- provenance
- reliability
- relevance
- completeness
- consistency
- freshness

Insufficient validation prevents promotion into evidence.

---

### Stage 3 — Knowledge Formation

**Purpose:** Organize validated evidence into coherent knowledge while preserving lineage.

Knowledge Formation shall preserve:

- supporting evidence
- contradictory evidence
- uncertainty
- historical context
- relationships

Knowledge is not yet judgment.

---

### Stage 4 — Context Integration

**Purpose:** Integrate knowledge with the current decision context.

Context includes:

- objectives
- constraints
- capital
- time horizon
- locale
- existing commitments
- constitutional limitations

Missing material context shall remain explicit.

---

### Stage 5 — Judgment Formation

**Purpose:** Produce justified judgments under uncertainty.

Judgment Formation shall evaluate:

- evidence
- assumptions
- alternatives
- asymmetries
- incentives
- costs
- Constitutional Distinctions
- Constitutional Tensions

Judgment shall preserve uncertainty.

---

### Stage 6 — Constitutional Evaluation

**Purpose:** Determine whether judgment satisfies GAR-0021.

Evaluation includes:

- Principles
- Distinctions
- Tensions
- Explainability
- Traceability
- Human Authority

No architectural outcome may bypass this stage.

---

### Stage 7 — Decision Formation

**Purpose:** Produce one of the constitutionally valid decision states.

Permitted outcomes include:

- Recommendation
- Conditional Recommendation
- Information Request
- Deferred Decision
- Constitutional Refusal

Recommendation is not the default.

---

### Stage 8 — Explainability

**Purpose:** Generate the justification appropriate to the decision state.

Explainability shall communicate:

- evidence
- assumptions
- uncertainty
- confidence
- limitations
- constitutional reasoning
- refusal rationale (where applicable)

Narrative shall never replace justification.

---

### Stage 9 — Traceability

**Purpose:** Record constitutional lineage.

Every decision state shall remain traceable to:

- constitutional authority
- architectural responsibility
- evidence
- reasoning
- explanation

Traceability completes the lifecycle.

---

### Canonical Lifecycle

```text
Observation
      │
      ▼
Evidence Validation
      │
      ▼
Knowledge Formation
      │
      ▼
Context Integration
      │
      ▼
Judgment Formation
      │
      ▼
Constitutional Evaluation
      │
      ▼
Decision Formation
      │
      ├───────────────┐
      ▼               ▼
Recommendation   Constitutional Refusal
      │               │
      └──────┬────────┘
             ▼
Explainability
             ▼
Traceability
```

---

### Lifecycle Guarantees

Every implementation derived from ADR-0014 shall preserve:

- Evidence before Judgment
- Judgment before Commitment
- Constitutional Evaluation before Decision
- Explainability before Delivery
- Traceability before Completion

These guarantees shall remain invariant across all future implementations.

---

### Architectural Consequences

The architecture is intentionally designed so that:

- recommendations are earned
- refusals are valid
- uncertainty is preserved
- evidence is never bypassed
- constitutional authority remains supreme

The lifecycle therefore governs **how intelligent investment decisions are constitutionally
formed**, independent of implementation technology.

---

### Scope Boundary

This article defines the canonical architectural lifecycle only.

It does not prescribe:

- runtime orchestration
- concurrency
- distributed execution
- scheduling
- infrastructure
- APIs
- storage
- transport
- implementation sequencing

Those remain outside the scope of ADR-0014.

**End of Article IV — Canonical Investment Intelligence Lifecycle**

---

## Non-Authorization

ADR-0014 Draft v0.6 does **not** authorize:

- Engineering
- Sprint drafting
- Production code
- Technology selection
- AI model selection
- Market data integration
- Broker connectivity
- Infrastructure
- User interface design

These remain subject to future governance.

---

## Draft Status

This document defines architectural principles, enduring responsibilities, Architectural Domains,
the Architectural Interaction Model, Constitutional Governance Architecture, and the Canonical
Investment Intelligence Lifecycle only.

No implementation components, interfaces, data schemas, runtime contracts, deployment structures,
or technology selections are established in this version.

Those remain subject to subsequent architectural review and Founder approval.

Approval of a later ADR-0014 version shall **not** by itself authorize GAR-SPRINT-0013 or
engineering. Sprint and engineering require separate Founder gates (Gate D authority boundary).

---

## Compliance

All future Investment Intelligence architecture, sprint specifications, implementations, reviews,
and certifications SHALL conform to:

- [GAR-0021](../../GAR-0021.md) v1.0 — Constitutional Principles for Investment Intelligence
- CEB Edition 1.0 — evidentiary foundation
- This ADR (upon Founder approval of a completed version)
- Book One GAR Constitutions and Foundations as applicable to platform inheritance

---

## Related Documents

- [GOVERNANCE-CYCLE-7-ADR-0014-AUTHORIZATION.md](../governance/GOVERNANCE-CYCLE-7-ADR-0014-AUTHORIZATION.md)
- [GAR-0021-FOUNDER-RATIFICATION.md](../governance/GAR-0021-FOUNDER-RATIFICATION.md)
- [GAR-0021-FREEZE.md](../governance/GAR-0021-FREEZE.md)
- [../constitutional-evidence-base/CEB-FREEZE.md](../constitutional-evidence-base/CEB-FREEZE.md)
- [ADR-0013-runtime-foundation.md](ADR-0013-runtime-foundation.md) — prior ADR form reference

---

End of ADR-0014 Draft v0.6
