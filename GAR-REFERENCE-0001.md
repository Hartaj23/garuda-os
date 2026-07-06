# GAR-REFERENCE-0001

# Garuda Constitutional Engineering Reference Manual

| Field | Value |
| --- | --- |
| Document ID | GAR-REFERENCE-0001 |
| Title | Garuda Constitutional Engineering Reference Manual |
| Classification | Institutional Reference |
| Authority | Descriptive |
| Normative Weight | None |
| Version | 1.0 |
| Published | 2026-07-06 |
| Constitutional chain | Not part of the constitutional chain |

---

## Reference Principle

The Reference Manual describes the system exactly as it exists at the time of publication. It is
descriptive rather than normative. Where conflict exists, constitutions, ADRs, approved sprint
specifications, and the repository always take precedence.

---

## 1. Purpose and Audience

This document consolidates how Project Garuda is engineered. It explains, organizes, cross-references,
and teaches the constitutional engineering lifecycle as practiced in the repository.

**Intended audience:**

- Human engineers joining Project Garuda
- AI implementation agents (Principal Implementation Engineers)
- Reviewers verifying institutional compliance

**This document SHALL:**

- explain workflows and conventions
- organize governance concepts into a single onboarding path
- cross-reference authoritative sources
- teach when and how each engineering stage applies

**This document SHALL NOT:**

- authorize work
- amend any GAR constitution
- supersede ADRs, sprint specifications, or mission plans
- redefine architecture or governance law

For operational rules governing AI agents, see `AGENTS.md`. For repository state, see
`GARUDA_CONTEXT.md` and `GAR-CODEX-CONTEXT.md`.

---

## 2. Authority Hierarchy

Project Garuda resolves conflicts through a fixed authority order. Lower artifacts never override
higher authority.

```
GAR-INDEX
    ↓
GAR Constitutions (GAR-0001 through GAR-0017 and successors)
    ↓
Architecture Decision Records (ADRs)
    ↓
Approved Sprint Specifications
    ↓
Approved Mission Implementation Plans
    ↓
GAR-CODEX-CONTEXT.md
    ↓
Committed Repository State
    ↓
Descriptive References (including this document)
```

| Layer | Role | Example |
| --- | --- | --- |
| GAR Constitution | Establishes constitutional law | GAR-0017 — Phase II Constitutional Extension |
| ADR | Records architectural decision subordinate to constitution | ADR-0011 — Interface Foundation |
| Sprint specification | Operationalizes architecture into authorized work | GAR-SPRINT-0010-interface-foundation.md |
| Mission plan | Defines scope, deliverables, and exit criteria for one mission | GAR-SPRINT-0010-mission-alpha-implementation-plan.md |
| Repository | Source of truth for implemented behavior | `packages/interface/`, tests, docs |

**Roles:**

| Role | Responsibility |
| --- | --- |
| Founder | Ratifies constitutions and releases |
| Chief Systems Architect | Drafts architecture, ADRs, sprint specifications; reviews missions |
| Principal Implementation Engineer | Plans, implements, tests, documents under approved scope |
| Repository (Git) | Immutable record of all approved work |

Never infer architecture from code alone. Always trace authority upward through the hierarchy.

---

## 3. Constitutional Workflow

Constitutional documents establish the highest governing law for Project Garuda.

**Typical constitutional lifecycle:**

1. Architectural need identified at Phase or foundation level
2. Chief Systems Architect drafts constitutional extension or amendment
3. Founder ratifies the document at a versioned status (for example, v1.0 — Founder Ratified)
4. Constitution authorizes architecture and governance — not implementation directly
5. Downstream ADRs and sprints derive authority from the ratified constitution

**Phase I baseline:** GAR-0001 through GAR-0016 are complete and frozen at v1.0.

**Phase II entry:** GAR-0017 establishes Phase II constitutional authority, including the
Constitutional Membrane and Interface Foundation authorization.

**Amendment path:** Constitutional change occurs only through the Architecture Change Proposal
process defined in GAR-0016. See Section 15 — Constitutional Evolution.

**Canonical example:** GAR-0017 was ratified before ADR-0011 and GAR-SPRINT-0010. No sprint or
mission may implement Phase II work without tracing authority to a ratified constitution.

---

## 4. Architectural Workflow

Architecture Decision Records translate constitutional authority into concrete architectural
decisions.

**Typical ADR lifecycle:**

