# AUTOGENERATED! DO NOT EDIT! File to edit: 02_recursion.ipynb (unless otherwise specified).

__all__ = ['depth', 'flatten', 'unflatten', 'get', 'give', 'sort', 'pipe', 'maps']

# Cell
import warnings
with warnings.catch_warnings(): #ignore warnings
    warnings.simplefilter("ignore")
    import typing
    import numpy as np
    from typing import Optional, Tuple, Dict, Callable, Union, Mapping, Sequence, Iterable
    from functools import partial
    import warnings
    from .conversion import cast,convert
    import collections

# Cell
def depth(obj : Union[dict,list]):
    '''
    Recursively sort the number of layers of a nested
    list or dictionary `x`.
    '''
    if type(obj) is dict and obj:
        return 1 + max(depth(obj[a]) for a in obj)
    if type(obj) is list and obj:
        return 1 + max(depth(a) for a in obj)
    return 0


# Cell
def flatten(obj : Union[dict,list], parent_key='',sep=','):
    '''
    Concatenate the nested input `obj` into an equivalent
    datastructure of depth 1. Uses the `parent_key` and `sep`
    arg to combine nested dictionary keys.
    https://stackoverflow.com/questions/6027558/flatten-nested-dictionaries-compressing-keys

    '''

    def flatten_list(obj):
        if obj == []:
            return obj
        if isinstance(obj[0], list):
            return flatten_list(obj[0]) + flatten_list(obj[1:])
        return obj[:1] + flatten_list(obj[1:])

    def flatten_dict(obj=obj,parent_key=parent_key,sep=sep):
        items = []
        for k, v in obj.items():
            new_key = parent_key + sep + str(k) if parent_key else str(k)
            if isinstance(v, collections.abc.MutableMapping):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    if type(obj) is dict:
            return flatten_dict(obj)
    elif type(obj) is list:
        return flatten_list(obj)


# Cell
def unflatten(d : dict, sep=","):
    '''
    Un-flatten a flattened nested dictionary `d` with
    concatenated key separation `sep`.
    https://gist.github.com/fmder/494aaa2dd6f8c428cede
    '''
    items = dict()
    for k, v in d.items():
        keys = k.split(sep)
        sub_items = items
        for ki in keys[:-1]:
            try:
                sub_items = sub_items[ki]
            except KeyError:
                sub_items[ki] = dict()
                sub_items = sub_items[ki]

        sub_items[keys[-1]] = v

    return items

# Cell
def get(obj : Union[object,dict,list,tuple,callable,np.ndarray],
        *args : Union[None,str,int,float,tuple,list,dict],
        retnone : bool = True,
        call : bool = False,
        **kwargs
       ) -> Union[object,dict,list,tuple,callable,int,float,set,np.ndarray]:
    '''
    Recursively accesses `obj` by the given ordered attributes/keys/indexes `args`.

    If `call`, the last accessed object will try to call any **kwargs.

    If `retnone`, returns None if
    the object can't be accessed by any of the args; else, returns `obj`.
    '''
    res=obj
    for attr in args:
        try: #list, arr, tuple w/index=attr, dict w/ key=attr
            res=res[attr]
        except:
            try: #class object w/ attr
                res=getattr(res,attr)
            except: #method or callable
                try:
                    res=res(attr)
                except:
                    pass

    if call:
        try:
            res=res(**kwargs)
        except:
            res=res

    if res is not obj:
        return res
    else:
        return (None if retnone else obj)

