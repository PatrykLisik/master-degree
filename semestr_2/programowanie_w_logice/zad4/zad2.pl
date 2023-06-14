wczytajDrzewo(F) :-
  open(F,read,X),
  current_input(CI),
  set_input(X),
  odczytajRodzica,
  close(X),
  set_input(CI).

odczytajRodzica :- read(Term), wczytajRodzica(Term).

wczytajRodzica(end_of_file):-!.
wczytajRodzica(Term) :- asserta(Term),odczytajRodzica.


usunDrzewo(F) :-
  open(F,read,X),
  current_input(CI),
  set_input(X),
  usunDrzewo,
  close(X),
  set_input(CI).

usunDrzewo :- read(Term), usunRodzica(Term).

usunRodzica(end_of_file):-!.
usunRodzica(Term) :- retractall(Term),usunDrzewo.


doPrzodka(X,X):-write(X).
doPrzodka(X,Y):-write(X),write('->'),rodzic(RodzicX,X),doPrzodka(RodzicX,Y),!.
doPrzodka(F,X,Y):-wczytajDrzewo(F),doPrzodka(X,Y),usunDrzewo(F).

:-dynamic(rodzic/2).
:- debug.