1. Constitution authorizes an architectural domain (for example, Interface Foundation under GAR-0017)
2. Chief Systems Architect drafts ADR with context, decision, principles, and consequences
3. ADR is approved at a versioned status (for example, Approved v1.0)
4. Sprint specification operationalizes the ADR into implementable missions
5. Implementation remains subordinate to ADR boundaries

**ADR characteristics:**

- Subordinate to governing GAR constitution
- Records a specific architectural decision — not a sprint plan
- Defines principles, boundaries, and explicit exclusions
- Does not authorize coding — sprints do

**Canonical example:** ADR-0011 establishes the Interface Foundation as the exclusive realization
of the Constitutional Membrane. It defines eight architectural principles (exclusive boundary,
technology neutrality, canonical communication, and others) that Sprint 0010 missions implemented
without expanding ADR scope.

**Dependency rule:** Phase II foundations extend Phase I additively. ADRs SHALL NOT redefine
completed Internal Cognitive Foundations unless separately authorized through GAR-0016.

---

## 5. Sprint Workflow

A sprint specification converts architectural authority into an authorized sequence of missions.

**Typical sprint lifecycle:**

```
Constitution (ratified)
        ↓
ADR (approved)
        ↓
Sprint specification (approved)
        ↓
Mission Alpha → … → Mission India
        ↓
Certification (Mission Golf)
        ↓
SDK documentation (Mission Hotel)
        ↓
Institutional release (Mission India)
        ↓
Published release (tag)
        ↓
Governance baseline
```

**Sprint specification contents:**

- Sprint ID and name
- Constitutional and architectural authority references
- Scope and explicit exclusions
- Mission decomposition (typically Alpha through India)
- Dependency rules and additive evolution constraints
- Certification and documentation requirements

**Sprint rules:**

- One sprint closes before the next sprint is authorized
- Sprint closure does not automatically authorize the next sprint
- Historical sprint documents are not modified after closure
- Sprint 0010 is the Canonical Foundation Reference for Phase II

**Canonical example:** GAR-SPRINT-0010 implemented the Interface Foundation under GAR-0017 and
ADR-0011 across nine missions, producing certification, SDK documentation, release notes, and a
closure report before institutional release at `v0.10.0-alpha`.

---

## 6. Mission Workflow

Every sprint divides work into independent missions. Each mission follows the same engineering
discipline.

**Standard mission sequence:**

| Mission | Typical role |
| --- | --- |
| Alpha | Core framework and substrate |
| Bravo | Canonical contracts |
| Charlie | Lifecycle and boundary model |
| Delta | Translation or transformation layer |
| Echo | Validation framework |
| Foxtrot | Registry, workspace, or reference store |
| Golf | Platform integration and quality certification |
| Hotel | Foundation SDK documentation |
| India | Sprint closure and institutional release preparation |

Not every foundation requires identical mission names, but the sequence pattern — core → contracts
→ boundary → processing → validation → catalog → certification → documentation → release — is the
established Garuda Engineering Standard.

**Mission lifecycle:**

1. Read applicable GAR documents, ADR, sprint specification, and repository state
2. Produce mission implementation plan
3. Wait for architecture approval — no coding before approval
4. Implement only approved scope
5. Write tests
6. Update documentation
7. Run verification (mission tests, foundation tests, full suite, repository checks)
8. Architecture review
9. One mission, one commit
10. Completion report — do not begin next mission without approval

**Implementation plan requirements:**

- Objective and deliverables
- Explicit scope and exclusions
- Tests and documentation
- Verification commands
- Completion criteria

**Canonical example:** GAR-SPRINT-0010 Mission Alpha (`c38ab77`) established `InterfaceFoundation`
under `packages/interface/` with Platform Core inheritance. Each subsequent mission built on prior
commits with independent review IDs (GAR-REVIEW-S10-001 through GAR-REVIEW-S10-009).

---

## 7. Review Methodology

Architecture review confirms that completed work satisfies approved scope and constitutional
compliance before a mission is considered complete.

**Review inputs:**

- Mission implementation plan (approved scope)
- Delivered code, tests, and documentation
- Verification results
- Explicit exclusions and known limitations

**Review confirms:**

- Scope compliance — no unauthorized expansion
- Constitutional compliance — traceable to GAR and ADR authority
- Repository health — clean working tree, passing tests
- Exclusion adherence — no future-mission functionality
- Honest limitation reporting

