Catalan Numbers
====
[What is this about?!?](http://en.wikipedia.org/wiki/Catalan_numbers)

Classes
------
* BTree
* Catalan
* RTree

### class BTree
Simple binary tree, this class is meant to be expanded if necessary. Actually the main difference from the Catalan class is that a tree can have a parent.

Methods defined here:
* `__init__(self, l=None, r=None, p=None, isLeft=True)` – constructor.

### class Catalan
A class for Catalan numbers and various objects numbered by them. **This is the important class in this module.**

Methods defined here:
* `__init__(self, l=None, r=None)` – constructor.

Data and other attributes defined here:
* `generated` = {} – all already generated objects, see the function [`generateCatalan`](#generatecatalansize) for more info.

### class RTree
Methods defined here:
* `__init__(self, ch=[], p=None)` – constructor.

Functions
----
In general: if a thing is named `c`, `c0`, `c1` or similar, it is assumed to be of the class `Catalan`. If it is named `ctx`, it is assumed to be a Cairo context.

When I write simply “object” in this file, I generally mean “object of class `Catalan`”.

If a funcion is not on this list, you probably don't need it since it's a helper for some other funcion. Also some parameters are just for recurrence and you probably won't need them, so they aren't documented.  Some funcions (drawing) are for use with the Cairo library.

Also, I have little experience in writing docomentation, so sorry for all confusion.

### add(c1, c2, left=True)
Concatenate two objects, ie. concatenate mountains.

`left` – how are the mountains mapped to objects (do we start from raised mountain on left).

### btToText(tree)
Write the binary tree `tree` as parenthesed characters.

### catalanFromBTree(bt)
Generate a Catalan object from a binary tree `bt`.

### catalanFromBrackets(brk)
Reverse of [`textBrackets`](#textbracketsc).

`brk` – brackets string.

### catalanFromBracketsWord(brk)
Reverse of [`textBracketsWord`](#textbracketswordc).

`brk` – brackets string.

### catalanFromPermutation(p)
Reverse of [`textPermutation`](#textPermutationc).

`p` – permutation; single space-separated.

### catalanFromRTree(rt)
Generate a Catalan object from a rooted tree `rt`.

### drawBinaryTree(c, ctx, x=0.0, y=0.0, size=0.9)
Draw `c` as a binary tree onto Cairo context `ctx`.

`x`,`y` – topleft corner

`size` – width and height of the drawing are less than size and reasonably close to it.

### drawMountain(c, ctx, x, y, size=0.9, step=0)
Draw `c` as a mountain-like thing onto Cairo context `ctx`.

`x`,`y` – topleft corner (actually the picture is lower, there is some whitespace)

`size` – width of the mountain

`step` – do not use that.

### drawStairs(c, ctx, x, y, size=0.9, step=0)
Draw `c` as a tiled staircase onto Cairo context `ctx`.

`x`,`y` – topleft corner

`size` – width and height

`step` – do not use that.

### drawTree(c, ctx, x=0, y=0, size=0.9, angle=0)
Draw `c` as a (nonbinary) rooted tree onto Cairo context `ctx`.

`x`,`y` – topleft corner

`size` – width and height of the drawing are less than size and reasonably close to it

`angle` – 0 means the root is on top; other angle means the tree is rotated (radians).

### eq(c1, c2)
Tell if two Catalan objects are equal.

### flip(c)
Flip the object, ie. flip horizontally the binary tree.

### flipRaised(c, left=True)
Flip the object on some stranger representation, ie. flip horizontally the mountain.

`left` – how are the mountains mapped to objects (do we start from raised mountain on left).

### generateCatalan(size)
Generate in Catalan.generated a dictionary i -> a list of all objects of size i, for i<= size. Eg. `Catalan.generated[1]` has 1 list member, [2] has 2, [3] has 5, [4] has 14 etc.

**Please be careful with size>14!**

### isFlip(c1, c2)
Tell if two objects are flips of each other.

### redux(c):
Return a smaller Catalan object, by representing `c` as bracketed word, remove the word and interpret the brackets as an object. Hard to explain, but I find it interesting.
`c` — the original object.

### rtToText(tree)
Write the rooted tree as nested parentheses.

### split(c, left=True)
Return a list of subtrees of a binary tree corresponding to `c` starting from a “spine”.

`left` – if equal to `True`: left subtrees, spine on right.

### subdivision(c,s=None)
Generate non-crossing subdivision of set (more precisely: a list) `s` corresponding to `c`. Returns a list of lists. Size of `s` should be equal to `c.size`. If s is set to `None` or not given, it will be set to [0, 1, 2, 3, ..., n].

### textBrackets(c)
Write `c` as a sequence of nested brackets, eg. `(()())`.

### textBracketsWord(c)
Write `c` as a sequence of bracketed characters (stars), eg. `((*(**))*)`.

### textPermutation(c, plus=1)
Write `c` as a 312-avoiding permutation, eg. 231.
The permutation is based on c as binary tree (preorder).

`plus` – do not use that.

### treeBinary(c)
Generate a binary tree (a `BTree` object) from `c`.

### treeRooted(c)
Generate a rooted tree (a `RTree` object) from `c`.

### triangulation(c)
Represent `c` as a polygon triangulation. Return a list of three-element lists of numbers, which represent vertices of the triangles. Tne polygon vertices are numbered 0, 1, …, n+1.
`c` – the Catalan object