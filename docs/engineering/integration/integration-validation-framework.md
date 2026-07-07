# Integration Validation Framework

## Implementation Summary

GAR-SPRINT-0011 Mission Echo adds the deterministic validation framework under
`packages/integration/validation/`.

The implementation is intentionally limited:

- pure evaluator with no side effects
- immutable validation policies and rule models
- canonical integration artifact validation only
- structural error contracts only
- deterministic aggregation and reporting

## Public Interface

```python
from packages.integration import (
    IntegrationSubordinationRule,
    IntegrationValidationPolicy,
    IntegrationValidationTarget,
    IntegrationVersionCompatibilityRule,
    build_integration_validation_report,
    evaluate_integration_artifact,
    validation_result_to_outcome,
)

policy = IntegrationValidationPolicy(
    policy_identifier="canonical-integration-contract:v1",
    validation_target=IntegrationValidationTarget.CONTRACT,
    target_object_type="CanonicalIntegrationContract",
    subordination_rule=IntegrationSubordinationRule(
        require_valid_subordination=True,
        require_interface_contract_match=True,
    ),
)

result = evaluate_integration_artifact(contract, policy, interface_contract=interface_request)
outcome = validation_result_to_outcome(result)
report = build_integration_validation_report(result)
```

## Validation Aggregation and Reporting

Use `compose_integration_validation_results()` to merge Platform Core `ValidationResult` values
in deterministic order. Use `build_integration_validation_report()` to aggregate multiple evaluation
results into an immutable `IntegrationValidationReport`.

Use `compose_cross_model_integration_validation()` when multiple validation policies must be applied
to a single artifact.

## Engineering Boundaries

Do not validate transport envelopes, provider payloads, credentials, authentication, runtime
execution state, or registry entries.

Do not add business validation rules, operational integration behavior, SDK examples, or persistence.

Do not modify frozen Mission Alpha–Delta production modules except cumulative export wiring.

## Related Documents

- [Integration Validation Framework Architecture Guide](../../architecture/integration/integration-validation-framework.md)
- [Integration Foundation Overview](../../architecture/integration/overview.md)
