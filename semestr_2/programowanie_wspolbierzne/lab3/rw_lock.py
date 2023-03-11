import threading
import time
import random


class RWLock:
    def __init__(self):
        self.rmut = threading.Lock()
        self.wmut = threading.Lock()
        self.readers = 0
    def rLock(self):
        with self.rmut:
            self.readers += 1
            if self.readers == 1:
                self.wmut.acquire()
    def rUnLock(self):
        with self.rmut:
            self.readers -= 1
            if self.readers == 0:
                self.wmut.release()
    def wLock(self):
        self.wmut.acquire()
    def wUnLock(self):
        self.wmut.release()


class RWLock2:
    def __init__(self):
        self.writer_active = False
        self.readers = 0
        self.waiting_writers=0
        self.condtion=threading.Condition()
    def rLock(self):
        with self.condtion:
            self.condtion.wait_for(lambda:not self.writer_active and self.waiting_writers == 0)
            self.readers += 1
    def rUnLock(self):
        with self.condtion:
            self.readers -= 1
            self.condtion.notify_all()
    def wLock(self):
        with self.condtion:
            self.waiting_writers += 1
            self.condtion.wait_for(lambda:self.readers == 0 and not self.writer_active)
            self.writer_active = True
            self.waiting_writers -= 1
    def wUnLock(self):
        with self.condtion:
            self.writer_active = False
            self.condtion.notify_all()    


rw = RWLock2()

class Reader(threading.Thread):
    def __init__(self, m):
        threading.Thread.__init__(self)
        self.m = m
    def run(self):
        for i in range(20):
            time.sleep(random.random())
            rw.rLock()
            print('Reader', self.m, 'starts reading,', i)
            time.sleep(random.random())
            print('Reader', self.m, 'stops reading,', i)
            rw.rUnLock()

class Writer(threading.Thread):
    def __init__(self, m):
        threading.Thread.__init__(self)
        self.m = m
    def run(self):
        for i in range(5):
            time.sleep(random.random())
            rw.wLock()
            print('Writer', self.m, 'starts writing,', i)
            time.sleep(random.random())
            print('Writer', self.m, 'stops writing,', i)
            rw.wUnLock()

def factory(m):
    if random.random() < 0.2:
        return Reader(m)
    else:
        return Writer(m)

threads = [factory(m) for m in range(10)]

for t in threads:
    t.start()      

for t in threads:
    t.join()                  