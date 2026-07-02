.PHONY: bootstrap backend frontend dev validate test lint format toolchain-check

bootstrap:
	python3 scripts/dev_setup.py bootstrap

backend:
	python3 scripts/dev_setup.py backend

frontend:
	python3 scripts/dev_setup.py frontend

dev:
	python3 scripts/dev_setup.py dev

validate:
	python3 scripts/run_checks.py

test:
	python3 -m unittest discover tests

lint:
	python3 -m ruff check . && npm --prefix apps/web run lint

format:
	python3 -m black . && npm --prefix apps/web run format

toolchain-check:
	python3 scripts/validate_toolchain.py
