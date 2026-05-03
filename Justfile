# Default recipe runs sync
default:
    uv sync

# Build static site
build:
    uv run python -m builder.build

# Build, serve, rebuild, and browser-reload on file changes
serve:
    uv run python -m builder.serve

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
