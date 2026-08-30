import sys
from time import sleep
print(sys.getrecursionlimit())
sys.setrecursionlimit(5)
i = 0

def printi():
    global i
    i += 1
    print(i)
    sleep(1)
    printi()

printi()