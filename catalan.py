#!/usr/bin/env python
class Catalan:
    """A class for Catalan numbers and various objects numbered by them."""
    generated=dict()
    def __init__(self,l=None,r=None):
        if (l==None):
            ls=0
        else:
            ls=l.size
        if (r==None):
            rs=0
        else:
            rs=r.size
        self.div=ls+1
        self.left=l
        self.right=r
        self.size=ls+rs+1
        
def brackets(c):
    if(c==None):
        return ""
    brk='('
    brk+=brackets(c.left)
    brk+=')'
    brk+=brackets(c.right)
    return brk

def letterBrackets(c):
    if(c==None):
        return "*"
    return "("+letterBrackets(c.left)+letterBrackets(c.right)+")"

def generateCatalan(size):
    Catalan.generated[1]=[Catalan()]
    for i in range(2,size+1):
        gen=[]
        #L child only
        for cl in Catalan.generated[i-1]:
            gen.append(Catalan(cl,None))
        #both
        for j in range(1,i-1):
            for cl in Catalan.generated[j]:
                for cr in Catalan.generated[i-j-1]:
                    gen.append(Catalan(cl,cr))
        #R only
        for cr in Catalan.generated[i-1]:
            #stuff
            gen.append(Catalan(None,cr))
        Catalan.generated[i]=gen

generateCatalan(5)
for i in range (1,6):
    print i
    for c in Catalan.generated[i]:
        print letterBrackets(c)
    print ""
