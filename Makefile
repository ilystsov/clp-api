CODE_FOLDERS := src
TEST_FOLDERS := tests

.PHONY: test format lint security_checks

test:
	poetry run pytest $(TEST_FOLDER) --cov=$(CODE_FOLDERS)

format:
	poetry run black --line-length 79 .

lint:
	poetry run black --line-length 79 --check $(CODE_FOLDERS) $(TEST_FOLDERS)
	poetry run flake8 $(CODE_FOLDERS) $(TEST_FOLDERS)
	poetry run ruff check $(CODE_FOLDERS) $(TEST_FOLDERS)

security_checks:
	poetry run bandit -r $(CODE_FOLDERS)