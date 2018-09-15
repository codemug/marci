

# Marci

[![Build Status](https://api.travis-ci.org/codemug/marci.svg?branch=master)](https://api.travis-ci.org/codemug/marci)

Navigate your python process' memory. Analyze objects and their relations to other objects.

### Motivation

During a memory leak detection spree, I came across multiple tools but I couldn't get them to analyze, navigate and traverse object graphs in memory like I wanted. My requirements forced me to use the `gc` package directly and I ended up writing snippets of memory analysis code that I needed to run again and again so I ended up packing these snippets in this package.


### Installation

To install, simply clone the source, navigate into the cloned directory and do a:
```
pip install .
```
I might be publishing a PyPi package pretty soon

### Usage

Fire up a python interpreter in your favorite terminal and run the following code:

```
from marci import ObjList, Capture
c = Capture()
c.start()

# Create some data, or do whatever needs to be observed for memory growth
some_data = {
    "string": "cobra"
}
more_data = [some_data]
obj_list = c.end()
```
Now obj_list contains all the objects that were created between the start() and the end() method It's a list with additional methods, so you can use it as a normal list:
```
>>> len(obj_list)
7
```

Additional methods include pretty printing
```
>>> obj_list.pprint()
(0, {})
(1, [{'string': 'cobra'}])
(2, ['obj_list', 'c', 'end'])
(3, ('c', 'end', 'obj_list'))
(4, (None,))
(5, <frame object at 0x7fdbaf32e548>)
(6, <frame object at 0x7fdbaf306810>)
```

Type to object count summary printing

```
>>> obj_list.psummary()
 <type 'dict'>	1
 <type 'list'>	2
<type 'frame'>	2
<type 'tuple'>	2
```

Extracting a specific type of objects from this list

```
>>> l_list = obj_list.extract(list)
>>> l_list.pprint()
(0, [{'string': 'cobra'}])
(1, ['obj_list', 'c', 'end'])
```
Or multiple types

```
>>> l_list = obj_list.extract([list,dict])
>>> l_list.pprint()
(0, {})
(1, [{'string': 'cobra'}])
(2, ['obj_list', 'c', 'end'])
```

Exclude specific type(s) of objects from the list
```
>>> l_list = obj_list.sanitize(dict)
>>> l_list.pprint()
(0, [{'string': 'cobra'}])
(1, ['obj_list', 'c', 'end'])
(2, ('c', 'end', 'obj_list'))
(3, (None,))
(4, <frame object at 0x7fdbaf32e548>)
(5, <frame object at 0x7fdbaf306810>)
```
Get a list of objects that are referencing an object inside the list

```
 >>> refs = l_list.refs_to_at(0)
 >>> refs.pprint(100)
 (0, '<frame object at 0x7fdbaf2e1420>')
 (1, '<frame object at 0x7fdbaf2e1608>')
```
Or a list of objects that are being referenced by an object inside the list
```
>>> refs = l_list.refs_by_at(0)
>>> refs.pprint()
(0, {'string': 'cobra'})
```


