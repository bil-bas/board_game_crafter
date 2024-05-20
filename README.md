BoardGameCrafter
================

A helper for designing game cards, dice and tokens (and probably other things)

Dependencies
------------

### Inkscape

This package relies on Inkscape 1.3+ (inkscape.org) being installed on your system (in specifically /usr/bin/inkscape).
This is only used to batch convert SVG files to PDF files, so if you are only generating SVGs there is no need for Inkscape.
Python packages that export to PDF or do this conversion seem to work well with drawing elements, but seem to ignore fonts entirely.

### pdftk

This package relies on pdftk, to shuffle merge fronts and backs of cards together into a single PDF file.

Example games
-------------

* Ecogame for Escape2Make


How to Use
----------

* Download the git repository.
* Put your game in ./games/ with:
    * /games/<game>/build.py file, which contains build() and, optionally, upload() methods.
    * /games/<game>/<game>/ folder containing your Python classes.
    * /games/<game>/images/ containing images.
    * /games/<game>/config/ containing config files (<name>.yaml)
* Build with ./board_game_crafter <game> (output in ./output/<game>/)

TODO
----

* Convert to a python package that can be installed on your system and a globally accessible command.