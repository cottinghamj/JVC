from msvcrt import getch
from datetime import date, time, datetime
from time import sleep
from Tkinter import *
import threading
import pickle

# Questions:
# * Should you be able to see that you have undone and redone a ton?
class Node():
    def __init__(self, c, t, parentNode=None):
        self.char = c
        self.time = t
        self.parent = parentNode
        self.children = []
       
    def getchildren(self):
        return self.children
        
    def haschildren(self):
        return len(self.children) > 0

    def addchild(self, child):
        self.children.append(child)
        
    def getlastchild(self):
        return self.children[len(self.children) - 1]
        
    def __str__(self):
        return "<Node: %s placed at %s with %d children>"%(self.char, self.time, len(self.children))
        
n1 = Node('a', datetime.now())
print n1


# Creates a tree of placements
def record(node):
    pointer = node
    print "Press ESC to end input"
    while True:
        
        key = ord(getch())
        print key
        # ESC
        if key == 27:
            end = Node("END0/", datetime.now(), pointer)
            pointer.addchild(end)
            break
        
        # PASTE -> CTRL + V
        elif key == 22:
            n = Node("<paste>", datetime.now(), pointer)
            pointer.addchild(n)
            pointer = n
            clip = root.clipboard_get() 
            currentDateTime = datetime.now()
            for c in clip:
                n = Node(c, datetime.now(), pointer)
                pointer.addchild(n)
                pointer = n
            n = Node('<endpaste>', datetime.now(), pointer)
            pointer.addchild(n)
            pointer = n
        # REDO -> CTRL + Y
        elif key == 25:
            if pointer.haschildren():
                n = Node(chr(key), datetime.now(), pointer)
                pointer.addchild(n)
                pointer = pointer.getlastchild()
        # BACKSPACE
        elif key == 8:
            if pointer.parent is not None:
                if pointer.char in ['<paste>', '<endpaste>']:
                    pointer = pointer.parent

                n = Node(chr(key), datetime.now(), pointer)
                pointer.addchild(n)
                pointer = pointer.parent   
        # UNDO -> CTRL + Z
        elif key == 26:
            if pointer.parent is not None:
                if pointer.char in ['<paste>', '<endpaste>']:
                    pointer = pointer.parent
                    while pointer.char not in ['<paste>', '<endpaste>']:
                        pointer = pointer.parent

                n = Node(chr(key), datetime.now(), pointer)
                pointer.addchild(n)
                pointer = pointer.parent
        else:
            n = Node(chr(key), datetime.now(), pointer)
            pointer.addchild(n)
            pointer = n
    return node


level = 0
# Is that DFS I see! :J
def printTree(node):
    #print "level is", level
    print node
    if node.haschildren():        
        for n in node.getchildren():
            global level 
            level += 1
            printTree(n)    
            level -= 1
       
def printFinishedState(node):
    answer = ""
    pointer = node
    while pointer.haschildren():
        if len(pointer.getchildren()) == 1:
            pointer = pointer.getchildren()[0]
        else:
            pointer = pointer.getlastchild()
            
        # Don't want to print the end tag
        if pointer.haschildren():
            answer+= pointer.char
    return answer
        
# This methods prints all the actions that have been applied, waiting
# the exact amount of time it was between keystrokes
'''
def playRecording(node):
    pointer = node
    if pointer.val != "\0START" or pointer.val != "END0/":
        pass
    if pointer.haschildren():
        for n in pointer.getchildren():
            if ord(pointer.val) is 8:
                T.delete('1.'+ str(len(T.get("1.0", "end-1c")) - 1), END)
            # undo code
            elif ord(pointer.val) is 26:
                if pointer.parent.char != "\0START":
                    for i in rand(0, len(pointer.parent.char)):
                        T.delete('1.'+ str(len(T.get("1.0", "end-1c")) - 1), END)
            else:
                T.insert(END, pointer.char)
            if n is not len(actionStore) - 1:
                if (actionStore[n+1][1] - i[1]).microseconds != 0:
                    sleep((actionStore[n+1][1] - i[1]).seconds + (100000.0/(actionStore[n+1][1] - i[1]).microseconds))      
            root.update()
'''    

    
root = Tk()
actionStore = []

newnode = Node('\0START', datetime.now())
record(newnode)
printTree(newnode)
print printFinishedState(newnode)
