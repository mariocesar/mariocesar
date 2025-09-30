# Default recipe runs sync
default:
    uv sync

# Run development server with hot reload
serve:
    uv run uvicorn --reload --port=8000 builder.app:app

# Build static site by mirroring from running server
build:
    rm -rf out
    rm -f pidfile

    nohup uv run uvicorn \
        --host=127.0.0.1 \
        --port=8000 \
        builder.app:app \
        > uvicorn.log 2>&1 & echo $! > pidfile

    @echo "Waiting for launch 8000..."

    while ! nc -z localhost 8000; do sleep 0.1; done

    @echo "Webapp launched"

    wget \
        --mirror \
        --adjust-extension \
        --convert-links \
        --page-requisites \
        --no-host-directories \
        --retry-on-host-error \
        --tries 10 \
        --timeout 10 \
        -P out \
        --input-file mirror.list

    kill $(cat pidfile)

    cat uvicorn.log
    find out/ -type f

    rm -f pidfile
    rm -f uvicorn.log
