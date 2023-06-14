zdarzenie(1410,['Bitwa pd Grunwaldem','Zmarl antypapiez Aleksander V']).
zdarzenie(1772,['Pierwszy rozbiór Polski','Bitwa morska pod Patras']).
zdarzenie(1939,['Wybuch II wojny swiatowej','Powstala firma Hewlett-Packard','Podpisano pakt stalowy']).

wypiszListe([]):-!.
wypiszListe([X|Y]):-write(X),nl,wypiszListe(Y).

rok(X):-zdarzenie(X,Y),wypiszListe(Y).

pytanie:-
  write('Podaj rok lub wydarzenie: '),
        read(D),
        tekstCzyLiczba(D).

tekstCzyLiczba(D):-number(D),rok(D);number(D),write('Nieznany rok').
tekstCzyLiczba(D):-string(D),podajRokZdarzenia(D);string(D),write('Nieznane zdarzenie').

podajRokZdarzenia(D):-zdarzenie(R,L),nalezy(D,L),write(R).

nalezy(X, [X|_]).
nalezy(X, [_|T]) :- nalezy(X, T).

dodajZdarzenie(R, W) :-
(zdarzenie(R, W1) ->
append(W1, [W], Nw),
retractall(zdarzenie(R, W1)),
assertz(zdarzenie(R, Nw));
assertz(zdarzenie(R, [W]))).


czytajPlik :-
  open('drzewo.txt',read,X),
  current_input(CI),
  set_input(X),
  kodOdczytujacy,
  close(X),
  set_input(CI).
  
wczytajZdarzenia(F) :-
  open(F,read,X),
  current_input(CI),
  set_input(X),
  odczytajZdarzenie,
  close(X),
  set_input(CI).

odczytajZdarzenie :- read(Term), obsluzZdarzenie(Term).

obsluzZdarzenie(end_of_file):-!.
obsluzZdarzenie(Term) :- asserta(Term),odczytajZdarzenie.

czytajPlik :-
open('./dane.txt',read,X),
current_input(CI),
set_input(X),
kodOdczytujacy,
close(X),
set_input(CI).
kodOdczytujacy :- read(Term), obsluz(Term).

obsluz(end_of_file):-!.

obsluz(Term) :-write(Term),nl,kodOdczytujacy.

:-dynamic(zdarzenie/2).
:- debug.
