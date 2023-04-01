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



nalezy(X, [X|_]).
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

dodaj(X,L1,[X|L1]).

sklej([],L,L).
sklej([H|T1],L2,[H|T2]):-sklej(T1,L2,T2).


usun(X, L, L). # potrzeben jeśli usuwamy element którego nie ma na liście
usun(X,[X|L1], L1).
usun(X, [Y|L2], [Y|L1]) :- usun(X,L2,L1).


permut([],[]).
permut(L, [X|P]):- usun(X,L,L1),permut(L1,P).


podzbior([],_).
podzbior([LH|LT],K):-nalezy(LH,K),podzbior(LT,K).

podzbior([a,b],[a,b,c]). #true
podzbior([a,p],[a,b,c]). # false


rozlaczny([],_).
rozlaczny([LH|LT],K) :- not(nalezy(LH,K)),rozlaczny(LT,K).

rozlaczny([a,p],[a,b,c]). # flase
rozlaczny([l,p],[a,b,c]). # true

# jeszcze nie działa
unikalne([],_).
unikalne([LH|LT],Out):- not(nalezy(LH,Out)),unikalne(LT,[Out|LH]).
unikalne([LH|LT],Out):- nalezy(LH,Out),unikalne(LT,Out).
suma(L,K,M) :- unikalne(sklej(L,K),M).



suma_num3([X],X).
suma_num3([G|O],M) :- suma_num3(O,N),M is N+G.



wyst_poz(X,[X|_],N, NCurr):- N==NCurr.
wyst_poz(X,[_|LT],N,NCurr):- NewCurr is NCurr+1, wyst_poz(X,LT,N,NewCurr).
wyst_poz(X,[LH|LT],N):- wyst_poz(X,[LH|LT],N,0).

wyst_poz(a,[b,a,d],1). # True