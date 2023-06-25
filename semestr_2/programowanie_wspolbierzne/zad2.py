import logging
import random as r
import threading
import threading as th

x = 10.0

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(thread)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
                    filename="zad2.log",
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(thread)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


class Adder(th.Thread):
    def __init__(self, condition_add):
        th.Thread.__init__(self)
        self.condition_add = condition_add

    def run(self):
        global x
        while True:
            with self.condition_add:
                self.condition_add.wait_for(lambda: x < 30)
                logging.info(f"Adder lock acquire x={x}")
                x += r.random() * 10.0
                logging.info(f"After add x={x}")
                self.condition_add.notify_all()


class Subtr(th.Thread):
    def __init__(self, condition_sub):
        th.Thread.__init__(self)
        self.condition_sub = condition_sub

    def run(self):
        global x
        while True:
            with self.condition_sub:
                self.condition_sub.wait_for(lambda: x > 10)
                logging.info(f"Sub lock acquire x={x}")
                x -= r.random() * 10.0
                logging.info(f"After sub x={x}")
                self.condition_sub.notify()


def factory(cond):
    if r.random() < 0.5:
        return Adder(cond)
    else:
        return Subtr(cond)


loc = threading.Lock()

condition = threading.Condition(lock=loc)

ths = [factory(condition) for i in range(30)]

for t in ths:
    t.start()
for t in ths:
    t.join()
