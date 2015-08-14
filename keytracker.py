'''
NOTE: THIS CODE ATTEMPTED TO USE LIST, BUT THAT FAILS WHEN YOU DO MULTIPLE UNDOs IN A ROW
Other code uses the much smarter approach of using a tree! :D
'''


from msvcrt import getch
from datetime import date, time, datetime
from time import sleep
from Tkinter import *
import threading
import pickle

def record():
    print "Press ESC to end input"
    while True:
        
        key = ord(getch())
        print key
        if key == 27:
            break
        elif key == 22:
            clip = root.clipboard_get() 
            currentDateTime = datetime.now()
            for l in clip:
                actionStore.append([ord(l), currentDateTime])
        else:
            actionStore.append([key, datetime.now()])
    
    

    
# This methods prints all the actions that have been applied, waiting
# the exact amount of time it was between keystrokes
def timePrint():
    for n, i in enumerate(actionStore):
        if i[0] is 8:
            T.delete('1.'+ str(len(T.get("1.0", "end-1c")) - 1), END)
        # undo code
        elif i[0] is 26:
            if n != 0:
                undoTime = actionStore[n-1][1]
                for num, chara in enumerate(reversed(actionStore)):
                    if num != 0:
                        if chara[1] == undoTime:
                            T.delete('1.'+ str(len(T.get("1.0", "end-1c")) - 1), END)
                        else:
                            break
        else:
            T.insert(END, chr(i[0]))
        if n is not len(actionStore) - 1:
            if (actionStore[n+1][1] - i[1]).microseconds != 0:
                sleep((actionStore[n+1][1] - i[1]).seconds + (100000.0/(actionStore[n+1][1] - i[1]).microseconds))      
        root.update()
       

# This returns a string of the document so far as well as displaying 
# the document in its most recent state
# Note: I still use Tkinter so that I can preserve the deletions
def fullPrint():
    for n, i in enumerate(actionStore):
        if i[0] is 8:
            T.delete('1.'+ str(len(T.get("1.0", "end-1c")) - 1), END)
        elif i[0] is 22:
            T.delete('1.0', END)
            
        else:
            T.insert(END, chr(i[0]))
            
        root.update()
    return T.get("1.0", "end-1c")
    
# Return a list with all deletion actions and deleted characters already removed.
# CAUTION: Unable to anything of value if you print out the document using this list
# Datetimes in the returned array pretty much become USELESS, keeping for consistency throughout program
# Useful if you want to quick copy the document so far or you want faster loads    
def mistakeFree():
    mistakeFreeList = []
    for i in actionStore:
        if i[0] is 8:
            mistakeFreeList.pop()
        else:
            mistakeFreeList.append(i)
    return mistakeFreeList
        


root = Tk()
actionStore = []
record()

T = Text(root, height=20, width=50)
T.pack()
timePrint()
root.mainloop()

        