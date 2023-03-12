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



