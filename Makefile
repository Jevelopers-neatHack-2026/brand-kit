PYTHON ?= python3

.PHONY: check-governance check-inventory check-links check-links-external check-provenance-register check-provenance test check

check-inventory:
	$(PYTHON) tools/check_inventory.py

check-governance:
	$(PYTHON) -I tools/check_governance.py

check-links:
	$(PYTHON) tools/check_links.py

# Structural validation of provenance/: coverage, exact hashes, paths, field presence. Honest UNKNOWNs pass.
check-provenance-register:
	$(PYTHON) -I tools/check_provenance.py --register-only

# Production export eligibility. Fails closed (nonzero) until a reviewed allowlist and cleared core rights exist.
# Deliberately not part of `check`.
check-provenance:
	$(PYTHON) -I tools/check_provenance.py

# Network probe; non-deterministic and not part of `check`.
check-links-external:
	$(PYTHON) tools/check_links.py --external

test:
	$(PYTHON) -m unittest discover -s tools/tests -v

check: check-inventory check-links check-governance check-provenance-register test
