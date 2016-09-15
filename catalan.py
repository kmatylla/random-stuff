#!/usr/bin/env python
import cairo
import math

class Catalan:
    """A class for Catalan numbers and various objects numbered by them."""
    generated=dict()
    """A place to keep already generated objects."""
    def __init__(self,l=None,r=None):
        """Construct from left l and right r."""
        if (l==None):
            ls=0
            self.degl=0
        else:
            ls=l.size
            self.degl=l.degl+1
        if (r==None):
            rs=0
            self.degr=0
        else:
            rs=r.size
            self.degr=r.degr+1
        self.rootn=ls+1
        self.left=l
        self.right=r
        self.size=ls+rs+1

#generate the object up to size
def generateCatalan(size):
    """ Generate in Catalan.generated a dictionary i -> a list of all objects of size i, for i<= size.
Eg. Catalan.generated[1] has 1 list member, [2] has 2, [3] has 5, [4] has 14 etc.
    WARNING: Too large size may make python unresponsive.
    (For my computer, large = 15 and above.)"""
    #if (size>14):
    #    die("nope.") #kill it. kill it with fire.
    #    #also, don't put above line on github
        
    Catalan.generated[0]=[None]
    Catalan.generated[1]=[Catalan()]
    for i in range(2,size+1):
        gen=[]
        for j in range(i):
            for cl in Catalan.generated[j]:
                for cr in Catalan.generated[i-j-1]:
                    gen.append(Catalan(cl,cr))
        Catalan.generated[i]=gen

def textBrackets(c):
    """Write c as a sequence of nested brackets, eg. (()())."""
    if(c==None):
        return ""
    brk='('
    brk+=textBrackets(c.left)
    brk+=')'
    brk+=textBrackets(c.right)
    return brk

def textBracketsWord(c):
    """Write c as a sequence of bracketed characters (stars), eg. ((*(**))*)."""
    if(c==None):
        return "*"
    return "("+textBracketsWord(c.left)+textBracketsWord(c.right)+")"

#in all drawX : x,y=topleft corner size = size of box containing the pic
def drawBinaryTree(c,ctx,x=0.0,y=0.0,size=0.9):
    """Draw c as a binary tree onto Cairo context ctx.
    x,y -- topleft corner
    size -- width and height of the drawing are less than size and reasonably close to it."""
    x=0.0+x #ints are bad
    y=0.0+y
    size=0.0+size #like, very bad.
    if(c==None):
        return
    rad=min(.002,size/4)
    ctx.arc(x+size/2,y,rad,0,2 * math.pi)
    ctx.fill()
    ctx.move_to(x+size/2,y)
    if(c.left!=None):
        ctx.line_to(x+size/4,y+size/2)
        ctx.stroke()
        drawBinaryTree(c.left,ctx,x,y+size/2,size/2)
    ctx.move_to(x+size/2,y)
    if(c.right!=None):
        ctx.line_to(x+(size*3)/4,y+size/2)
        ctx.stroke()
        drawBinaryTree(c.right,ctx,x+size/2,y+size/2,size/2)

def drawTree(c,ctx,x=0,y=0,size=.9,angle=0):
    """Draw c as a (nonbinary) rooted tree onto Cairo context ctx.
    x,y -- topleft corner
    size -- width and height of the drawing are less than size and reasonably close to it
    angle -- 0 means the root is on top; other angle means the tree is rotated (radians)."""
    x=0.0+x
    y=0.0+y
    size=0.0+size
    angle=0.0+angle
    rad=min(.002,size/16)
    ctx.arc(x+size/2,y+size/2,rad,0,2 * math.pi)
    ctx.fill()
    _drawTreeHelper(c,ctx,x+size/2,y+size/2,size/2,angle)

def _drawTreeHelper(c,ctx,x,y,size,angle,da=0,mod=0):
    """You probably don't need to use that"""
    if(c==None):
        return
    rad=min(.0015,size/20)
    ctx.arc(x,y,rad,0,2 * math.pi)
    ctx.fill()
    if(c.degr > 0 and mod==0):
        mod=math.pi/2-math.pi/(2*(c.degr+1))
        angle=angle-mod
    xx=x+size*(math.sin(angle))/2
    yy=y+size*(math.cos(angle))/2
    ctx.move_to(x,y)
    ctx.line_to(xx,yy)
    ctx.stroke()
    _drawTreeHelper(c.left,ctx,xx,yy,size/2,angle,0,0)
    if(c.right!=None):
        if (da==0):
            da=math.pi/(1.0+c.degr)
        ctx.move_to(x,y)
        _drawTreeHelper(c.right,ctx,x,y,size,angle+da,da,mod)
    ctx.stroke()

