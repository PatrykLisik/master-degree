from threading import Thread, RLock
from time import sleep
from random import random

counter = 0
lock = RLock()

def count():
    global counter
    counter = counter + 1


def sleep_count():
    global counter
    sleep(5*random())
    lock
    x = counter + 1
    sleep(random())
    counter = x

def lock_sleep_count():
    global counter
    sleep(5*random())
    lock.acquire()
    x = counter + 1
    sleep(random())
    counter = x
    lock.release()
    print(x)

threads = [Thread(target=lock_sleep_count) for i in range(50)]

for t in threads:
    t.start()

for t in threads:
    t.join()

print(f"Counter {counter}")