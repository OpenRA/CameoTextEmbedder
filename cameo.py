#!/usr/bin/env python2

# Place this script as
# C:\Program Files\GIMP 2\lib\gimp\2.0\plug-ins\ra1-cameo.py
# or something so that GIMP will detect this as a plugin.
# On Linux, it is might be ~/.config/GIMP/2.10/plug-ins/ra1-cameo.py,
# make sure it is EXECUTABLE by running chmod +x ra1-cameo.py command.
# Then this will be visible in Filters --> Python-fu --> RA1 Cameo Text
#
# Please modify the FONT variable accordingly.
# You CAN use this script for RA2 if you provide the right data.
#
# Please take a look at the official plugin if you want more examples.
# https://github.com/GNOME/gimp/blob/master/plug-ins/python/

from gimpfu import *
import os

FONT = os.path.join(gimp.directory, "ra1_cameo_font")

LETTER_WIDTH = {
    "0": 4, "1": 3, "2": 4, "3": 5, "4": 5,
    "5": 4, "6": 4, "8": 5, "9": 5, "a": 5,
    "b": 5, "c": 5, "d": 5, "e": 5, "f": 5,
    "g": 5, "h": 5, "i": 2, "j": 5, "k": 5,
    "l": 5, "m": 6, "n": 6, "o": 5, "p": 5,
    "q": 5, "r": 5, "s": 5, "t": 4, "u": 5,
    "v": 6, "w": 6, "x": 6, "y": 6, "z": 4,
    " ": 2
}

# Cameo width, of course
WIDTH = 64
HEIGHT = 48

# Assertion: cameo size is 64x48.
# Letters will be placed at y of...
COORD_Y = 42


def compute_width(letters):
    w = 0
    for letter in letters:
        w += LETTER_WIDTH[letter]
    return w


def put_letters(image, drawable, letters, x):
    text_layer = pdb.gimp_layer_new(image, WIDTH, HEIGHT, 1, "text", 100, 0)
    pdb.gimp_image_insert_layer(image, text_layer, None, -1)

    for letter in letters:
        if letter == " ":
            x += LETTER_WIDTH[letter]
            continue

        charf = letter + ".png"
        charf = os.path.join(FONT, charf)

        layer = pdb.gimp_file_load_layer(image, charf)
        pdb.gimp_layer_translate(layer, x, COORD_Y)
        pdb.gimp_image_insert_layer(image, layer, None, -1)
        pdb.gimp_image_merge_down(image, layer, 0)
        x += LETTER_WIDTH[letter]


def put_bg(image):
    layer = pdb.gimp_layer_new(image, WIDTH, 7, 1, "bg", 100, 0)
    pdb.gimp_image_insert_layer(image, layer, None, -1)

    pdb.gimp_context_set_foreground((0, 0, 0))
    pdb.gimp_drawable_fill(layer, 0)
    pdb.gimp_layer_set_opacity(layer, 50)
    pdb.gimp_layer_translate(layer, 0, COORD_Y - 1)


def add_ra1_text(img, drawable, words):
    # split char by char.
    letters = words.lower()
    width = compute_width(letters)

    # Letter starts at x:
    x = (WIDTH - width) // 2
    # slightly to the right, if odd
    if (WIDTH - width) % 2 == 1:
        x += 1

    pdb.gimp_image_undo_group_start(img)
    put_bg(img)
    put_letters(img, drawable, letters, x)
    pdb.gimp_image_undo_group_end(img)


register(
    "python-fu-ra1-cameo-text",
    "Add text to the cameo image",
    "Add text to the cameo image",
    "BoolBada",
    "BoolBada",
    "2017,2021",
    "RA1 Cameo Text...",
    "RGB*, GRAY*",
    [
        (PF_IMAGE,    "img",       "Input image", None),
        (PF_DRAWABLE, "drawable",  "Input drawable", None),
        (PF_STRING,   "words", "Text", "Unit Name")
    ],
    [],
    add_ra1_text,
    menu="<Image>/Filters/CnC Modding/RA1 Cameo Text",
    domain=("gimp20-python", gimp.locale_directory)
    )

main()
