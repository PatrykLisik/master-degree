kobieta(monika).
mezczyzna(pawel).
kobieta(marta).
kobieta(ewa).
mezczyzna(marcin).
mezczyzna(bartosz).
mezczyzna(adam).
matka(monika,marta).
matka(monika,bartosz).
ojciec(pawel,marta).
ojciec(pawel,bartosz).
ojciec(marcin,adam).
ojciec(marcin,ewa).
matka(marta,adam).
matka(marta,ewa).





rodzic(X,Y) :- ojciec(X,Y);matka(X,Y).
rodzenstwo(X,Y) :- rodzic(R,Y),rodzic(R,X).
siostra(X,Y) :- kobieta(X),rodzenstwo(X,Y).
brat(X,Y):- mezczyzna(X),rodzenstwo(X,Y).
jest_ojcem(X) :- ojciec(X,_).
jest_matka(X) :- matka(X,_).
dziadek(X,Y) :-  mezczyzna(X),ojciec(X,A),rodzic(A,Y).
babcia(X,Y) :- kobieta(X),matka(X,A),rodzic(A,Y).



nalezy(X, [X|_]) :-  True.
nalezy(X, [_|Yogon]) :- nalezy(X,Yogon).

usun(X, [X]):-list.
usun(X, [X|Yogon]):-[Yogon].
usun(X, [Y|Yogon]):-usun(X,[Y,Yogon]).
# nie działa - nie można zwacać
# Type error: `callable' expected, found `[]' (an empty_list)

usun(X, [X], []).
usun(X,[X|L1], L1).
usun(X, [Y|L2], [Y|L1]) :- usun(X,L2,L1).
usun(X,Y) :- usun(X,Y,OUT). # Nie działa zwraca true