**Review identifiers:** Sprint 0010 used structured review IDs (for example, GAR-REVIEW-S10-007 for
Mission Golf). Review approval is recorded before the mission commit is accepted as complete.

**Escalation:** Constitutional ambiguity discovered during review SHALL NOT be resolved by
implementation. Escalate through the GAR-0016 ACP process and stop until ratified guidance exists.

**Pass/fail gate:** A mission is not complete until review passes. Failed verification is reported
honestly — never suppressed.

---

## 8. Checkpoint Taxonomy

Garuda uses institutional checkpoints to record architectural and governance milestones. Checkpoints
are descriptive records — they do not authorize work.

**Checkpoint categories:**

| Category | Purpose | Example |
| --- | --- | --- |
| Architectural checkpoint | Records foundation or phase milestone | Checkpoint 025 — Phase II Reference Foundation Established |
| Governance checkpoint | Records baseline freeze or standard adoption | Checkpoint 027 — Phase II Governance Baseline Frozen |
| Release checkpoint | Records published release state | Checkpoint 026 — Phase II Release Published |

**Phase II checkpoints (Sprint 0010 completion):**

| Checkpoint | Name | Significance |
| --- | --- | --- |
| 025 | Phase II Reference Foundation Established | Interface Foundation is first completed Phase II foundation; GAR-0017 and ADR-0011 validated in practice |
| 026 | Phase II Release Published | `v0.10.0-alpha` published; repository internally consistent |
| 027 | Phase II Governance Baseline Frozen | Sprint 0010 elevated to Canonical Foundation Reference; Garuda Engineering Standard established |
| 028 | Constitutional Engineering Reference Manual Established | GAR-REFERENCE-0001 published; Reference Principle institutionalized |
| 029 | Governance Baseline Published | Post-release institutional stabilization complete; frozen baseline at `a3f2ba3` |

Checkpoints complement but do not replace sprint closure reports, certification records, or release
notes.

---

## 9. Certification Philosophy

Certification missions (typically Mission Golf) verify cross-foundation interoperability and
constitutional compliance. Certification is a constitutional obligation — not optional testing.

**Certification principles:**

- **Certification-only scope:** Golf missions introduce no new production functionality
- **Evidence-based records:** Every constitutional obligation maps to a verification scenario
- **Bidirectional traceability:** Forward (authority → scenario) and reverse (scenario → authority) matrices
- **Reproducibility:** Identical outcomes from a clean checkout using documented commands

**Certification record structure:**

- Mission scope statement
- Modules certified with mission attribution
- Verification workflow (exact commands)
- Traceability matrices linking GAR articles, ADR principles, sprint objectives, and scenarios
- Scenario descriptions and expected outcomes
- Defect classification policy — certification does not expand architecture

**Canonical example:** GAR-SPRINT-0010-interface-certification.md certifies ten constitutional
scenarios covering Platform Core inheritance, cognitive independence, boundary exclusivity,
translation containment, and registry catalog semantics. All scenarios passed at Mission Golf
commit `d542f51`.

**Certification Completeness Invariant:** Every constitutional obligation authorized by the sprint
SHALL have corresponding verification evidence before institutional release.

---

## 10. Developer Enablement

Developer enablement missions (typically Mission Hotel) produce SDK documentation that enables
external engineers to use a foundation correctly.

**SDK documentation model:**

- Located under `docs/sdk/<foundation>/`
- Covers developer guide, architecture guide, API reference, best practices, extension boundaries,
  and practical examples
- Documents only implemented public APIs — no speculative surfaces
- Verified against actual exports (Sprint 0010 achieved 80/80 public API coverage)

**Documentation Fidelity Invariant:** SDK documentation SHALL describe implemented behavior only
and SHALL remain synchronized with the public API surface at release time.

**Canonical example:** Interface Foundation SDK documentation under `docs/sdk/interface/` comprises
eight files: README, developer guide, architecture guide, API reference, best practices,
extension guide, and practical examples — all traceable to Mission Hotel commit `da111fe`.

**Extension boundaries:** SDK extension guides reference GAR-0016 for architectural changes that
exceed sprint scope. Documentation teaches boundaries; it does not authorize expansion.

---

## 11. Institutional Release

Institutional release missions (typically Mission India) close a sprint without introducing
production functionality. They produce the institutional record required for release readiness.

**India mission deliverables:**

