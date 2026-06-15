# Make commands for dev environment

lint: ## Lint Python files
	ruff format && ruff check --fix
.PHONY: lint

test: ## Run back-end tests
	uv run pytest
.PHONY: lint