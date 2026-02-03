run:
	rsync -av src/code.py /Volumes/CIRCUITPY/

settings:
	rsync -av src/settings.toml /Volumes/CIRCUITPY/

lib:
	rsync -av src/lib /Volumes/CIRCUITPY/

font:
	rsync -av src/fonts /Volumes/CIRCUITPY/

bmp:
	rsync -av src/bmp /Volumes/CIRCUITPY/

util:
	rsync -av src/util /Volumes/CIRCUITPY/

all:
	rsync -av src/code.py src/lib src/settings.toml /Volumes/CIRCUITPY/