def drawMountain(c,ctx,x,y,size=.9,step=0):
    """Draw c as a mountain-like thing onto Cairo context ctx.
    x,y -- topleft corner (actually the picture is lower, there is some whitespace)
    size -- width of the mountain
    step -- do not use that."""
    x=0.0+x
    y=0.0+y
    size=0.0+size
    if (c==None):
        return
    if (step==0):
        step=size/(c.size*2)
    ctx.move_to(x,y+size)
    ctx.line_to(x+step,y+size-step)
    ctx.stroke()
    drawMountain(c.left,ctx,x+step,y-step,size,step)
    r=2.0*c.rootn
    ctx.move_to(x+step*(r-1),y+size-step)
    ctx.line_to(x+step*r,y+size)
    ctx.stroke()
    drawMountain(c.right,ctx,x+step*r,y,size,step)

def drawStairs(c,ctx,x,y,size=.9,step=0):
    """Draw c as a tiled staircase onto Cairo context ctx.
    x,y -- topleft corner
    size -- width and height
    step -- do not use that."""
    x=0.0+x
    y=0.0+y
    size=0.0+size
    if (c==None):
        return
    if(step==0):
        step=size/c.size
    w=step*(c.rootn)
    h=step*(c.size-c.rootn+1)
    ctx.rectangle(x,y+size,w,-h)
    ctx.stroke()
    drawStairs(c.left,ctx,x,y-h,size,step)
    ctx.stroke()
    drawStairs(c.right,ctx,x+w,y,size,step)
    ctx.stroke()

#tree numbering
def textPermutation(c, plus=1):
    """Write c as a 312-avoiding permutation, eg. 231.
    The permutation is based on c as binary tree (preorder).
    plus -- do not use that."""
    if(c==None):
        return ""
    t=str(textPermutation(c.left,plus+1))+" "+str(plus)+" "+str(textPermutation(c.right,plus+c.rootn))
    return t.lstrip().rstrip()
#---
def eq(c1,c2):
    """Tell if two Catalan objects are equal."""
    if(c1==None):
        if(c2==None):
            return True
        else:
            return False
    if(c2==None):
        return False
    if(c1.size!=c2.size):
        return False
    if(c1.degl!=c2.degl):
        return False
    if(c1.degr!=c2.degr):
        return False
    if(c1.rootn!=c2.rootn):
        return False
    return(eq(c1.left,c2.left) and eq(c1.right,c2.right))

#flips brackets with letters, binary trees etc
def flip(c):
    """Flip the object, ie. flip horizontally the binary tree."""
    if (c==None):
        return None
    return Catalan(flip(c.right),flip(c.left))

def isFlip(c1,c2):
    """Tell if two objects are flips of each other."""
    if(c1==None):
        if(c2==None):
            return True
        else:
            return False
    if(c2==None):
        return False
    if(c1.size!=c2.size):
        return False
    if(c1.degl!=c2.degr):
        return False
    if(c1.degr!=c2.degl):
        return False
    return(isFlip(c1.left,c2.right) and isFlip(c1.right,c2.left))

def add(c1,c2,left=True):
    """Concatenate two objects, ie. concatenate mountains.
    left -- how are the mountains mapped to objects (do we start from raised mountain on left)."""
    if(left):   
        if(c1==None):
            return c2
        return Catalan(c1.left,add(c1.right,c2))
    else:
        if(c2==None):
            return c1
        return Catalan(add(c1,c2.left),c2.right)
    
# all left [right] subtrees from the spine
def split(c,left=True):
    """Return a list of subtrees of a tree starting from a "spine".
    left -- left subtrees, spine on right."""
    if(c==None):
        return []
    s=[]
    if(left):
        s.append(c.left)
        while(c.right!=None):
            c=c.right
            s.append(c.left)
    else:
        s.append(c.right)
        while(c.left!=None):
            c=c.left
            s.append(c.right)
    return s

