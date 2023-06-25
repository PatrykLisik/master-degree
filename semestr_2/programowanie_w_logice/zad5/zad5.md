# Zadanie 1
N to akumulator
```
wyst_ile(_,[],0).
wyst_ile(X,[X|LT],N) :- wyst_ile(X,LT,C),N is C+1,!. 
wyst_ile(X,[_|LT],N) :- wyst_ile(X,LT,C),N is C,!.
```

# Zadanie 3
```
s --> [a],s,[a].
s --> [b],s,[b].
s --> [a].
s --> [b].
s --> [].

parsuj(X) :- s(X,[]),!, length(X, N), N mod 2 =:=1.
```