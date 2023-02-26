# Lab 4 

tabela i dane 

```
create table m(p1 int, p2 int, c1 int , c2 int, v int, primary key((p1,p2), c1, c2));

insert into m(p1,p2,c1,c2,v) values(1,1,1,2,2) ;
insert into m(p1,p2,c1,c2,v) values(1,1,2,2,2) ;
insert into m(p1,p2,c1,c2,v) values(1,2,2,2,2) ;
```

Efekt
```
cqlsh:test> SELECT * from m ;

 p1 | p2 | c1 | c2 | v
----+----+----+----+---
  1 |  2 |  2 |  2 | 2
  1 |  1 |  1 |  1 | 1
  1 |  1 |  1 |  2 | 2
  1 |  1 |  2 |  2 | 2

(4 rows)


```

Trzeba robić `WHERE` po całym kluczu partycjonowania(p1,p2).
```
cqlsh:test> SELECT * from m WHERE p1=1 AND c2=2;
InvalidRequest: Error from server: code=2200 [Invalid query] message="Cannot execute this query as it might involve data filtering and thus may have unpredictable performance. If you want to execute this query despite the performance unpredictability, use ALLOW FILTERING"
```

Doczytać o kluczu klastrowania.
```
cqlsh:test> SELECT * from m WHERE p1=1 AND p2=1 and c1=1;

 p1 | p2 | c1 | c2 | v
----+----+----+----+---
  1 |  1 |  1 |  1 | 1
  1 |  1 |  1 |  2 | 2

(2 rows)
```

Gdy robimy update musimy określić całość klucza głównego. 
Cassandra robi update bez odczytu -> nie sprawdza czy dana wartość już istnieje
```
cqlsh:test> update m set v=10 where p1=10 and p2=20 and c1=10 and c2=10;
cqlsh:test> SELECT * from m ;

 p1 | p2 | c1 | c2 | v
----+----+----+----+----
  1 |  2 |  2 |  2 |  2
  1 |  1 |  1 |  1 |  1
  1 |  1 |  1 |  2 |  2
  1 |  1 |  2 |  2 |  2
 10 | 20 | 10 | 10 | 10
 ```

Usuwanie polega na wstawiniu nagrobka do komórki. 
Nagrobki trzymane są domyślne przez 10 dni. 
Przyczyną tego jest potencjlana awaria jednego z węzłów i brak replikacji nagrobka. 
Gdyby kompaktyfikacja usuneła nagrobek a węzeł który uległ awarii powrócił do życia, przywrócił by też usunięte dane bez nagrobka. 

## UUID i time UUID

tabela i dane
```
create table uuidt(p int, c uuid, v int, primary key(p,c));
insert into uuidt(p,c,v) values(1,uuid(), 1);
insert into uuidt(p,c,v) values(1,uuid(), 2);
insert into uuidt(p,c,v) values(1,uuid(), 3);
insert into uuidt(p,c,v) values(1,uuid(), 4);
```
```
cqlsh:test> SELECT * from uuidt ;

 p | c                                    | v
---+--------------------------------------+---
 1 | 50fde2ab-7768-4f44-80de-506588247402 | 3
 1 | 551d80f7-ea58-4ad4-ac2c-b01b64f1e42f | 2
 1 | 9fb3b562-129a-4371-8b09-37324dba8982 | 4
 1 | e3894661-e347-4e76-b9ba-e69cec860fd1 | 1

(4 rows)

```

```
create table tuuidt(p int, c timeuuid, v int, primary key(p,c));
insert into tuuidt(p,c,v) values(1,now(), 1);
insert into tuuidt(p,c,v) values(1,now(), 2);
insert into tuuidt(p,c,v) values(1,now(), 3);
insert into tuuidt(p,c,v) values(1,now(), 4);
SELECT * from tuuidt ;

 p | c                                    | v
---+--------------------------------------+---
 1 | 7d8445a0-7ebe-11ed-b536-e966e5d1b1f2 | 1
 1 | 7f90de80-7ebe-11ed-b536-e966e5d1b1f2 | 2
 1 | 818cd590-7ebe-11ed-b536-e966e5d1b1f2 | 3
 1 | 82f89a90-7ebe-11ed-b536-e966e5d1b1f2 | 4

(4 rows)
```

## Counter

Cassandara posiada wiele feature'ów które do niej nie pasują jak np ligthweigth transations które nie są lekkie. 
Jeśli potrzebujemy dobierać się do danych po róznych ścieżkach to jest to znak żeby nie uzywać Cassandry.

Nie można mieszac kolumn typu counter z innymi typami kolumn. 
Nie można wstawiać do kolumny typu counter. 
Counter potrafi gubić dane -> zaleca się nie stosować;

```
cqlsh:test> create table cnt(id int primary key, c counter)
        ... ;
cqlsh:test> update cnt set c = c + 10 where id =1;
cqlsh:test> SELECT * from cnt; 

 id | c
----+----
  1 | 10

(1 rows)
```

## Kolekcje
Listy - obecna implementacja jest błędna 

Mapa i set są ok.
```
create table col(id int primary key, s set<int>, m map<text, int>, l list<int>);
```
```
cqlsh:test> update col set s = s + {3, 11} where id=1;
cqlsh:test> SELECT * from col;

 id | l    | m    | s
----+------+------+---------
  1 | null | null | {3, 11}

(1 rows)
cqlsh:test> update col set s = s + {3, 10, 1} where id=1;
cqlsh:test> SELECT * from col;

 id | l    | m    | s
----+------+------+----------------
  1 | null | null | {1, 3, 10, 11}

(1 rows)
```

```
cqlsh:test> insert into col(id, m) values(2, {'a':1000, 'b':200});
cqlsh:test> SELECT * from col;

 id | l    | m                     | s
----+------+-----------------------+----------------
  1 | null |                  null | {1, 3, 10, 11}
  2 | null | {'a': 1000, 'b': 200} |           null

(2 rows)

```
```
cqlsh:test> update col set m=m-{'b'} where id=2;
cqlsh:test> SELECT * from col;

 id | l    | m           | s
----+------+-------------+----------------
  1 | null |        null | {1, 3, 10, 11}
  2 | null | {'a': 1000} |           null

(2 rows)
```