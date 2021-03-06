# AUTOGENERATED! DO NOT EDIT! File to edit: 00_utils.ipynb (unless otherwise specified).

__all__ = ['timer', 'filesize', 'save', 'load', 'push', 'refresh', 'backup', 'fig_params', 'force_aspect', 'matshow',
           'RNG']

# Cell
import warnings
with warnings.catch_warnings(): #ignore warnings
    warnings.simplefilter("ignore")
    import time
    import gzip
    import pickle
    import os
    import functools
    from functools import wraps
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    import numpy as np
    import typing
    from typing import Optional, Tuple, Dict, Callable, Union, Mapping, Sequence, Iterable, List

# Cell
def timer(func : callable) -> str:
    '''Decorator that reports the execution time
    and optionally returns the time difference by
    adding a `return_time` Boolean keyword argument
    to the function being wrapped.'''
    @wraps(func)
    def wrapper(*args, return_time = False, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        t = end-start
        print(func.__name__+' : '+f"Elapsed time: {t:0.4f} seconds")
        if not return_time:
            return result
        else:
            if result is not None:
                return result,t
            else:
                return t
    return wrapper

# Cell
def filesize(fname : str ='data.gz',
             exp : int = 1e-6):
    '''
    Returns filesize in bytes*`exp`, which defaults to megabytes.
    '''
    prefix={1:'', 1e-3:'kilo', 1e-6:'mega', 1e-9:'giga'}
    size=float((os.stat(fname).st_size)*(exp if exp in prefix else 1))
    return f"{fname} is {size:.5} {prefix.get(exp) or ''}bytes"

# Cell
def save(data,fname='data.gz'):
    '''
    Saves `data` as `fname` using gzip and pickle.
    Maximizes speed and compression of objects.
    '''
    with gzip.open(fname, "wb") as f:
        pickle.dump(data,f,-1)
    print(filesize(fname))

# Cell
def load(fname='data.gz',delete=False):
    '''
    Loads `fname`, returning pickled `data`.
    '''
    with gzip.open(fname, "rb") as f:
        data=pickle.load(f)
    if delete is True:
        os.remove(fname)
    return data

# Cell
def push(branch='master',comment='auto'):
    "Pushes all current files to given branch with comment."
    os.system('git branch -M {}'.format(branch))
    os.system('git add -A') #stage all files
    os.system('git commit -m "{}"'.format(comment)) #commit all files
    os.system('git push -u origin {} --force'.format(branch))

def refresh(comment='auto',branch='master'):
    "Builds nbdev library and docs."
    os.system('nbdev_build_lib') #build core python module
    os.system('nbdev_install_git_hooks')
    os.system('nbdev_build_docs') #build code documentation
    push(comment=comment,branch=branch)

def backup(comment='Backup'):
    "Like `Push` but with branch set to `backup`."
    os.system('git branch -M backup')
    os.system('git add -A') #stage all files
    os.system('git commit -m "{}"'.format(comment)) #commit all files
    os.system('git push -u origin backup --force')

# Cell
def fig_params(reset : bool = False,
              X : float = 3.5,
              Y : float = 3,
              hspace : float = 0.0,
              offset : float = -.4,
              font : str = 'Times New Roman',
              fontsize : int = 12,
              ticksize : int = 6,
              tickwidth : int = 2,
              linewidth : int = 2
             ):
    '''
    Changes the `rcParams` for plotting, with the option to `reset` to default.
    '''
    if reset:
        mpl.rcParams.update(mpl.rcParamsDefault)
    else:
        #figure font Times New Roman,Helvetica, Arial, Cambria, or Symbol
        mpl.rcParams['font.family'] = font
        mpl.rcParams['font.size'] = fontsize
        mpl.rcParams['axes.titlesize'] = fontsize
        mpl.rcParams['axes.linewidth'] = linewidth
        mpl.rcParams['axes.titley'] = offset


        mpl.rcParams['xtick.major.size'] = ticksize
        mpl.rcParams['xtick.major.width'] = tickwidth
        mpl.rcParams['xtick.minor.size'] = ticksize//2
        mpl.rcParams['xtick.minor.width'] = tickwidth//2
        mpl.rcParams['xtick.direction']='out'

        mpl.rcParams['ytick.major.size'] = ticksize
        mpl.rcParams['ytick.major.width'] = tickwidth
        mpl.rcParams['ytick.minor.size'] = ticksize//2
        mpl.rcParams['ytick.minor.width'] = tickwidth//2
        mpl.rcParams['ytick.direction']='out'

        mpl.rcParams['figure.figsize'] = [X,Y]
        mpl.rcParams['figure.subplot.hspace'] = hspace

def force_aspect(ax : mpl.axes,
                aspect : int = 1):
    '''
    Forces the aspect of the axes object `ax`.
    '''
    im = ax.get_images()
    extent =  im[0].get_extent()
    ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)

