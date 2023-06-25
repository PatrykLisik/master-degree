import random
import threading


class MyThread(threading.Thread):
    def __init__(self, sem, mut, nr):
        threading.Thread.__init__(self)
        self.nr = nr
        self.sem = sem
        self.mut = mut

    def run(self):
        while True:
            print(f"{self.nr} | Before With mut")
            with self.mut:
                print(f"{self.nr} | With mut")
                if random.random() < 0.5:
                    print(f"{self.nr} | self.sem.release()")
                    self.sem.release()
                else:
                    print(f"{self.nr} | self.sem.acquire()")
                    self.sem.acquire()


sem = threading.Semaphore(2)
mut = threading.Semaphore(1)
ths = [MyThread(sem, mut, i) for i in range(10)]

for t in ths:
    t.start()
for t in ths:
    t.join()
