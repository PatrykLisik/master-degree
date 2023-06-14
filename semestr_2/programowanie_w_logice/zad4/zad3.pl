                                                          rodzic(a,b).
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
