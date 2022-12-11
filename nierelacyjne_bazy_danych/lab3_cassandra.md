# Casandara

Baza typu whitetable
Zalety:

- dane są masywnie rozproszone - tysiące serwerów
- potrzeba dużej szybkości zapisu

Wady:

- brak transakcji
- brak spójności innej niż ewentualna
- nie można robić złączeń(join)

Cassandy używamy tylko w obrębie podstawowej funkcjonalności, jeśli potrzebujmy czegoś więcej to znak, że  trzeba użyć innej technologi

wejście do shella cassandry

```
docker exec -it cas cqlsh
```

Tworzymy nowy keyspace

```
CREATE KEYSPACE test WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
```

Pozorna denormalizacja

Kopia danych z katalogu do koszyka nie jest demoralizacją, bo zachowuje stan danych z chwili ich wybierania.

 ```
 use test ;
 ```

```
create table basket(id_client int, id_prod int, address text static, pdesc text, uprice float, quant int,primary key(id_client, id_prod));
```

static oznacza że jest jedna komórka per klucz partycypowania(key(id_client, id_prod))

`key(id_client, id_prod)` kolejność jest kluczowa. Zależy od niego to jak interpretowane są zapytania

```
insert into basket(id_client, id_prod, address, pdesc, uprice, quant) values(1,1,'swansea', 'bike', 1000.0, 1);
insert into basket(id_client, id_prod, address, pdesc, uprice, quant) values(2,3,'someMark', 'rack', 2200.1, 2);
insert into basket(id_client, id_prod, address, pdesc, uprice, quant) values(2,2,'someMark', 'bigRack', 4200.1, 1);
```

```
cqlsh:test> select * from basket;

 id_client | id_prod | address  | pdesc   | quant | uprice
-----------+---------+----------+---------+-------+-----------
         1 |       1 |  swansea |    bike |     1 |      1000
         2 |       2 | someMark | bigRack |     1 | 4200.1001
         2 |       3 | someMark |    rack |     2 | 2200.1001

(3 rows)

```

```
select id_client, id_prod, pdesc, writetime(pdesc), quant, writetime(quant) from basket;
```

Casandra nie pozwala na odczyt przed zapisem

```
cqlsh:test> update basket set quant=quant + 100 where client=1 and id_prod=2; 
InvalidRequest: Error from server: code=2200 [Invalid query] message="Invalid operation (quant = quant + 100) for non counter column quant"
```
```
update basket set quant=100 where id_client=2 and id_prod=2;
```

update wiersza który nie istnieje.
Nastąpiła inferencja `addres` bo jest static.

```
cqlsh:test> select id_client, id_prod, pdesc, writetime(pdesc), quant, writetime(quant) from basket;

 id_client | id_prod | pdesc   | writetime(pdesc) | quant | writetime(quant)
-----------+---------+---------+------------------+-------+------------------
         1 |       1 |    bike | 1670756499633119 |     1 | 1670756499633119
         2 |       2 | bigRack | 1670756550609264 |   100 | 1670759016184812
         2 |       3 |    rack | 1670756587144055 |     2 | 1670756587144055

(3 rows)
cqlsh:test> update basket set quant=100 where id_client=2 and id_prod=4;
cqlsh:test> select *  from basket;

 id_client | id_prod | address  | pdesc   | quant | uprice
-----------+---------+----------+---------+-------+-----------
         1 |       1 |  swansea |    bike |     1 |      1000
         2 |       2 | someMark | bigRack |   100 | 4200.1001
         2 |       3 | someMark |    rack |     2 | 2200.1001
         2 |       4 | someMark |    null |   100 |      null

(4 rows)
```

Kasowanie wiersza
```
cqlsh:test> select *  from basket;

 id_client | id_prod | address   | pdesc    | quant | uprice
-----------+---------+-----------+----------+-------+-----------
         5 |       5 | someMark1 | bigRack1 |     1 | 4200.1001
         1 |       1 |   swansea |     bike |     1 |      1000
         2 |       2 |  someMark |  bigRack |   100 | 4200.1001
         2 |       3 |  someMark |     rack |     2 | 2200.1001
         2 |       4 |  someMark |     null |   100 |      null
         4 |       4 |  someMark |  bigRack |     1 | 4200.1001

(6 rows)
cqlsh:test> delete from basket where id_client=5 and id_prod=5; 
cqlsh:test> select *  from basket;

 id_client | id_prod | address   | pdesc   | quant | uprice
-----------+---------+-----------+---------+-------+-----------
         5 |    null | someMark1 |    null |  null |      null
         1 |       1 |   swansea |    bike |     1 |      1000
         2 |       2 |  someMark | bigRack |   100 | 4200.1001
         2 |       3 |  someMark |    rack |     2 | 2200.1001
         2 |       4 |  someMark |    null |   100 |      null
         4 |       4 |  someMark | bigRack |     1 | 4200.1001

(6 rows)
```

usuwanie po zakresie
```
 id_client | id_prod | address   | pdesc   | quant | uprice
-----------+---------+-----------+---------+-------+-----------
         5 |    null | someMark1 |    null |  null |      null
         1 |       1 |   swansea |    bike |     1 |      1000
         2 |       2 |  someMark | bigRack |   100 | 4200.1001
         2 |       3 |  someMark |    rack |     2 | 2200.1001
         2 |       4 |  someMark |    null |   100 |      null
         4 |       4 |  someMark | bigRack |     1 | 4200.1001

(6 rows)
cqlsh:test> delete from basket where id_client=2;
cqlsh:test> select *  from basket;

 id_client | id_prod | address   | pdesc   | quant | uprice
-----------+---------+-----------+---------+-------+-----------
         5 |    null | someMark1 |    null |  null |      null
         1 |       1 |   swansea |    bike |     1 |      1000
         4 |       4 |  someMark | bigRack |     1 | 4200.1001
```
Zobaczyć:

- mem - table, ss - table
- bloom filter
