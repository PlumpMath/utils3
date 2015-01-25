import sys


def is_python2():
    return sys.version_info.major == 2

def is_python27():
    return sys.version_info.major == 2 and  sys.version_info.minor == 7

def is_python3():
    return sys.version_info.major == 3


def is_empty(object):
    return not object

def is_list(var):
    """
    Test if variable var is list

    :return: True if var is list, False if var is not list
    :rtype:  bol
    """
    return isinstance(var, list)

def is_tuple(var):
    return isinstance(var, tuple)

def is_num(var):
    """
    Test if variable var is number (int or float)

    :return: True if var is number, False otherwise.
    :rtype:  bol
    """
    return isinstance(var, int) or isinstance(var, float)

def is_dict(var):
    return isinstance(var, dict)

def is_string(var):
    return isinstance(var, str)

def is_function(var):
    """
    Test if variable is function (has a __call__ attribute)

    :return: True if var is function, False otherwise.
    :rtype:  bol
    """
    return hasattr(var, '__call__')

def is_none(var):
    return var is None


def is_empty(lst):
    return len(lst) == 0

def is_not_empty(lst):
    return len(lst) !=0

def is_pos(x):
    return x > 0

def is_neg(x):
    return x < 0



#-------------------------------#
#  OPERATING SYSTEM DETECTION   #
#-------------------------------#

def is_unix():
    return sys.platform.startswith('linux') or \
           sys.platform.startswith('bsd') or \
           sys.platform.startswith('darwin')


def is_linux():
    """
    :return: Return True if OS is Linux, False otherwise
    :rtype: bool
    """
    return sys.platform.startswith('linux')


def is_windows():
    """
    :return: Return True if OS is Windows, False otherwise
    :rtype: bool
    """
    return sys.platform.startswith('win')


def is_darwin():
    """
    :return: Return True if OS is OSX, False otherwise
    :rtype: bool
    """
    return sys.platform.startswith('darwin')


def is_bsd():
    """
    :return: Return True if OS is BSD, False otherwise
    :rtype: bool
    """
    return sys.platform.startswith('bsd')
