import os
from time import sleep

print(f'Parent: {os.getpid()}')

for i in range(10):
    if os.fork() == 0:
        print(f'Child pid = {os.getpid()}')
    while True:
        sleep(1)

for i in range(10):
    pid, _ = os.wait()
    print(f'Child {pid} finished')
