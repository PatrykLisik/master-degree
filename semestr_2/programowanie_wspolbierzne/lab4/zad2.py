"""
Napisać skrypt w Pythonie który stworzy 10-ciu potomków. Każdy z potomków powinien wejść w nieskończoną pętlę.
Natomiast proces rodzicielski powinien czekać na zakończenie tych dziesięciu potomków.
Rozwiązanie niekorzystające z pętli jest nieakceptowalne: Nie przyjmę rozwiązania w którym student zrobił kopiuj-wklej 10-ciu wywołań fork-a.
Zweryfikować rozwiązanie przy pomocy narzędzia pstree (pod ubuntu można je zainstalować komendą sudo apt-get install psmisc).
Na koniec zabić wszystkie procesy jednym kill-em (kill -9 -n gdzie n jest pid-em rodzica.
Jest to jednocześnie gid grupy wszystkich tych procesów a kill z ujemnym pidem wysyła sygnał do grupy której gid jest równe wartości bezwzględnej podanego ujemnego pid-a).
"""
import os
from time import sleep

for i in range(10):
    me = os.getpid()
    pid = os.fork()
    if pid > 0:
        print(f'Parent: {me} waits for child {pid}')
    os.wait()
    print(f'pid={me} finishes')
    exit(0)

print(f'Last child pid = {os.getpid()}')
while True:
    sleep(1)
