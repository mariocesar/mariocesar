
defualt:
	poetry install

fix:
	poetry run isort src/
	poetry run black src/
	poetry run flake8 src/

check:
	poetry run isort --diff --check src/
	poetry run black --diff --check src/
	poetry run flake8 src/

build:
	rm -rf out
	poetry run python -m builder
