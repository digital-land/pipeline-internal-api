.DEFAULT_GOAL := help

help:
	@echo
	@echo "    ____  __                  _                ____        __       "
	@echo "   / __ \/ /___ _____  ____  (_)___  ____ _   / __ \____ _/ /_____ _"
	@echo "  / /_/ / / __ \`/ __ \/ __ \/ / __ \/ __ \`/  / / / / __ \`/ __/ __ \`/"
	@echo " / ____/ / /_/ / / / / / / / / / / / /_/ /  / /_/ / /_/ / /_/ /_/ / "
	@echo "/_/   /_/\__,_/_/ /_/_/ /_/_/_/ /_/\__, /  /_____/\__,_/\__/\__,_/  "
	@echo "                                  /____/                            "
	@echo
	@echo "Usage: make <action>"
	@echo
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-10s\033[0m %s\n", $$1, $$2}'
	@echo



.PHONY: init
init: ## # installs all python dependencies for the project, including test dependencies
	python -m pip install --upgrade pip
	python -m pip install -r requirements/test_requirements.txt

.PHONY:  upgrade
upgrade: ## # upgrade package versions in the lock files (requirements.txt and test_requirements.txt), the python version is fixed by .python-version
	@test "$$(python -c 'import sys; print("%d.%d" % sys.version_info[:2])')" = "$$(cat .python-version)" \
		|| (echo "python version does not match .python-version, activate the right virtualenv" && exit 1)
	pip-compile --upgrade requirements/requirements.in
	pip-compile --upgrade requirements/test_requirements.in
	python -m pip install -r requirements/test_requirements.txt

.PHONY: compose-up
compose-up: ## run the docker compose file in detached mode, building the images first
	docker compose up -d --build

.PHONY: test
test: lint test-coverage ## run all tests and check code coverage, linting is also run as part of this target

.PHONY: test-coverage
test-coverage:: coverage-unit coverage-integration

.PHONY: coverage-unit
coverage-unit:
	pytest --cov=src tests/unit/

.PHONY: coverage-integration
coverage-integration:
	pytest --cov=src --cov-append --cov-fail-under=80 tests/integration/

.PHONY: lint
lint:: black-check flake8 ## run lint checks on all code, do not actually change the code though

.PHONY: format
format:: black ## run code formatting on all code, this will change the code to match the formatting rules

.PHONY: black-check
black-check:
	black --check .

.PHONY:  black
black:
	black .

.PHONY: flake8
flake8:
	flake8 .