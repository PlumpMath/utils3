#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Linux Helpers and Tools

"""
import os
from . import Path
from .check import is_none
from .hof import mapdict_values
import re


HOME = Path.home().path


def get_xdg_user_dir():
    """
    Returns a dictionary containing the user Default XDG directories
    in a Linux desktop following the Freedesktop Standard.

    :return: Dictonary

    Example of Output:

        {'XDG_DESKTOP_DIR': '/home/tux/Desktop',
         'XDG_DOCUMENTS_DIR': '/home/tux/Documents',
         'XDG_DOWNLOAD_DIR': '/home/tux/Downloads',
         'XDG_MUSIC_DIR': '/home/tux/Music',
         'XDG_PICTURES_DIR': '/home/tux/Pictures',
         'XDG_PUBLICSHARE_DIR': '/home/tux/',
         'XDG_TEMPLATES_DIR': '/home/tux/Templates',
         'XDG_VIDEOS_DIR': '/home/tux/Videos'}
    """

    user_dirs = Path.home().get(".config/user-dirs.dirs").read()
    key_values = re.findall('(^XDG.*)="(.*)"', user_dirs, re.M)
    xdg_dirs = mapdict_values(lambda p: p.replace("$HOME", HOME), dict(key_values))
    return xdg_dirs


XDG_DIRS = get_xdg_user_dir()


class DesktopEntry(object):

    def __init__(self, Type="Application", Version=None, Name="", GenericName=None,
                 Comment=None, Icon="", Terminal=None, Categories=None, MimeType=None,
                 Exec="", StartupNotify=None, ):
        """
        Create .desktop entry for Linux Destkop

        :return:
        """

        self.Type = Type
        self.Version = Version
        self.Name = Name
        self.GenericName = GenericName
        self.Comment = Comment
        self.Icon = Icon
        self.Terminal = Terminal
        self.Categories = Categories
        self.MimeType = MimeType
        self.Exec = Exec
        self.StartupNotify = StartupNotify

    def __str__(self):
        return self.make()

    def __repr__(self):
        return self.make()

    def make(self):
        txt = "[Desktop Entry]\n"
        txt += "\nType=" + self.Type

        txt += "\nEncoding=UTF-8"

        if not is_none(self.Version):
            txt += "\nVersion=" + self.Version

        txt += "\nName=" + self.Name



        if not is_none(self.GenericName):
            txt += "\nGenericName=" + self.GenericName

        if not is_none(self.Comment):
            txt += "\nComment=" + self.Comment

        if not is_none(self.Icon):
            txt += "\nIcon=" + self.Icon

        if not is_none(self.Terminal):
            txt += "\nTerminal=" + str(self.Terminal)

        if not is_none(self.MimeType):
            txt += "\nMimeType=" + self.MimeType

        if not is_none(self.StartupNotify):
            txt += "\nStartupNotify=" + str(self.StartupNotify)

        if not is_none(self.Categories):
            txt += "\nCategories=" + str(self.Categories)

        txt += "\nExec=" + self.Exec

        return txt

