# Developer Setup

## Current Task

GAR-SPRINT-0001 Task 1 establishes the repository foundation.

## Requirements

- Git
- Python 3

Backend, frontend, Docker and CI dependencies will be added in later GAR-SPRINT-0001 tasks.

## Validate the Foundation

```bash
python3 -m unittest discover tests
```

## Notes

Do not add secrets to the repository. Use environment examples only when environment configuration is implemented.


## Toolchain

Mission Bravo configures Python metadata in `pyproject.toml` and Node workspace metadata with pnpm. See `docs/engineering/toolchain.md` for decisions and commands.

Run all current foundation checks:

```bash
python3 scripts/run_checks.py
```
