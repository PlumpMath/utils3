#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
from utils3 import linux

pprint(linux.XDG_DIRS)

# #!/usr/bin/env xdg-open
# [Desktop Entry]
# Type=Application
# Encoding=UTF-8
# Name=EcnfsGtk
# Comment=Encfs Wizard -- Helps you to protect your data and privacy.
# Exec=python /home/tux/bin/encfsgtk.egg
# Icon=/usr/share/encfsgtk/icon.png
# Categories=Application;GTK;Security;Utility

desk = linux.DesktopEntry(
    Name="EcnfsGtk",
    Comment="Encfs Wizard -- Helps you to protect your data and privacy.",
    Icon="/usr/share/encfsgtk/icon.png",
    Categories="Application;GTK;Security;Utility",
    Exec="python /home/tux/bin/encfsgtk.egg"
)

print(desk)

