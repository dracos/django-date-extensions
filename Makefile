define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

.PHONY: black
black: ## code-formatting with black
		black approximate_date examples setup.py 

.PHONY: help
help:
		@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)