- Sprint closure report with release manifest and implementation lineage
- Version consistency matrix across VERSION, CHANGELOG, release notes, and context documents
- Repository state snapshot (branch, commit, test count, working tree status)
- Sprint retrospective (informational — does not authorize future work)
- Release preparation checklists
- Confirmation that no new platform functionality was introduced

**Institutional Integrity Invariant:** Release artifacts SHALL reference the correct immutable
commit hashes. The authoritative mission commit and any post-closure alignment commits SHALL be
distinguished clearly. The release tag SHALL point to the finalized institutional record.

**Canonical example:** GAR-SPRINT-0010 Mission India closed at commit `fe34f8c`. A subsequent
documentation-only alignment commit (`369a93b`) corrected closure report hash references before
the `v0.10.0-alpha` tag was published — preserving traceability without reopening the sprint.

---

## 12. Release Process

Published releases mark the transition from institutional closure to an immutable tagged baseline.

**Release artifacts:**

| Artifact | Location | Purpose |
| --- | --- | --- |
| VERSION | Root `VERSION` file | Current version, architecture, sprint reference |
| CHANGELOG | `CHANGELOG.md` | Version history |
| Release notes | `docs/releases/v<version>.md` | Human-readable release summary |
| Closure report | `docs/sprints/GAR-SPRINT-*-closure-report.md` | Institutional audit record |
| Git tag | Annotated tag on finalized commit | Immutable release pointer |

**Typical release sequence:**

1. Mission India creates closure report and release notes
2. VERSION and CHANGELOG updated
3. Full regression suite verified
4. Founder approval for tag
5. Post-closure documentation alignment if required (separate commit)
6. Annotated Git tag created on finalized institutional record
7. Push commits and tag to origin
8. Governance baseline established (see below)

**Governance Baseline (terminal lifecycle stage):**

Published Release freezes the software artifact. Governance Baseline freezes the institutional
record around it:

1. Constitutional Engineering Reference Manual published (GAR-REFERENCE-0001)
2. Institutional context synchronized with published state
3. Sprint elevated to canonical exemplar
4. Repository history clean, auditable, and remote-published
5. Next sprint explicitly not authorized

**Canonical Phase II baseline (Sprint 0010):**

| Artifact | Value |
| --- | --- |
| Constitution | GAR-0017 v1.0 — Ratified |
| ADR | ADR-0011 v1.0 — Approved |
| Sprint | GAR-SPRINT-0010 — Closed |
| Release | `v0.10.0-alpha` |
| Mission India commit | `fe34f8c` |
| Alignment commit | `369a93b` |
| Tag | `v0.10.0-alpha` on `369a93b` |
| Reference manual | GAR-REFERENCE-0001 on `5b09b5e` |
| Governance baseline | `a3f2ba3` (Checkpoint 029) |
| Tests at release | 806 passed |

Tags are created only after explicit approval. One mission, one commit discipline applies to release
work as to all missions.

---

## 13. Governance Invariants

Governance invariants are engineering principles validated through Sprint 0010 practice. They
describe observed institutional discipline — authoritative rules remain in GAR documents and
approved sprint specifications.

**Documentation Fidelity Invariant**

SDK and engineering documentation SHALL describe implemented behavior only. Documentation SHALL
remain synchronized with the public API and verification state at release time. Hotel missions
enforce this through coverage verification.

**Institutional Integrity Invariant**

Release and closure artifacts SHALL maintain accurate commit references, version consistency, and
internal cross-reference integrity. Post-closure corrections that do not change architecture or
implementation are handled as separate documentation maintenance — not sprint reopening.

**Certification Completeness Invariant**

Every constitutional obligation authorized by a sprint SHALL have corresponding verification
evidence in the certification record before institutional release.

**Additive Evolution Invariant**

Phase II and future foundations SHALL extend prior foundations without redefining them. Phase I
modifications require GAR-0016 authorization.

**One Mission, One Commit Invariant**

Each mission produces exactly one verified commit. Multiple missions are never combined. The
repository remains clean between missions.

---

## 14. Engineering Conventions

**Bootstrap sequence for every mission:**

1. `AGENTS.md`
2. `GARUDA_CONTEXT.md`
3. `GARUDA_WORKFLOW.md`
4. `GARUDA_GLOSSARY.md`
5. `GARUDA_NAVIGATION.md`
6. Applicable GAR Constitutions
7. Approved sprint mission
8. Current repository state

**Verification commands:**

