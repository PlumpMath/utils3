#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils3 import is_empty
from utils3.Chain import Chain
from utils3.Path import Path
from pprint import pprint

lines = Path.home().get(".bashrc").read().splitlines()

#print(lines)

# p = Chain(lines)
# result = p.match("alias").regexf("alias\s(\S+)\s*='(.*)'").reject(is_empty).sort() #.select(lambda x: len(x[0]) == 2)
#
# pprint(dict(result.list))


print(p)


#pprint(result)


