# Integration Foundation SDK Troubleshooting Guide

## Documentation Provenance

| Field | Value |
| --- | --- |
| Governing Constitution | [GAR-0018](../../../GAR-0018.md) |
| Governing ADR | [ADR-0012](../../adr/ADR-0012-integration-foundation.md) |
| Governing Sprint | [GAR-SPRINT-0011](../../sprints/GAR-SPRINT-0011-integration-foundation.md) |
| Repository baseline | `121365c` |

## Validation Failures

### Symptom: `invalid_validation_artifact_type`

**Cause:** A non-integration artifact was passed to `evaluate_integration_artifact()`.

**Resolution:** Pass only canonical Integration Foundation artifacts whose `object_type` is listed in
`CANONICAL_INTEGRATION_ARTIFACT_TYPES`.

### Symptom: `policy_target_mismatch`

**Cause:** The validation policy target does not match the artifact `object_type`.

**Resolution:** Align `IntegrationValidationPolicy.target_object_type` with the artifact being evaluated.

### Symptom: `interface_subordination_mismatch`

**Cause:** Subordination match validation was requested with a non-matching interface contract reference.

**Resolution:** Pass the exact canonical interface contract used to build subordination metadata.

## Registry Failures

### Symptom: `Registry entry already exists`

**Cause:** Duplicate `registration_identifier` registration.

**Resolution:** Use a new identifier or lookup the existing entry instead of re-registering.

### Symptom: `registry_artifact_type_mismatch`

**Cause:** Participant descriptor artifact type does not match the supplied integration artifact.

**Resolution:** Set `IntegrationParticipantDescriptor.artifact_object_type` to the artifact's
`object_type`.

### Symptom: `invalid_artifact_object_type`

**Cause:** Descriptor references an artifact type outside `CANONICAL_INTEGRATION_ARTIFACT_TYPES`.

**Resolution:** Use one of the published canonical integration artifact types only.

## Contract Failures

### Symptom: `invalid_interface_contract_object_type`

**Cause:** Subordination references a non-canonical interface contract type.

**Resolution:** Subordinate only to `CanonicalInterfaceRequest` or `CanonicalInterfaceResponse`.

## Serialization Surprises

### Symptom: Metadata key order differs between dict input and output

**Cause:** Metadata dataclasses normalize dictionary inputs to sorted tuples.

**Resolution:** Compare using `to_dict()` rather than raw constructor inputs.

## When To Stop Troubleshooting And Escalate

Stop local troubleshooting and request architectural review when:

- the required behavior is operational integration, transport, or provider execution
- the fix requires modifying Phase I or Interface packages
- the fix requires new Integration Foundation production behavior not present at baseline `121365c`

These cases require constitutional or sprint authorization — not SDK usage changes.

## Related Documents

- [Developer Guide](developer-guide.md)
- [API Reference](api-reference.md)
