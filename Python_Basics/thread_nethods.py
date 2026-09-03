from threading import Thread
from time import sleep

def A():
    for i in range(5):
        print("A")
        sleep(1)

def B():
    for i in range(5):
        print("B")
        sleep(1)

T1 = Thread(target=A)
T2 = Thread(target=B)

T1.start()
T2.start()

T1.join()
T2.join()

print("Bye")