
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

	nohup poetry run uvicorn \
		--host=0.0.0.0 \
		--port=8000 \
		builder.app:app \
		> uvicorn.log 2>&1 & echo "$$!" > pidfile

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

	cat uvicorn.log
	find out/ -type f

	rm -f pidfile
	rm -f uvicorn.log
