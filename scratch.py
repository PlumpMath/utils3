#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

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


from io import StringIO
import sys

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



