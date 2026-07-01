# Security Policy

Security is part of the Garuda governance layer and is mandatory for every implementation.

## Current Status

GAR-SPRINT-0001 establishes repository and engineering foundations only. Authentication, authorization, broker APIs and secrets infrastructure are out of scope for this task.

## Security Requirements

- Secrets must never be committed.
- Environment files are ignored except documented examples.
- Dependencies must be reviewed before use.
- Sensitive information must not appear in logs.
- Least privilege is the default operating principle.

## Reporting

Report security concerns to the repository owner. Do not disclose suspected vulnerabilities publicly before maintainers have reviewed them.

