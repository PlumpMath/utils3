#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This Module Provides Useful Python functions

Path: Path Manipulalation API and listing

"""


__author__ = "Caio Rodrigues Soares Silva"
__version__ = "0.1"
__email__ = "caiorss.rodrigues@gmail.com"


import sys
import os 

from .Path import Path
from .Enum import Enum
from .Container import Container
from .Chain import Chain

from .check import is_python2, is_python27, is_python3

from .check import ( is_list, is_tuple, is_num, is_dict, is_string, is_function, 
is_none, is_empty, is_not_empty, is_pos, is_neg )

from .check import is_unix, is_linux, is_windows, is_darwin, is_bsd


from .hof import ( unique, mapl, reducel, zipl, sort, filterl, unique )

try:
    from io import StringIO
except ImportError:
    from csString import StringIO

###############################
#       TYPE TESTING          #
###############################




def expandpath(path):
    """
    Expand path variables to absolute path
    """
    plist = []

    for p in path.split(os.sep):
        p_ = os.path.expanduser(p)
        p_ = os.path.expandvars(p_)
        plist.append(p_)

    return os.path.abspath(os.path.join(*plist))

#-------------------------------------#
#           FILES                     #
#-------------------------------------#



def write_file(filename, content):
    f = open(filename, 'w')
    f.write(content)
    f.close()


def read_file(filename):
    return open(filename).read()


def read_binfile(filename):
    return open(filename, "rb").read()



def load_yaml_string(yamlstring):
    """
    Load Yaml string and return a dictionary.
    
    :param yamlstring:  String containing yaml configuration
    :return:            Dictionary of yaml string
    :rtype:             dict
    """
    import yaml
    import io

    output = io.StringIO()
    output.write(yamlstring)

    data = yaml.safe_load(output.getvalue())
    output.close()
    return data


def load_yaml_file(yamlfile):
    """"
     Load Yaml file and return a dictionary.
    
    :param yamlfile:    Filename containing yaml configuration
    :return:            Dictionary of yaml string
    :rtype:             dict
    """
    import yaml

    with  open(yamlfile, 'r') as f:
        data = yaml.load(f)
    return data


def load_json_file(jsonfile):
    """
     Load json file and return a dictionary.

    :param jsonfile:    Filename containing yaml configuration
    :return:            Dictionary of yaml string
    :rtype:             dict
    """
    import json

    with  open(jsonfile, 'r') as f:
        data = json.load(f)
    return data

# ------------------------------------#
#     STRING MANIPULATION            #
#------------------------------------#

def byte2str(bytestring):
    """Convert byte type objects to String objects in python3"""
    return bytestring.decode("utf-8")


def joinstr(seq, sep=" "):
    """ Join strings str.join() is annoying """
    return sep.join(str(x) for x in seq)


def schar(char, idx, string):
    """
    Substitute character of idx position
    by character char

    :param char: Character
    :param idx:  Character index
    :param string: String to be susbstituted.
    :type char: str
    :type idx:  int
    :type string: str
    :return: string[idx] = char
    :rtype: str
    """
    return string[:idx] + char + string[idx + 1:]



Colors = Container(
    BLACK="\033[0;30m",
    BLUE="\033[0;34m",
    WHITE="\033[0;37m",
    GREEN="\033[0;32m",
    CYAN="\033[0;36m",
    RED="\033[0;31m",
    YELLOW="\033[0;33m",
    MAGNETA="\033[0;35m",
    BOLD="\033[1m",
    # BACKGROUNDS,
    BG_BLACK="\033[0;40m",
    BG_BLUE="\033[0;44m",
    BG_WHITE="\033[0;41m",
    BG_GREEN="\033[0;42m",
    BG_CYAN="\033[0;46m",
    BG_RED="\033[0;41m",
    BG_YELLOW="\033[0;43m",
    BG_MAGNETA="\033[0;45m",
    BG_BOLD="\033[4m",
)


#----------------------------#

def printc(*args):
    """
    Print text in colored format

    Color tags:
    {r} - red
    {y} - yellow
    {g} - green
    {0} - black
    {m} - magneta
    {w} - white
    {b} - Blue

    {b0} - background black
    {br} - background white
    {by} - background yello

    {bold} - Bold text
    {line} - Underline

    """
    import re

    txt = "".join(args) + "{w}"

    txt = re.sub(r'{\0}', r"\033[0;30m", txt)  # BLACK
    txt = re.sub(r'{b}', r"\033[0;34m", txt)  # BLUE
    txt = re.sub(r'{w}', r"\033[0;37m", txt)  # WHITE
    txt = re.sub(r'{g}', r"\033[0;32m", txt)  # GREEN
    txt = re.sub(r'{c}', r"\033[0;36m", txt)  # CYAN
    txt = re.sub(r'{r}', r"\033[0;31m", txt)  # RED
    txt = re.sub(r'{y}', r"\033[0;33m", txt)  # YELLOW
    txt = re.sub(r'{m}', r"\033[0;35m", txt)  # MAGNETA

    # BACKGROUNDS
    txt = re.sub(r'{b0}', r"\033[0;40m", txt)  # BLACK
    txt = re.sub(r'{bb}', r"\033[0;44m", txt)  # BLUE
    txt = re.sub(r'{bw}', r"\033[0;41m", txt)  # WHITE
    txt = re.sub(r'{bg}', r"\033[0;42m", txt)  # GREEN
    txt = re.sub(r'{bc}', r"\033[0;46m", txt)  # CYAN
    txt = re.sub(r'{br}', r"\033[0;41m", txt)  # RED
    txt = re.sub(r'{by}', r"\033[0;43m", txt)  # YELLOW
    txt = re.sub(r'{bm}', r"\033[0;45m", txt)  # MAGNETA

    txt = re.sub(r'{bold}', r"\033[1m", txt)  # Bold
    txt = re.sub(r'{line}', r"\033[4m", txt)  # Bold

    print(txt)




def lookup_dict(dic, val):
    """
    Get key, ==> dic[key] = val

    :param dic:   Dictionary
    :param val:   Value to be looked up
    :return:      Dictionary key which value is val
    :type dic: dict
    """
    for k in list(dic.keys()):
        if val == dic[k]:
            return k

    return None


def sort_tuple_list(lst, col):
    """
    :param lst: List of tuples
    :param col: Column number of tuple

    Example:

    x = [
    ("Person 1",10),
    ("Person 2",8),
    ("Person 3",12),
    ("Person 4",20)]

    In [21]: sort_tuple_list(x, 1)
    Out[21]: [('Person 2', 8), ('Person 1', 10), ('Person 3', 12), ('Person 4', 20)]

    In [22]: sort_tuple_list(x, 0)
    Out[22]: [('Person 1', 10), ('Person 2', 8), ('Person 3', 12), ('Person 4', 20)]
    """
    import operator

    lst.sort(key=operator.itemgetter(col))
    return lst


def sort_columns_by_column(lst, colindex):
    sorted = sort_tuple_list(list(zip(*lst)), colindex)
    return list(zip(*sorted))



def loadconfig(filename, separator="=", comment_symbol="#"):
    """
    :param filename:        Filename to be parsed
    :param separator:       Separtor between entry
    :param comment_symbol:  Comment symbol
    :return:                Dictionary containing the entries and values in config file.
    :type  filename:        str
    :type  separator:       str
    :type  comment_symbol:  str
    :type return: dict

    Parse a configuration file like:

            # Storage directory
            STORAGE  = ./storage
            DATABASE = zotero.sqlite
            PORT = 8080
            HOST = 0.0.0.0
            LOGFILE = /tmp/zotero.log

    and returns:

    {'LOGFILE ': ' /tmp/zotero.log', 'STORAGE  ': ' ./storage', 'DATABASE ...}


    """
    import re

    text = open(filename).read()

    entry_pattern = re.compile("(.*)%s(.*)" % separator)
    line_comment_pattern = re.compile("%s.*" % comment_symbol, re.M)

    _text = line_comment_pattern.sub("", text)
    _test = _text

    data = entry_pattern.findall(_text)
    #data = [(k.strip(), v.strip()) for k,v in data]
    Config = Container()

    for k, v in data:
        Config.set(k.strip(), v.strip())

    #return dict(data)
    return Config



def shape_list(lst, N):
    """
    Transforms a list into a matrix, for instance:

    :param N: Number of elements per row
    :return:  Reshaped list

    [a0, b0, c0, a1, b1, c1, a2, b2, c2] into

    [
    [a0 b0 c0],
    [a1 b1 c1],
    [a2 b2 c2],
    ]

    Examples:
    In [20]: lst = range(9)
    In [22]: lst
    Out[22]: [0, 1, 2, 3, 4, 5, 6, 7, 8]

    In [24]: shape_list(lst, 3)
    Out[24]: [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

    In [25]: shape_list(lst, 4)
    Out[25]: [[0, 1, 2, 3], [4, 5, 6, 7]]

    In [28]: shape_list(lst, 1)
    Out[28]: [[0], [1], [2], [3], [4]]
    """
    ls = lst[:]
    return [[ls.pop(0) for i in range(N)] for r in ls]


class ChDir(object):
    """
    Step into a directory temporarily.

    Example of usage:
    enter in the directory /opt/pycharm
    and goes back to actual directory

    with ChDir("/opt/pycharm"):
        print(os.getcwd())
        print(os.listdir("."))
    """
    def __init__(self, path):
        self.old_dir = os.getcwd()
        self.new_dir = path

    def __enter__(self):
        os.chdir(self.new_dir)

    def __exit__(self, *args):
        os.chdir(self.old_dir)


class Stdout(list):
    """
    Context Manager to capture Stdout output:

    From: http://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call

    with Capturing() as output:
        do_something(my_object)


    """
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout

