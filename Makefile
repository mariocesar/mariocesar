
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
	rm -f pidfile

	poetry run uvicorn --port 8000 --workers 2 builder.app:app & echo "$$!" > pidfile

	wget \
		--mirror \
		--adjust-extension \
		--convert-links \
		--page-requisites \
		--no-host-directories \
		--timeout 10 \
		-P out \
		http://localhost:8000

	kill $$(cat pidfile)

	rm -f pidfile