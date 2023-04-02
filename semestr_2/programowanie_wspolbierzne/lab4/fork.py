#!/usr/bin/python3
import sys
from os import fork, getpid, getppid

print(f"Before fork pid={getpid():<10} ppid={getppid()}")

fork()
print(f"After fork pid={getpid():<10} ppid={getppid()}")

"""
Result:

Before fork
After fork
After fork

'After fork' is doubled because fork is executing same code 
"""