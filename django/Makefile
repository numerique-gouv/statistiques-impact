# Make commands for dev environment

lint: ## Lint Python files
	ruff format && ruff check --fix
.PHONY: lint

test: ## Run back-end tests. --no-migrations option is passed because of weird 
	pytest --no-migrations
.PHONY: lint