
s --> [a],s,[a].
s --> [b],s,[b].
s --> [a].
s --> [b].
s --> [].

parsuj(X) :- s(X,[]),!, length(X, N), N mod 2 =:=1.