```bash
.venv/bin/python -m unittest tests.test_<mission>_*
.venv/bin/python -m unittest discover tests
.venv/bin/python scripts/run_checks.py
```

**Code quality expectations:**

- Deterministic and reproducible
- Immutable where appropriate
- Platform neutral and service independent
- Typed where appropriate
- Fully tested and documented

**Git discipline:**

- One mission, one commit
- Never combine missions
- Never commit unverified work
- Never modify unrelated packages
- Repository clean before next mission begins

**Completion report contents:**

- Files created and modified
- Commands executed
- Tests executed and results
- Documentation summary
- Commit hash
- Repository status
- Architecture review summary
- Known limitations

**Permanent prohibitions (observed across all foundations):**

- No trading, portfolio, or broker integrations
- No AI reasoning behavior in foundation packages
- No database persistence
- No REST endpoints or frontend features
- No event bus, deployment, scheduling, or orchestration engines
- No execution behavior outside approved scope

**Recovery procedure:** When uncertainty exists — stop. Re-read authority hierarchy sources.
Never guess architecture.

---

## 15. Constitutional Evolution

One of the greatest risks in mature systems is unnecessary constitutional churn. This section
teaches engineers when to use — and when not to use — the GAR-0016 Architecture Change Proposal
process.

### When GAR-0016 ACPs are appropriate

An ACP is required when change would:

- amend or supersede a ratified GAR constitution
- redefine constitutional terms or authority boundaries
- invalidate or replace a completed Internal Cognitive Foundation
- introduce governance law not covered by existing constitutions
- resolve genuine constitutional ambiguity that blocks authorized work

**Examples requiring ACP:**

- Amending GAR-0017 to authorize a new constitutional boundary type
- Redefining "Foundation" in a way that changes dependency law across Phase I
- Modifying a frozen Phase I foundation package when additive extension is insufficient

### When GAR-0016 ACPs are not appropriate

An ACP is not required when change is:

- a bug fix within approved sprint scope
- documentation maintenance or synchronization
- an engineering or process refinement
- an architectural decision properly handled by a new ADR under existing constitutional authority
- a sprint-level implementation within an already-authorized domain

**Sprint 0010 examples (no ACP required):**

| Observation | Classification | Resolution |
| --- | --- | --- |
| Closure report referenced pre-amend commit hashes | Documentation maintenance | Alignment commit `369a93b`; sprint not reopened |
| Catalog vs container registry distinction | Engineering refinement within ADR scope | Implemented in Mission Foxtrot under ADR-0011 |
| Bidirectional traceability matrices | Process refinement | Adopted in Golf certification methodology |
| Institutional Integrity Invariant | Governance practice | Codified in release workflow; no constitutional change |
| Post-release `GAR-CODEX-CONTEXT.md` drift | Documentation synchronization | Standalone maintenance commit; not Sprint 0010 correction |

No constitutional ambiguity remained after Sprint 0010. No architectural contradiction emerged. No
dependency inversion was violated. GAR-0016 remains untouched.

### Change classification guide

| Change type | Typical handling | ACP required? |
| --- | --- | --- |
| Bug fix | Mission or maintenance commit within scope | No |
| Documentation maintenance | Standalone docs commit; preserve closed sprint immutability | No |
| Engineering refinement | Mission implementation under existing ADR | No |
| Architectural evolution | New or amended ADR under existing constitution | No |
| Constitutional evolution | GAR-0016 Architecture Change Proposal | Yes |

When in doubt, classify upward conservatively — propose an ACP rather than silently amending
constitutional interpretation. The Chief Systems Architect and Founder determine whether an ACP is
truly required.

---

## 16. Canonical Reference Index

Sprint 0010 (Interface Foundation) is the Canonical Foundation Reference for Phase II. Future
foundational sprints should inherit — not recreate — these institutional assets.

### Constitutional chain

| Document | Location |
| --- | --- |
| GAR-0017 — Phase II Constitutional Extension | [GAR-0017.md](GAR-0017.md) |
| ADR-0011 — Interface Foundation | [docs/adr/ADR-0011-interface-foundation.md](docs/adr/ADR-0011-interface-foundation.md) |
| GAR-SPRINT-0010 specification | [docs/sprints/GAR-SPRINT-0010-interface-foundation.md](docs/sprints/GAR-SPRINT-0010-interface-foundation.md) |

### Mission implementation plans

