#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

description: Provides a fluent interface for functional programming,
             filtering sequences, and streams.

Examples:

    >>> from utils3 import Chain
    >>>
    >>> x = Chain([['233', 'a', 'b'], ['4343', 'y', 'o'], ['44', 'p', 'k']])

    >>>
    >>> x
    Chain : [['233', 'a', 'b'], ['4343', 'y', 'o'], ['44', 'p', 'k']]
    >>>

    Test if Chain is empty
    >>> x.is_empty()
    False

    Flat All sublists
    >>> x.flat()
    Chain : ['233', 'a', 'b', '4343', 'y', 'o', '44', 'p', 'k']

    Get an Element by Position
    >>> x[0]
    ['233', 'a', 'b']
    >>> x[1]
    ['4343', 'y', 'o']

    Count the Number of Elements
    >>> x.count()
    3

    Get an Element of each sublist by postion in this list
    >>> x.select_pos(0)             # Get the element 0 in each sublist
    Chain : ['233', '4343', '44']
    >>> x.select_pos(1)             # Get the element 1 in each sublist
    Chain : ['a', 'y', 'p']
    >>> x.select_pos(2)
    Chain : ['b', 'o', 'k']
    >>> x.select_pos(3)
    Chain : [None, None, None]


    >>> x.enumerate()
    Chain : [(0, ['233', 'a', 'b']), (1, ['4343', 'y', 'o']), (2, ['44', 'p', 'k'])]

    Add a New Element to the list
    >>> x.append(['1669', 'u', 'k'])
    Chain : [['233', 'a', 'b'], ['4343', 'y', 'o'], ['44', 'p', 'k'], ['1669', 'u', 'k']]


    Reversing a list, creates a new list
    >>> x.reverse()
    Chain : [['44', 'p', 'k'], ['4343', 'y', 'o'], ['233', 'a', 'b']]

    Retrive the Original Data
    >>> x.list
    [['233', 'a', 'b'], ['4343', 'y', 'o'], ['44', 'p', 'k']]


    Converting a sequence of strings to Int
    >>> x.select_pos(0).to_int()
    Chain : [233, 4343, 44]

    >>> x.select_pos(0).to_int().list
    [233, 4343, 44]

    >>> x.select_pos(0).to_float().list
    [233, 4343, 44]

    >>> x.update_pos(lambda x: float(x)/10, 0)
    Chain : [[23.3, 'a', 'b'], [434.3, 'y', 'o'], [4.4, 'p', 'k']]
    >>>

    >>> y = x.update_pos(lambda x: float(x)/10 -1, 0)
    >>> y
    Chain : [[22.3, 'a', 'b'], [433.3, 'y', 'o'], [3.4000000000000004, 'p', 'k']]


    >>> y.select_by_pos(lambda x: x > 20, 0)
    [[22.3, 'a', 'b'], [433.3, 'y', 'o']]
    >>>

    >>> y.select_by_pos(lambda x: x<10, 0)
    [[3.4000000000000004, 'p', 'k']]
    >>>

    >>> y.select_by_pos(lambda x: x == 'a', 1)
    [[22.3, 'a', 'b']]
    >>>


References:
    https://ochronus.com/a-rubyists-confessions-on-python/
    http://martinfowler.com/articles/collection-pipeline/
    http://www.ruby-doc.org/core-2.2.0/Array.html
    http://jeromedalbert.com/ruby-how-to-iterate-the-right-way/


p = ch.Chain([2, 3, 4, 5, 6, 7, 8, 11])
In [70]: p.enumerate().transpose()
Out[70]: Chain : [(0, 1, 2, 3, 4, 5, 6, 7), (2, 3, 4, 5, 6, 7, 8, 11)]


