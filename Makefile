iconsizes = 16 32 48 256 512
iconnames = $(addsuffix .png, $(addprefix src/icons/icon-, $(iconsizes)))
# brew install imagemagick

src/app/favicon.ico: $(iconnames)
	convert \
		-background transparent \
		src/icons/icon-16.png \
		src/icons/icon-32.png \
		src/icons/icon-48.png \
		src/icons/icon-256.png \
		src/app/favicon.ico

$(iconnames): src/icons/icon-%.png:
	$(eval half_width=$(shell echo "$* / 2" | bc))
	convert src/icons/icon.jpg \
		-resize $*x$*^ \
		-gravity center \
		-background none \
		-extent $*x$* \
		-alpha set \
		\( +clone -threshold -1 -negate -fill white -draw "circle $(half_width),$(half_width) $(half_width),0" \) \
		-compose copy_opacity \
		-composite \
		$@
