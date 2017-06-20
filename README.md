# CameoTextEmbedder

GIMP plugin to embed text to side bar icons in C&amp;C mods

# Installation

* First, you have to determine where your GIMP plugin should be placed.
* To do that, open GIMP.
* Filters --> Python-Fu --> Console
* Type the following command without quotes: "print(gimp.directory)"
* You'll see something like this:
  * C:\\Users\user\\.gimp-2.8
  * /home/user/.gimp-2.8
* We will call this $GIMP\_HOME
* Place put\_ra1.py in $GIMP_HOME/plug-ins directory, which should be already there.
* Copy (or soft link) ra1\_cameo\_font data into $GIMP\_HOME so that
  the plugin can find $GIMP\_HOME\_ra1\_cameo\_font\_a.png, b.png, ...
* Restart GIMP, if you haven't closed it already.

# How to use

* You'll see the following new menu:
* Filters --> Python-Fu --> RA1 Cameo Text
* Click on it, type your cameo text and that's it.
* It creates two new layers, one is half-transparent background for the text
  and the other is the cameo text. You can move or delete them to fit your need.
* This script can be adapted to do RA2 cameo too.
  You need to copy the script, make alphabets in PNG format
  like the ones in ra1\_cameo\_font (with alpha channel as transparency),
  then modify LETTER\_WIDTH variable in the script.
