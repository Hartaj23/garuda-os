# Engineering Toolchain Foundation

Mission Bravo configures the maintainability toolchain authorized by GAR-SPRINT-0001.

## Tool Decisions

### Python Package Manager

Python dependency metadata is centralized in `pyproject.toml`. The project uses the standard Python packaging interface so future backend work can add dependencies without changing repository shape.

Why selected:

- It is the current Python packaging standard.
- Black and Ruff read configuration from it directly.
- It avoids introducing backend application code during the toolchain milestone.

Note: `pyproject.toml` uses the Python-compatible normalized version `0.1.0a0`; the root `VERSION` file preserves the product version label `0.1.0-alpha`.

### Node Package Manager

Node workspace management uses pnpm, configured through `package.json` and `pnpm-workspace.yaml`.

Why selected:

- It supports monorepos cleanly.
- It keeps dependency installation deterministic once lockfiles are generated.
- It aligns with a workspace model for future `apps`, `packages`, `services` and `agents` work.

### Black

Black is configured in `pyproject.toml` for deterministic Python formatting.

### Ruff

Ruff is configured in `pyproject.toml` for fast Python linting and import checks.

### Prettier

Prettier is configured through `.prettierrc.json` for JavaScript, TypeScript, JSON, Markdown and related text formatting.

### ESLint

ESLint is configured through `eslint.config.mjs` using the modern flat config format.

### Pre-commit Hooks

Pre-commit is configured in `.pre-commit-config.yaml` to run Ruff, Black and Prettier before commits once dependencies are installed.

## Local Workflow

Run all current foundation checks:

```bash
python3 scripts/run_checks.py
```

Equivalent make target:

```bash
make validate
```

Run tests only:

```bash
python3 -m unittest discover tests
```

Run toolchain validation only:

```bash
python3 scripts/validate_toolchain.py
```

## Scope Boundary

This milestone configures toolchain metadata only. It does not implement backend services, frontend application logic, Docker, CI/CD, database, authentication, trading or AI functionality.