| Mission | Plan |
| --- | --- |
| Alpha | [GAR-SPRINT-0010-mission-alpha-implementation-plan.md](docs/sprints/GAR-SPRINT-0010-mission-alpha-implementation-plan.md) |
| Bravo | [GAR-SPRINT-0010-mission-bravo-implementation-plan.md](docs/sprints/GAR-SPRINT-0010-mission-bravo-implementation-plan.md) |
| Charlie | [GAR-SPRINT-0010-mission-charlie-implementation-plan.md](docs/sprints/GAR-SPRINT-0010-mission-charlie-implementation-plan.md) |
| Delta | [GAR-SPRINT-0010-mission-delta-implementation-plan.md](docs/sprints/GAR-SPRINT-0010-mission-delta-implementation-plan.md) |
| Echo | [GAR-SPRINT-0010-mission-echo-implementation-plan.md](docs/sprints/GAR-SPRINT-0010-mission-echo-implementation-plan.md) |
| Foxtrot | [GAR-SPRINT-0010-mission-foxtrot-implementation-plan.md](docs/sprints/GAR-SPRINT-0010-mission-foxtrot-implementation-plan.md) |
| Golf | [GAR-SPRINT-0010-mission-golf-implementation-plan.md](docs/sprints/GAR-SPRINT-0010-mission-golf-implementation-plan.md) |
| Hotel | [GAR-SPRINT-0010-mission-hotel-implementation-plan.md](docs/sprints/GAR-SPRINT-0010-mission-hotel-implementation-plan.md) |
| India | [GAR-SPRINT-0010-mission-india-implementation-plan.md](docs/sprints/GAR-SPRINT-0010-mission-india-implementation-plan.md) |

### Institutional artifacts

| Artifact | Location |
| --- | --- |
| Certification record | [docs/sprints/GAR-SPRINT-0010-interface-certification.md](docs/sprints/GAR-SPRINT-0010-interface-certification.md) |
| Closure report | [docs/sprints/GAR-SPRINT-0010-closure-report.md](docs/sprints/GAR-SPRINT-0010-closure-report.md) |
| Release notes | [docs/releases/v0.10.0-alpha.md](docs/releases/v0.10.0-alpha.md) |
| SDK documentation | [docs/sdk/interface/README.md](docs/sdk/interface/README.md) |
| Implementation | [packages/interface/](packages/interface/) |

### Governance and workflow documents

| Document | Location |
| --- | --- |
| AI engineering operating manual | [AGENTS.md](AGENTS.md) |
| Engineering workflow | [GARUDA_WORKFLOW.md](GARUDA_WORKFLOW.md) |
| Engineering governance baseline | [ENGINEERING_GOVERNANCE_v1.0.md](ENGINEERING_GOVERNANCE_v1.0.md) |
| Repository context | [GARUDA_CONTEXT.md](GARUDA_CONTEXT.md) |
| Codex context | [GAR-CODEX-CONTEXT.md](GAR-CODEX-CONTEXT.md) |

### Published lifecycle (Garuda Engineering Standard)

```
Constitution
        ↓
Architecture
        ↓
Sprint
        ↓
Mission Planning
        ↓
Implementation
        ↓
Verification
        ↓
Certification
        ↓
Developer Enablement
        ↓
Institutional Release
        ↓
Published Release
        ↓
Governance Baseline
```

---

## 17. What This Document Is Not

To prevent authority confusion, this section states explicit boundaries.

| GAR-REFERENCE-0001 is | GAR-REFERENCE-0001 is not |
| --- | --- |
| A descriptive onboarding reference | A GAR constitution |
| An organizational guide to existing workflows | An ADR recording a decision |
| A cross-reference index to canonical examples | A sprint specification authorizing work |
| A teaching document for constitutional evolution discipline | A mission implementation plan |
| A snapshot of engineering culture at publication | A substitute for repository state |

**If this document conflicts with:**

- A GAR constitution → the constitution prevails
- An approved ADR → the ADR prevails
- An approved sprint specification → the sprint specification prevails
- Committed repository state → the repository prevails

**This document does not:**

- Authorize Sprint 0011 or any future work
- Amend GAR-0016, GAR-0017, or any frozen constitutional document
- Redefine the Interface Foundation or any completed foundation
- Replace architecture review or Founder ratification
- Create new governance law

When engineering process evolves, this reference may be revised in a future GAR-REFERENCE version.
Revisions remain descriptive. Constitutional change always flows through GAR-0016.

---

End of GAR-REFERENCE-0001
