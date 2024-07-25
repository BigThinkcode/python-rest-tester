help: ## Display this help message
	@echo "Available commands:"
	@echo "[For docker related]"
	@awk 'BEGIN {FS = ":.*?##"}; /^[a-zA-Z0-9_-]+:.*?##/ {if ($$0 ~ /\(docker\)/) {sub(" \\(docker\\)", "", $$2); printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}}' $(MAKEFILE_LIST) | sort
	@echo "[For app related]"
	@awk 'BEGIN {FS = ":.*?##"}; /^[a-zA-Z0-9_-]+:.*?##/ {if ($$0 ~ /\(app\)/) {sub(" \\(app\\)", "", $$2); printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}}' $(MAKEFILE_LIST) | sort


run-dev-shell: ## Run the application in Dev mode once build completed as interactive shell(docker)
	sudo docker compose -f deployment/dev-docker-compose.yml run --rm -i --entrypoint bash rest_tester

run-dev: ## Run the application in Dev mode once build completed straight away (docker)
	sudo docker compose -f deployment/dev-docker-compose.yml run rest_tester make test-with-report

run-prod: ## Run the application in Prod mode once build completed (docker)
	sudo docker compose -f deployment/prod-docker-compose.yml run rest_tester make test-with-report

local-remove-images: ## Removes locally present dangling images (docker)
	sudo docker image prune -f



lint: ## Lint (app)
	poetry run python3 -m black --line-length 120 .

check-lint: ## Check Lint (app)
	poetry run python3 -m black --check --line-length 120 .

test: ## To performs all tests (app)
	poetry run pytest rest_tester/main.py -s -rA

test-with-report: ## To performs all tests and generate a HTML report file (app)
	poetry run pytest rest_tester/main.py -s -rA --html=rest_tester/report/report_`date +%Y-%m-%d-%H:%M:%S`.html --css=rest_tester/report/assets/custom.css --self-contained-html