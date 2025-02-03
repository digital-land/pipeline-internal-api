compose-up:
	docker compose up -d --build

test: lint test-coverage

test-coverage:: coverage-unit coverage-integration

coverage-unit:
	pytest --cov=src tests/unit/

coverage-integration:
	pytest --cov=src --cov-append --cov-fail-under=75 tests/integration/

lint:: black-check flake8

black-check:
	black --check .

black:
	black .

flake8:
	flake8 .