# Cell
def give(obj : Union[object,dict,list,tuple,np.ndarray],
        *args : Union[str,int,float,tuple,list,dict],
         **kwargs : object
       ) -> Union[object,dict,list,tuple,np.ndarray]:
    '''
    Assign `args` element of `obj` to a value. If no `kwargs`,
    assign the last item of `args`. If `kwargs`, assign those.
    '''

    if kwargs=={}:# no key-value pairs to set, use last ordered arg, assuming len(args)>1:
        if len(args)<2:
            print('Not enough args or kwargs - require access to elements of obj.')

        elif len(args)==2: #index by first, set value of second
            try:
                obj[args[0]]=args[1]
            except:
                try:
                    setattr(obj,args[0],args[1])
                except:
                    print(f"Could not access up to {args[:-1]} and/or apply {args[-1]}.")

        elif len(args)>2: #get up to -3, access by -2, set value with -1
            temp=get(obj,*args[:-2]) #need to access temporary variable
            try:
                temp[args[-2]]=args[-1]
            except:
                try:
                    setattr(temp,args[-2],args[-1])
                except:
                    print(f"Could not access up to {args[:-1]} and/or apply {args[-1]}.")

    else: #dict or obj-like
        if len(args)==0: #set key,value pairs or attrs
            try:
                for k,v in kwargs.items():
                    try:
                        obj[k]=v
                    except:
                        setattr(obj,k,v)
            except:
                print(f"Could not access {k} and/or apply {v}.")

        else:
            try:
                temp=get(obj,*args,retnone=False)
                for k,v in kwargs.items():
                    try:
                        temp[k]=v
                    except:
                        setattr(temp,k,v)
            except:
                print(f"Could not access {k} and/or apply {v}.")



# Cell
def sort(obj : Iterable,
         *args : Union[None,str,int,float,tuple,list,dict],
         by : Union[None,object,dict,list,tuple,callable,np.ndarray] = None,#lambda o: o,
         key : callable = lambda t: get(t,-1,retnone=False) if get(t,-1,retnone=False) else 0,#lambda t:t[-1] if depth(t)!=0 else t,
         sift : callable = lambda t: True,# if get(t,-1,retnone=False) else False,
         reverse : bool = True
        ) -> Union[None,int,float,list,tuple,str,dict,np.ndarray]:
    '''
    Recursively sorts `obj` `by` `args` using `key`.

    Treats `obj` as an iterator and wraps `by` around the elements of `obj`,

    before optionally wrapping any remaining `args`, and returning the evaluated

    tuples generated over `obj`. If `by` is None, searches for `args`.

    If both `by` and `args` is None, sorts over `obj` only : default behavior.

    `sift` defaults to keeping all elements, while

    `key` defaults to treating empty objects as having value 0.

    `reverse` sorts ascending by default.

    '''

    if by is not None:#if you're sorting over a different evaluation than the object elements

        sorting=filter(sift,[ (i, get( get( by, i, retnone=False), #evaluate inner function
                        *args,retnone=False) #and any remaining args
                  ) for i in obj]) #over iterable and store tuples then sort

    elif args is not (): #if you're sorting over the object and provide args

        sorting=filter(sift,[get(get(obj,i,retnone=False),*args,retnone=False) for i in obj])

    else: #otherwise you're just sorting the object

        sorting=filter(sift,obj)

    return sorted(sorting,key=key,reverse=reverse)


# Cell
def pipe(func,otype=None,ftype=None,cast=cast,*args,**kwargs):
    '''
    Pipelines the `func` to act on a later object.
    Returns a partially evaluated function over any `args` and `kwargs`.
    The object is casted to type `otype` before being evaluated.
    The output of the function is casted to `ftype`
    '''
    f=partial(func,*args,**kwargs)
    def line(obj):
        obj=cast(obj,otype)
        return cast(f(obj),ftype)
    return line


# Cell
def maps(obj,
             *funcs,
             depth=0,
             zipit=False,
             to=None,
             squeeze=True):
    '''
    Sequentially map `funcs` over the elements of `obj`, "o".
    The first `depth` number of funcs are mapped sequentially f(g(h(...(o)..)))=x.
    The remaining number of funcs are mapped separately (u(x),v(x),...).
    Use partial `funcs` to fill in all args but `obj` if other parameters needed.
    If `keys`, return tuples of the object elements "o" along with map outputs.
    '''
    if not funcs:
        return obj
    else:
        obj=obj if hasattr(obj,'__iter__') and type(obj)!='str' else [obj] #asiter(obj)
        r=[o for o in obj]
        [[give(r,i,get(f,r[i])) for f in funcs[:depth]] for i in range(len(r))]
        [give(r,i,[get(f,r[i]) for f in funcs[depth:]]) for i in range(len(r))]
        if squeeze:
            r=np.ndarray.tolist(np.squeeze(np.array(r,dtype=object)))
        if zipit:
            r=list(zip(obj,r))
        return cast(r,to)