def matshow(x : np.ndarray,
            aspect : int = 1,
            save : bool = True,
            fname : str = 'test'):
    '''
    Simplified image plot of matrix `x` with forced `aspect` that can save `fname` to `path`.
    '''
    fig,ax=plt.subplots()
    ax.matshow(x)
    force_aspect(ax,aspect)
    if save:
        plt.savefig(fname, dpi=600,transparent=False, bbox_inches='tight')

# Cell
class RNG:
    '''
    Globally stable random number generator. Initialized with fixed `seed`.
    Contains `normal`, `random`, and `multimodal` methods, each with an
    `absval` and `asint` argument, which convert to positive values
    and round to integers respectively.
    '''

    overloaded = ['random','normal']

    def __init__(self, seed : Optional[int] = None, update = False):
        self.rng=np.random.default_rng(seed)
        if update:
            self.update()

    def typecast(self,
                 y : Union[int,float],
                 absval : bool = False,
                 asint : bool = False) -> Union[int,float,np.ndarray]:
        if absval:
            y=abs(y)
        if asint:
            y=np.rint(y).astype(int)
        return y

    def normal(self,
               x : Union[list,float,int] = 0,
               y : Union[list,float,int] = 0,
               shape : Optional[tuple] = None,
               absval : bool = False,
               asint : bool = False,
               clip = None
              ) -> Union[int,float,np.ndarray]:
        '''
        Draw from a Gaussian distribution with mean `x` and standard deviation `y`.
        If `shape` is not None, return a numpy array of draws.
        '''
        res = self.rng.normal(loc=x,scale=y,size=shape)
        if clip:
            res = np.clip(res,*clip)
        return self.typecast(res,absval=absval,asint=asint)

    def random(self,
               x : Union[list,float,int] = 0,
               y : Union[list,float,int] = 0,
               shape : Optional[tuple] = None,
               absval : bool = False,
               asint : bool = False) -> Union[int,float,np.ndarray]:
        '''
        Draw from a uniform distribution in the interval [`x`,`y`].
        If `shape` is not None, return a numpy array of draws.
        '''
        if hasattr(x,'__iter__') and hasattr(y,'__iter__'):
            res = []
            for xi,yi in zip(x,y):
                res += [xi+(yi-xi)*self.rng.random(size=shape)]
            res = self.typecast(np.array(res),absval=absval,asint=asint)
        else:
            res = self.typecast(x+(y-x)*self.rng.random(size=shape),
                                absval=absval,asint=asint)
        return res

    def __getattr__(self,attr):
        if attr in RNG.overloaded:
            return getattr(self,attr)
        else:
            return getattr(self.rng,attr)

    def update(self):
        '''
        Force all the rng functions into
        the global namespace. This is unsafe,
        but convenient. Running it e.g causes
        `random` to be callable without an RNG instance.
        '''
        for i in dir(self.rng):
            if i[0]!='_':
                globals().update({i:getattr(self,i)})