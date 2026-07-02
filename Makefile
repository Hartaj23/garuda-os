.PHONY: validate test toolchain-check

validate:
	python3 scripts/run_checks.py

test:
	python3 -m unittest discover tests

toolchain-check:
	python3 scripts/validate_toolchain.py
