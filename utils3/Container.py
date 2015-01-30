import shelve
from collections import OrderedDict

class Container(dict):
    """
    An improved doted dictionary class.

    Examples:
    ---------------------------------
    >>> cont = Container()
    >>> cont['a'] = 10.23
    >>> cont.a
    10.23
    >>>
    >>> cont.b = "hello world"
    >>>
    >>> cont.keys()
    ['a', 'b']
    >>>
    >>> cont.get('a')
    10.23
    >>> cont.get('b')
    'hello world'
    >>> cont.set('hello', 'world')
    >>> cont.hello
    'world'


    >>> c = Container(x=10, y=40)
    >>> c
    {'x': 10, 'y': 40}

    >>> c.x
    10
    >>> c.y
    40

    """

    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)

    def set(self, key, value):
        self[key] = value

    # self.__keys__.append(key)

    def save(self, filename):
        """
        Save dictionary content to a file
        """
        import shelve

        s = shelve.open(filename)
        s['container_data'] = list(self.items())
        s.close()

    @classmethod
    def load(cls, filename):
        """
        Load dictionary content from a file
        """
        import shelve

        s = shelve.open(filename)
        items = s['container_data']

        #print "items = ", items

        c = Container(**dict(items))
        return c
        #for k, v in items:
        #    self[k] = v
        s.close()

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value



class OrderedConatainer(OrderedDict):
    """
    An improved doted dictionary class.

    Examples:
    ---------------------------------
    >>> cont = Container()
    >>> cont['a'] = 10.23
    >>> cont.a
    10.23
    >>>
    >>> cont.b = "hello world"
    >>>
    >>> cont.keys()
    ['a', 'b']
    >>>
    >>> cont.get('a')
    10.23
    >>> cont.get('b')
    'hello world'
    >>> cont.set('hello', 'world')
    >>> cont.hello
    'world'


    >>> c = Container(x=10, y=40)
    >>> c
    {'x': 10, 'y': 40}

    >>> c.x
    10
    >>> c.y
    40

    """

    def __init__(self, **kwargs):
        super(OrderedDict, self).__init__(**kwargs)

    def set(self, key, value):
        self[key] = value

    # self.__keys__.append(key)

    def save(self, filename):
        """
        Save dictionary content to a file
        """
        import shelve

        s = shelve.open(filename)
        s['container_data'] = list(self.items())
        s.close()

    @classmethod
    def load(cls, filename):
        """
        Load dictionary content from a file
        """
        import shelve

        s = shelve.open(filename)
        items = s['container_data']

        #print "items = ", items

        c = Container(**dict(items))
        return c
        #for k, v in items:
        #    self[k] = v
        s.close()

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value
