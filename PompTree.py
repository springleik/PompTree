#!/usr/bin/env python
# Json text generator, for creating random trees
# http://www.williamsonic.com/CompTree/

import sys, random, string

# check command line args
leafFileName  = 'leaf.txt'
if len(sys.argv) > 1: leafFileName = sys.argv[1]
else:
    print ('usage: python PompTree.py leaf.txt')
    quit()
leafFile = open(leafFileName, 'r')

# base class for tree nodes
class node:
    # class variables
    theDepth = 0
    nodeCount = 0
    maxDepth = 0

    # instance methods
    def Populate(self):
        if node.theDepth > node.maxDepth: node.maxDepth = node.theDepth
        node.theDepth += 1
        numChildren = random.randint(1,10)
        while (numChildren and node.theDepth < 10 and node.nodeCount < 100):
            newItem = random.choice(['dict', 'array', 'array', 'leaf', 'leaf', 'leaf', 'leaf'])
            if newItem == 'dict': newItem = dBranch()
            elif newItem == 'array': newItem = aBranch()
            elif newItem == 'leaf': newItem = leaf()
            newItem.Populate()
            self.AddToList(newItem)
            numChildren -= 1
        node.theDepth -= 1

    # generate random key names
    def keyRand(self, theKey):
        theRange = string.ascii_uppercase + string.ascii_lowercase + string.digits
        for _ in range(5): theKey += random.choice(theRange)
        return theKey

# subclass for dictionary branch nodes
class dBranch(node):
    def __init__(self):
        node.nodeCount += 1
        self.dList = {}

    # add key-value pair to dictionary
    def AddToList(self, newItem):
        self.dList[self.keyRand('_')] = newItem

    # serialize as Json text on console
    def Express(self):
        print ('{', end='')
        first = True
        for key, value in self.dList.items():
            if first: first = False
            else: print (',', end='')
            print ('"{0}":'.format(key), end='')
            value.Express(),
        print ('}', end='')

# subclass for array branch nodes
class aBranch(node):
    def __init__(self):
        node.nodeCount += 1
        self.aList = []

    # add value to array
    def AddToList(self, newItem):
        self.aList.append(newItem)

    # serialize as Json text on console
    def Express(self):
        print ('[', end='')
        first = True
        for item in self.aList:
            if first: first = False
            else: print (',', end='')
            item.Express(),
        print (']', end='')

# subclass for tree leaf nodes
class leaf(node):
    def __init__(self):
        node.nodeCount += 1
        self.content =  None

    # obtain content from input file
    def Populate(self):
        if node.theDepth > node.maxDepth: node.maxDepth = node.theDepth
        line = leafFile.readline()
        if not line:
            leafFile.seek(0)
            line = leafFile.readline()
        self.content = line.rstrip()

    # serialize as Json text on console
    def Express(self):
        if self.content == None: print ('null', end='')
        elif self.content == True: print ('true', end='')
        elif self.content == False: print ('false', end='')
        else: print (self.content, end='')

# build random tree out of objects, arrays, and leaf nodes
listHead = random.choice(['dict', 'array'])
if listHead == 'dict': listHead = dBranch()
elif listHead == 'array': listHead = aBranch()
listHead.Populate()

# express random tree as Json text
listHead.Express()
print ()
leafFile.close()
