# UTILS3

Python Helpers and utilities for Functional Programming, Fluent Interface and Path Manipulation compatilbe with 
Python 3 and Python 2.7.

This modules provides the following submodules:

   * .Chain         Chain class that is useful for piping, sequencial functional programming. Similar to Fsharp, Scala and Ruby.
   
   * .Path          Fast and Syntax sugar Path Manipulation
   
   * .hof           A collections of higher order functions and functions for list and sequence processing based on functional 
                    programming languages like Haskell, Fsharp, Ocaml and Ruby.
   
   * .Enum          Enumeration Type Class/ Similar to C ENUM
   
   * .Container     A Generalized dot dictionary
   
   * .windows       Windows OS Helpers for Python.
    

# SUB MODULES

## Path

## Chain

Examples:

```python

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

```


## Enum

## Cotainer 




    
   

