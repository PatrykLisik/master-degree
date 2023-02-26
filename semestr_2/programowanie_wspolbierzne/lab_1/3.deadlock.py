from threading import Thread, RLock
from time import sleep
from random import random, choice

locks = [ RLock(), RLock()]

"""
Zakleszczenie wystęuje gdy wątki pobierją blokady na zmianę.
"""
def f(n):
    def _f():
        for i in range(20):
            print(f"Thread {n} iter {i} -- start")
            sleep(random())
            c = choice([0,1])
            sleep(random())
            locks[c].acquire()
            locks[1-c].acquire()
            print(f"Thread {n} iter {i} -- Critical section")
            sleep(random())
            locks[1-c].release()
            locks[c].release()

        print(f"Thread {n} exit")
    return _f

threads = [Thread(target=f(i)) for i in range(5)]

for t in threads:
    t.start()

for t in threads:
    t.join()



