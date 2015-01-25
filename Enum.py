class Enum: 
    """
    Enumaration Type:
    
    colors =  Enum(["RED", "WHITE", "GREEN", "BLUE", "YELLOW", "BLACK"])
    """
    
    def __init__(self, named_values):
        self.__dict__ = dict([ (e, i) for i, e in enumerate(named_values)])
        self.__names__ = named_values
    
    def __getitem__(self, name):        
        return self.__dict__.get(name)
    
    def __str__(self):
        return ", ".join([ "{} = {}".format(e, i) for i, e in enumerate(self.__names__)])
        
    def __repr__(self):
        return self.__str__()
    
    def name(self, param):
        
        return self.__names__[param]  