"""

from . import hof
from .check import is_empty, is_none, is_empty, is_list, is_tuple

from subprocess import Popen, PIPE

import re

def flatten(List):
    result = []

    for lst in List:
        result.extend(lst)
    return result

def get_pos(List, pos):

    if len(List) <= pos:
        return None
    else:
        return List[pos]

def update_pos(List, pos, function):

    if is_tuple(List):
        List2 = list(List)
    else:
        List2 = List.copy()

    List2[pos] = function(List[pos])

    return List2

def append_element(List, element):

    if is_tuple(List):
        List2 = list(List)
    else:
        List2 = List.copy()

    List2.append(element)
    return List2

def runcmd(command):
    command = command.encode("utf-8")
    p = Popen(command, shell=True, stdout=PIPE, stdin=PIPE)
    out, err = p.communicate()
    #out = hof.ifelse(is_none(out), "", out.decode("utf-8"))

    try:
        out = out.decode("utf-8")
    except:
        out = ""

    try:
        err = out.decode("utf-8")
    except:
        err = ""


    return "\n".join([out, err]).strip('\n\r')



class Chain(object):

    def __init__(self, list=[]):
        self.list = list

    def map(self, function):
        return Chain(hof.mapl(function, self.list))

    def select(self, predicate):
        return Chain(hof.filterl(predicate, self.list))

    def select_pos(self, pos):
        return Chain(hof.mapl(lambda a: get_pos(a, pos), self.list))

    def select_by_pos(self, predicate, pos):
        return  Chain(hof.filterl(lambda sublist: predicate(sublist[pos]), self.list))

    def append_pos(self, element):
        """ Append an element to each sublist """
        return Chain(hof.mapl(lambda sublist: append_element(sublist, element), self.list))

    def update_pos(self, function, pos):
        return Chain(hof.mapl(lambda sublist: update_pos(sublist, pos, function), self.list))



    def reject(self, predicate):
        return Chain(hof.filterl(lambda x: not predicate(x), self.list))

    def reject_none(self):
        return self.reject(is_none)

    def reject_type(self, type):
        return self.reject(lambda t: isinstance(t, type))

    def partition(self, predicate):
        return self.select(predicate), self.reject(predicate)

    def match(self, pattern):
        return Chain(hof.filterl(lambda txt: re.match(pattern, txt), self.list))

    def regex(self, pattern):
        return Chain(hof.mapl(lambda txt: re.findall(pattern, txt), self.list))

    def regexf(self, pattern):
        return Chain(flatten(hof.mapl(lambda txt: re.findall(pattern, txt), self.list)))

    def strip(self, param=None):
        return Chain(hof.mapl(lambda x: x.strip(param), self.list))

    def split(self, param=None):
        return Chain(hof.mapl(lambda x: x.split(param), self.list))

    def take(self, n):
        """
        Returns the firsts n elements of the Chain list
        :param n:
        :return:
        """
        if n > len(self.list):
            n = len(self.list)
        return Chain(self.list[:n])

    def drop(self, n):
        if n > len(self.list):
            n = len(self.list)
        return Chain(self.list[n:])

    def reverse(self):
        reversed_ = self.list.copy()
        reversed_.reverse()
        return Chain(reversed_)

    def sort(self):
        return Chain(sorted(self.list))


    def join(self, param=""):
        return param.join(hof.mapl(str, self.list))

    def get(self, attribute):
        return Chain(hof.mapl(hof.get(attribute), self.list))

    def count(self):
        return len(self.list)

    def is_empty(self):
        return self.list == []

    def append(self, element):
        lst = self.list.copy()
        lst.append(element)
        return Chain(lst)

    def insert(self, position , element):
        lst = self.list.copy()
        lst.insert(position, element)
        return Chain(lst)

    def unique(self):
        return Chain(hof.unique(self.list))

    def enumerate(self):
        return Chain(list(enumerate(self.list)))

    def any(self, predicate):
        return any(hof.mapl(predicate, self.list))

    def all(self, predicate):
        return all(hof.mapl(predicate, self.list))

    def find(self, predicate):
        return hof.find(predicate, self.list)

    def find_index(self, predicate):
        return hof.find_index(predicate, self.list)

    def transpose(self):
        return Chain(hof.transpose(self.list))

    def sum(self):
        return sum(self.list)

    def flat(self):
        return Chain(flatten(self.list))

    def to_int(self):
        return Chain(hof.mapl(lambda x: int(x), self.list))

    def to_float(self):
        return Chain(hof.mapl(lambda x: int(x), self.list))

    def to_str(self):
        return Chain(hof.mapl(lambda x: str(x), self.list))

    def to_dict(self, filednames):
        return Chain(hof.mapl(lambda sublist: dict(zip(filednames, sublist)), self.list))

    def splitlines(self):
         return Chain(hof.mapl(lambda x: x.splitlines(), self.list))

    def type(self):
        return self.map(type)

    def __str__(self):
        return "Chain : {}".format(self.list)

    def __repr__(self):
        return "Chain : {}".format(self.list)

    def __contains__(self, item):
        return item in self.list

    def __getitem__(self, item):
        return self.list[item]

