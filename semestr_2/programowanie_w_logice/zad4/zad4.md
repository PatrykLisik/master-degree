# Zadanie 1

## 1 
```
tekstCzyLiczba(D):-number(D),rok(D).
tekstCzyLiczba(D):-string(D),podajRokZdarzenia(D).
```

## 2 
```prolog
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
nalezy(X, [_|T]) :- nalezy(X, T)

```


```
[debug]  ?- pytanie().
Podaj rok lub wydarzenie: "adada".
Nieznane zdarzenie

[debug]  ?- pytanie().
Podaj rok lub wydarzenie: 1411
|: .
Nieznany rok

[debug]  ?- 
```


## 3/5

```
dodajZdarzenie(R, W) :-
(zdarzenie(R, W1) ->
append(W1, [W], Nw),
retractall(zdarzenie(R, W1)),
assertz(zdarzenie(R, Nw));
assertz(zdarzenie(R, [W]))).
```

```
[debug]  ?- dodajZdarzenie(1492, "Odkrycie Ameryki").

[debug]  ?- pytanie().
Podaj rok lub wydarzenie: 1492
|: .
Odkrycie Ameryki

```

## 4
```prolog
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
```


```log
[debug]  ?- pytanie().
Podaj rok lub wydarzenie: 1944.
Nieznany rok

[debug]  ?- wczytajZdarzenia("./zdarzenia.txt").

[debug]  ?- pytanie().
Podaj rok lub wydarzenie: 1944.
Powstanie Warszawskie
bitwa o Ardeny
```

# Zadanie 3 

```
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

```

```
?- consult('zad4').

[debug]  ?- doPrzodka("./drzewo.txt", k,a).
k->f->b->a

[debug]  ?- 
```


# Zadanie 4

```
rodzic(a,c).
rodzic(a,d).
rodzic(b,e).
rodzic(b,f).
rodzic(c,g).
rodzic(c,h).
rodzic(c,i).
rodzic(d,j).
rodzic(f,k).
rodzic(f,l).


doPrzodka(X,X,S):-is_stream(S),write(S,X).
doPrzodka(X,Y, S):-is_stream(S),write(S,X),write(S,'->'),rodzic(RodzicX,X),doPrzodka(RodzicX,Y,S),!.
doPrzodka(X,Y,F):-string(F),open(F, append,S),doPrzodka(X,Y,S),close(S).
```