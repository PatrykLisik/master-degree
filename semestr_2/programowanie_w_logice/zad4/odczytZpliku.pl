czytajPlik :-
	open('drzewo.txt',read,X),
	current_input(CI),
	set_input(X),
	kodOdczytujacy,
	close(X),
	set_input(CI).

kodOdczytujacy :- read(Term), obsluz(Term).

obsluz(end_of_file):-!.
obsluz(Term) :- write(Term),nl,kodOdczytujacy.
