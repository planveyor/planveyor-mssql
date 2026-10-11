# Preserve JUNIT literally: neither make nor the recipe evaluates path contents.
override JUNIT := $(value JUNIT)
export JUNIT

.PHONY: setup db-extract db-build lint test check-secrets db-proof db-state
setup db-extract db-build lint test check-secrets db-proof db-state:
	@python3 -B scripts/sql.py $@
