#!/usr/bin/env python2

# Place this script as
# C:\Program Files\GIMP 2\lib\gimp\2.0\plug-ins\cameo.py
# or something so that GIMP will detect this as a plugin.
# On Linux, it is might be ~/.config/GIMP/2.10/plug-ins/cameo.py,
# make sure it is EXECUTABLE by running chmod +x cameo.py command.
# Then this will be visible in Filters --> Cnc Modding --> RA1 Cameo Text
#
# Please modify the FONT_DIR and LETTER_WIDTH variables accordingly.
# You CAN use this script for more games if you provide the right data.
#
# Please take a look at the official plugin if you want more examples.
# https://github.com/GNOME/gimp/blob/master/plug-ins/python/

from gimpfu import *
import os

FONT_DIR = {
    "ra1": os.path.join(gimp.directory, "cameo_font/ra1"),
    "ra2": os.path.join(gimp.directory, "cameo_font/ra2"),
    "ra2_gloss": os.path.join(gimp.directory, "cameo_font/ra2_gloss"),
}

LETTER_WIDTH = {
    "ra1": {
        "0": 4, "1": 3, "2": 4, "3": 5, "4": 5,
        "5": 4, "6": 4, "7": 5, "8": 5, "9": 5,
        "a": 5, "b": 5, "c": 5, "d": 5, "e": 5,
        "f": 5, "g": 5, "h": 5, "i": 2, "j": 5,
        "k": 5, "l": 5, "m": 6, "n": 6, "o": 5,
        "p": 5, "q": 5, "r": 5, "s": 5, "t": 4,
        "u": 5, "v": 6, "w": 6, "x": 6, "y": 6,
        "z": 4,
        " ": 2  # " " is a dummy and has no PNG image
    },
    "ra2": {
        "0": 5, "1": 4, "2": 5, "3": 5, "4": 5,
        "5": 5, "6": 5, "7": 5, "8": 5, "9": 5,
        "a": 5, "b": 5, "c": 5, "d": 5, "e": 4,
        "f": 4, "g": 5, "h": 5, "i": 2, "j": 4,
        "k": 5, "l": 4, "m": 6, "n": 5, "o": 5,
        "p": 5, "q": 5, "r": 5, "s": 5, "t": 4,
        "u": 5, "v": 6, "w": 6, "x": 5, "y": 6,
        "z": 5,
        " ": 2
    },
    "ra2_gloss": {
        "0": 5, "1": 4, "2": 5, "3": 5, "4": 5,
        "5": 5, "6": 5, "7": 5, "8": 5, "9": 5,
        "a": 5, "b": 5, "c": 5, "d": 5, "e": 4,
        "f": 4, "g": 5, "h": 5, "i": 2, "j": 4,
        "k": 5, "l": 4, "m": 6, "n": 5, "o": 5,
        "p": 5, "q": 5, "r": 5, "s": 5, "t": 4,
        "u": 5, "v": 6, "w": 6, "x": 5, "y": 6,
        "z": 5,
        " ": 2
    }
}

# Cameo width
WIDTH = {
    "ra1": 64,
    "ra2": 60,
    "ra2_gloss": 60
}

# Cameo height
HEIGHT = {
    "ra1": 48,
    "ra2": 48,
    "ra2_gloss": 48
}

# Letters will be placed at y of...
COORD_Y = {
    "ra1": 42,
    "ra2": 42,
    "ra2_gloss": 42
}

def compute_width(letters, game):
    w = 0
    for letter in letters:
        w += LETTER_WIDTH[game][letter]
    return w


def put_letters(image, drawable, letters, x, game):
    text_layer = pdb.gimp_layer_new(image, WIDTH[game], HEIGHT[game], 1, "text", 100, 0)
    pdb.gimp_image_insert_layer(image, text_layer, None, -1)

    for letter in letters:
        if letter == " ":  # This is an exception :)
            x += LETTER_WIDTH[game][letter]
            continue

        charf = letter + ".png"
        charf = os.path.join(FONT_DIR[game], charf)

        layer = pdb.gimp_file_load_layer(image, charf)
        pdb.gimp_layer_translate(layer, x, COORD_Y[game])
        pdb.gimp_image_insert_layer(image, layer, None, -1)
        pdb.gimp_image_merge_down(image, layer, 0)
        x += LETTER_WIDTH[game][letter]


def put_bg(image, game):
    layer = pdb.gimp_layer_new(image, WIDTH[game], 7, 1, "bg", 100, 0)
    pdb.gimp_image_insert_layer(image, layer, None, -1)

    pdb.gimp_context_set_foreground((0, 0, 0))
    pdb.gimp_drawable_fill(layer, 0)
    pdb.gimp_layer_set_opacity(layer, 50)
    pdb.gimp_layer_translate(layer, 0, COORD_Y[game] - 1)


def add_text(img, drawable, words, game):
    # split char by char.
    letters = words.lower()
    width = compute_width(letters, game)

    # Letter starts at x:
    x = (WIDTH[game] - width) // 2
    # slightly to the right, if odd
    if (WIDTH[game] - width) % 2 == 1:
        x += 1

    pdb.gimp_image_undo_group_start(img)
    put_bg(img, game)
    put_letters(img, drawable, letters, x, game)
    pdb.gimp_image_undo_group_end(img)


def add_ra1_text(img, drawable, words):
    add_text(img, drawable, words, "ra1")


def add_ra2_text(img, drawable, words):
    add_text(img, drawable, words, "ra2")


def add_ra2_text_gloss(img, drawable, words):
    add_text(img, drawable, words, "ra2_gloss")


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

register(
    "python-fu-ra2-cameo-text",
    "Add text to the cameo image",
    "Add text to the cameo image",
    "BoolBada",
    "BoolBada",
    "2017,2021",
    "RA2 Cameo Text (no gloss)...",
    "RGB*, GRAY*",
    [
        (PF_IMAGE,    "img",       "Input image", None),
        (PF_DRAWABLE, "drawable",  "Input drawable", None),
        (PF_STRING,   "words", "Text", "Unit Name")
    ],
    [],
    add_ra2_text,
    menu="<Image>/Filters/CnC Modding/RA2 Cameo Text (no gloss)",
    domain=("gimp20-python", gimp.locale_directory)
    )

register(
    "python-fu-ra2-cameo-text-gloss",
    "Add text to the cameo image",
    "Add text to the cameo image",
    "BoolBada",
    "BoolBada",
    "2017,2021",
    "RA2 Cameo Text (glossy)...",
    "RGB*, GRAY*",
    [
        (PF_IMAGE,    "img",       "Input image", None),
        (PF_DRAWABLE, "drawable",  "Input drawable", None),
        (PF_STRING,   "words", "Text", "Unit Name")
    ],
    [],
    add_ra2_text_gloss,
    menu="<Image>/Filters/CnC Modding/RA2 Cameo Text (glossy)",
    domain=("gimp20-python", gimp.locale_directory)
    )

main()