# flips brackets, rooted trees etc; left = left mountain is raised
def flipRaised(c, left=True):
    """Flip the object on some stranger representation, ie. flip horizontally the mountain.
    left -- how are the mountains mapped to objects (do we start from raised mountain on left)."""
    if (c==None):
        return None
    cc=None
    if(left):
        for sub in split(c,left):
            cc=Catalan(flipRaised(sub,left),cc)
    else:
        for sub in split(c,left):
            cc=Catalan(cc,flipRaised(sub,left))
    return cc

def biflip(c, left=True):
    """Do both flips (useful as a shortcut."""
    return flipRaised(flip(c),left)

def getIndex(c,col):
    """Return the position of a given Catalan object c in an array col or -1.
    You probably don't need to use that."""
    for i in range(len(col)):
        if (eq(c,col[i])):
            return i
    return -1

def catalanFromBrackets(brk):
    """Reverse of textBrackets().
    brk -- brackets string."""
    if(brk==""):
        return None
    i=0
    if (brk[i]!="("):
        die("wrong input")
    deg=1
    while(deg>0):
        i+=1
        if(brk[i]=='('):
            deg+=1
        elif(brk[i]==')'):
            deg-=1
        else:
            die("wrong input")
    return Catalan(catalanFromBrackets(brk[1:i]),catalanFromBrackets(brk[i+1:]))

def catalanFromBracketsWord(brk):
    """Reverse of textBracketsWord().
    brk -- brackets string."""
    if(brk=='*'):
        return None
    brk=brk[1:-1] #remove parentheses
    if (brk[0]=='*'):
        i=1
    else: #brk[0]=='('
        deg=1
        i=1
        while(deg>0):
            if(brk[i]=="("):
                deg+=1
            if(brk[i]==")"):
                deg-=1
            i+=1
    return Catalan(catalanFromBracketsWord(brk[0:i]),
                   catalanFromBracketsWord(brk[i:]))

def catalanFromPermutation(p):
    """Reverse of textPermutation().
    p -- permutation; single space-separated."""
    if(p==""):
        return None
    numbers=p.split()
    l=[]
    r=[]
    flag=0
    i=1
    for sn in numbers:
        n=int(sn)
        if (n==1):
            flag=i
        else:
            if(flag==0):
                l.append(str(n-1))
                i+=1
            else:
                r.append(str(n-flag))
    pl=" ".join(l)
    pr=" ".join(r)
    return Catalan(catalanFromPermutation(pl),catalanFromPermutation(pr))

class BTree:
    """Simple binary tree, this class is meant to be expanded if necessary.
    Actually the main difference from the Catalan class is that a tree can have a parent."""
    def __init__(self,l=None,r=None,p=None,isLeft=True):
        self.parent=p
        self.left=l
        self.right=r
        if(p!=None):
            if(isLeft):
                p.left=self
            else:
                p.right=self
        if(l!=None):
            l.parent=self
        if(r!=None):
            r.parent=self
            
def btToText(tree):
    """Write the binary tree as parenthesed characters."""
    if(tree==None):
        return "*"
    return "("+btToText(tree.left)+btToText(tree.right)+")"

class RTree:
    def __init__(self,ch=[],p=None):
        self.parent=p
        self.children=ch
        if(p!=None):
            p.children.append(self)
        for t in ch:
            t.parent=self

def rtToText(tree):
    """Write the rooted tree as nested parentheses."""
    if(tree==None):
        return ""
    t=""
    for c in tree.children:
        t+="("+rtToText(c)+")"
    return t

def treeBinary(c):
    """Generate a binary tree structure from c."""
    if(c==None):
        return None
    return BTree(treeBinary(c.left),treeBinary(c.right))

def treeRooted(c):
    """Generate a rooted tree structure from c."""
    if(c==None):
        return RTree()
    t=RTree([treeRooted(c.left)])
    if(c.right!=None):
        tr=treeRooted(c.right)
        for t0 in tr.children:
            t.children.append(t0)
        for t0 in t.children:
            t0.parent=t
    return t

def catalanFromBTree(bt):
    """Generate a Catalan object from a binary tree bt."""
    if (bt==None):
        return None
    return Catalan(catalanFromBTree(bt.left),catalanFromBTree(bt.right))

def catalanFromRTree(rt):
    """Generate a Catalan object from a rooted tree rt."""
    if (len(rt.children)==0):
        return None
    rtr=RTree(rt.children[1:])
    lc=catalanFromRTree(rt.children[0])
    rc=catalanFromRTree(rtr)
    return Catalan(lc,rc)
