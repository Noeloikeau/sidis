# -*- coding: utf-8 -*-
"""
Created on Mon May 17 13:36:45 2021

@author: Noeloikeau Charlot
"""



def trycast(obj : data, to : type) -> data:
    '''
    Attempts to typecast `obj` to datatype `to`,
    without any customized conversion. Fallback
    of more complex casting cases in this module.
    '''
    try:
        return to(obj)
    except:
        return typing.cast(to,obj)
    

def nonitr2itr(obj : data, to : type) -> data:
    '''
    Wrap the noniterable `obj` into the iterable type `to`.
    '''
    if to is list:
        return [obj]
    elif to is tuple:
        return (obj,)
    elif to is str:
        return f'{obj}'
    elif to is dict:
        return {obj:obj}
    elif to is set:
        return {obj}
    elif to is np.ndarray:
        return np.array(obj)
    else:
        return trycast(obj,to)

def itr2nonitr(obj : data, to : type) -> data:
    '''
    Treat each element of the iterable `obj` as the 
    noniterable type `to`.
    '''
    t=type(obj)
    if t is dict:
        return {k:trycast(v,to) for k,v in obj.items()}
    else:
        return trycast([trycast(i,to) for i in obj],to)

def itr2itr(obj : data, to : type) -> data:
    '''
    Treat the iterable `obj` as a new iterable of type `to`.
    Just treats dictionaries as their items rather than default keys.
    '''
    if type(obj) is dict:
        return trycast(obj.items(),to)
    elif to is dict:
        return {i:o for i,o in enumerate(obj)}
    else:
        return trycast(obj,to)

class Cast:
    '''
    Universal typecasting class with customizable ruleset.
    Stores the ruleset as a dictionary of dictionaries.
    The outer dictionary stores the type of the object to be converted.
    The inner dictionary stores all the types to convert into.
    The values are partially evaluated functions on the inner type,
    which get called by a class object and evaluated on the outer type.
    The ruleset can be updated and changed as needed.
    '''
    types=[None,int,float,list,tuple,str,dict,set,np.ndarray]

    isiter = lambda t: hasattr(t,'__iter__')
    
    iterables=[t for t in types if isiter(t)]
    
    iterables.remove(str) #want to wrap strings like numbers
                
    def get_rules(types=types,
                  iterables=iterables,
                  itr2itr=itr2itr,
                  nonitr2itr=nonitr2itr,
                  itr2nonitr=itr2nonitr):
        
        rules={t1:{t2:None for t2 in types} for t1 in types}
        noniterables=[t for t in types if t not in iterables]
        
        for t1 in types:
            for t2 in types:
                if t1 in noniterables and t2 in iterables:
                    rules[t1][t2]=partial(nonitr2itr,to=t2)
                elif t1 in iterables and t2 in noniterables:
                    rules[t1][t2]=partial(itr2nonitr,to=t2)
                elif t1 in iterables and t2 in iterables:
                    rules[t1][t2]=partial(itr2itr,to=t2)
                else:
                    rules[t1][t2]=partial(trycast,to=t2)
                    
        return rules
        
    
    def __init__(self,
                 rules : Optional[dict] = None):
        if rules is None:
            rules=Cast.get_rules()
        self.rules=rules
        
    def __getitem__(self,item):
        return self.rules[item]
    
    
    def __call__(self,
                 obj : data,
                 *args : type):
        res=obj
        for arg in args:
            t=type(res)
            try:
                res=self.rules[t][arg](res)
            except:
                res=trycast(res,arg)
        return res

cast=Cast()
                
            
            
