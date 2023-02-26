from threading import Thread
from time import sleep
from random import random

class CountingThread(Thread):
    def __init__(self, n):
        Thread.__init__(self)
        self.n=n
    def run(self):
        print(f"Starting thread {self.n}")
        for m in range(10):
            sleep(random())
            print(f"Thread {self.n}, {m} th iteration")
        print(f"Thread {self.n} exiting")

threads = [CountingThread(n) for n in range(5)]

for t in threads:
    t.start()

for t in threads:
    t.join()

print("All threads finished")