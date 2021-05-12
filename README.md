# *sidis* :
> **Si**mple **D**ata **I**nterface**S** , https://noeloikeau.github.io/sidis/


## Install

**NYI**: `pip install sidis`

## How to use

```python
import sidis
from sidis import *
```

## Sorting, converting, accessing complex datastructures

```python
from sidis import sort, convert
```

```python
sort([9,0,1,8,7],by=convert,key=lambda t:len(t[-1])) 
```




    [(9, array([1, 0, 0, 1])),
     (8, array([1, 0, 0, 0])),
     (7, array([1, 1, 1])),
     (0, array([0])),
     (1, array([1]))]



```python
sort([9,0,1,8,7],by=nbits,sift=lambda t:t[-1]>2)
```




    [(9, 4), (8, 4), (7, 3)]



```python
from functools import partial
sort([9,0,1,8,7],by=partial(convert,to=hex,astype=int)) 
```




    [(9, '0x9'), (8, '0x8'), (7, '0x7'), (1, '0x1'), (0, '0x0')]



```python
import networkx as nx
g=nx.DiGraph()
g.add_edges_from([(0,1),(1,2),(2,0)])
g.add_edges_from([(0,0)])
g.in_degree()
```




    InDegreeView({0: 2, 1: 1, 2: 1})



```python
from sidis import get
get(g,'in_degree',0) #arbitrary access to objects and functions
```




    2



```python
sort(g.nodes,by=g.in_degree)
```




    [(0, 2), (1, 1), (2, 1)]



```python
sort(g.nodes,by=g.edges,key=lambda t:len(list(t[-1])))
```




    [(0, OutEdgeDataView([(0, 1), (0, 0)])),
     (1, OutEdgeDataView([(1, 2)])),
     (2, OutEdgeDataView([(2, 0)]))]



```python
from sidis import give
give(g,'nodes',0,newattr='for fun')
g.nodes[0]['newattr']
```




    'for fun'



```python
[give(g,'edges',e,weight=np.random.rand(1)) for e in g.edges]
sort(g.edges,'weight')
```




    [array([0.88512267]),
     array([0.52500761]),
     array([0.45325752]),
     array([0.27580335])]



## ... and more!

```python
from sidis import depth,flatten,inflate,fillar,Template,RNG,cast
```

```python
depth({'a':0,'b':{'c':1,'d':3}})
```




    2



```python
flatten({'a':0,'b':{'c':1,'d':3}})
```




    {'a': 0, 'b,c': 1, 'b,d': 3}



```python
inflate({'a': 0, 'b,c': 1, 'b,d': 3})
```




    {'a': 0, 'b': {'c': 1, 'd': 3}}



```python
fillar([[1],[2,3]],fillwith=1000,mask=False)
```




    array([[   1, 1000],
           [   2,    3]])



```python
Template('''
fill out your _name
and provide {0} ZIP _iter, lambda t: 'embedded iterable functions!'
''',_name='name and information',_iter=range(1))
```




    fill out your name and information
    and provide embedded iterable functions! 



```python
cast((0.1,0.5,2.5),int)
```




    (0, 0, 2)



```python
rng=RNG(0) #globally stable
rng.random(0,1,shape=(2,2))
```




    array([[0.63696169, 0.26978671],
           [0.04097352, 0.01652764]])


