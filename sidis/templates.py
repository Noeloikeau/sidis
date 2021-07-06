# AUTOGENERATED! DO NOT EDIT! File to edit: 03_templates.ipynb (unless otherwise specified).

__all__ = ['replace', 'txt2lst', 'lst2txt', 'ZIP', 'getEvals', 'filltxt', 'Template']

# Cell
import warnings
with warnings.catch_warnings(): #ignore warnings
    warnings.simplefilter("ignore")
    from typing import Optional, Tuple, Dict, Callable, Union, Mapping, Sequence, Iterable
    import numpy as np
    from .conversion import cast
    from .recursion import get

# Cell
def replace(l,**kwargs):
    'Replace the line `l` in `txt` with any occurances of the dictionaried values. '
    for k,v in kwargs.items():
        l=l.replace(k,str(v))
    return l

def txt2lst(txt):
    'Remove all newlines `\n` and empty strings `''` from the template `txt`.'
    return [t for t in txt.split('\n') if t!='']

def lst2txt(ltxt):
    'Concatenate a list of text `ltxt` into a string separated by newlines.'
    return '\n'.join(ltxt)

def ZIP(txt,_iter,*lambdas,as_txt=False):
    '''Loop over the iterable `_iter` and format `txt` in order of the `lambdas`.
    If `_iter` is an int, it is treated as `range(_iter)`, and if it is a tuple,
    it is treated as `np.ndindex(_iter)`.
    '''
    _iter=cast(_iter,list)
    try:
        l=[str(txt).format( *[l(*i) for l in lambdas] ) for i in _iter]
    except:
        l=[str(txt).format( *[l(i) for l in lambdas] ) for i in _iter]
    if as_txt is True:
        l=lst2txt(l)
    return l

def getEvals(replaced_txt,funcs=['ZIP']):
    '''Obtain a tuple of containing the `funcs`, the text they format, their arguments,
    and their line index in the template `txt`.
    '''
    y=[]
    for i,o in enumerate(replaced_txt):
        for f in funcs:
            if len(o.split(f))>1:
                #function, (txt to be formatted, func args), position in file
                y+=[(f,o.split(f),i)]
    return y

def filltxt(txt,funcs=['ZIP'],**kwargs):
    '''Take a template `txt`, replace all `kwargs` via `Replace`, then evaluate the `funcs`
       on the surrounding text using `GetEvals`.'''
    txt=txt2lst(txt)
    for i,l in enumerate(txt):
        txt[i]=replace(l,**kwargs)
    y=getEvals(txt,funcs)
    e=list(map(lambda s: eval(s[0]+'('+'{0:s[1][0]}[0]'+','+s[1][1]+')' ),y)) #evaluate the function
    u=[(i,e) for i,e in zip([y[i][-1] for i in range(len(y))],[e[i] for i in range(len(y))])] #position/evals
    t=[] #new txt
    for i in range(len(txt)):
        t+=[txt[i]]
        for j,e in u: #remove old lines
            if i==j:
                t.remove(txt[i])
                for q in e:
                    t+=[q]
    return t


class Template:
    '''
    Automates iteration over arbitrary Python functions embedded into blocks of text.

    Class attrs:

        funcs=[`ZIP`] (list of callable) : the keyword function to map over the text it's embedded in

        filler=`fill` (callable) : method of filling the text


    Inputs:

        `temp` (str): input string to be filled, or file name to be loaded

        `kwargs` (dict): characters to be replaced and evaluated


    Attrs:

        `plate` (list): line-by-line filling of `temp` based on `kwargs`

        `temp` (str): saved version of `temp` separated by newlines


    Methods:

        `load`: loads `fname` and fills based on `kwargs`.

        `out`: write/append `txt`, which defaults to filled data `str`, to `fname`.

        `fill`: fills the template by replacing `kwargs` and evaluating `funcs`.

    '''
    funcs=['ZIP']
    filler=filltxt
    def __init__(self,temp,**kwargs):
        self.__dict__.update({k:v for k,v in kwargs.items() if k!='self' and k!='kwargs'})
        self.temp=temp
        try:
            self.load(temp,**kwargs)
            print(f'Loaded {temp}.')
        except:
            self.temp=temp
            self.fill(**kwargs)

    def fill(self,temp=None,append=False,**kwargs):
        if not append:
            if temp is not None:
                self.temp=temp
            if kwargs!={}:
                self.plate=Template.filler(self.temp,Template.funcs,**kwargs)
                self.__dict__.update(kwargs)
        else:
            if (temp is not None) and (temp!=self.temp):
                self.temp+='\n'+temp
            if kwargs!={}:
                self.plate+=Template.filler(temp,Template.funcs,**kwargs)
                self.__dict__.update(kwargs)

    def txt(self):
        return lst2txt(self.plate)

    def load(self,fname,**kwargs):
        with open(fname,'r') as f:
            self.temp=f.read()
        self.fill(**kwargs)

    def out(self,fname,txt=None,s='a'):
        if txt is None:
            txt=self.txt()
        with open(fname,s) as f:
            f.write(txt)

    def __repr__(self):
        try:
            return self.txt()
        except:
            return self.temp