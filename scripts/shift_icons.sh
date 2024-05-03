#! /bin/bash

# convert               use imagemagick
# -repage               set location of image (shift)
# -background none      fill empty space with alpha
# -flatten              compose image
# PNG32:                keep four color channels
COMMAND="convert -page -2+2 {} -background none -flatten PNG32:{}"
DIRECTORY='../static/images/default/'

find $DIRECTORY -maxdepth 1 -iname '*.png' -exec sh -c "$COMMAND" \;
