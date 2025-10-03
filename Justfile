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

# Generate favicon assets from the source icon
build-favicon:
    #!/usr/bin/env bash
    set -euo pipefail

    src="public/static/icons/icon.jpg"
    out_dir="public/static/icons"
    sizes=(16 32 48 256 512)

    for size in "${sizes[@]}"; do
        size_px="${size}x${size}"

        magick "$src" \
            -resize "${size_px}^" \
            -gravity center \
            -extent "$size_px" \
            -strip \
            "$out_dir/icon-${size}.png"

        cx=$((size / 2))
        mask="circle ${cx},${cx} ${cx},0"

        magick "$src" \
            -resize "${size_px}^" \
            -gravity center \
            -extent "$size_px" \
            -alpha set \
            -background none \
            \( -size "$size_px" xc:none -fill white -draw "$mask" \) \
            -compose copyopacity \
            -composite \
            -strip \
            "$out_dir/icon-${size}.png"
    done

    magick \
        -gravity center \
        -background transparent \
        public/static/icons/icon-16.png \
        public/static/icons/icon-32.png \
        public/static/icons/icon-48.png \
        public/static/icons/icon-256.png \
        public/favicon.ico