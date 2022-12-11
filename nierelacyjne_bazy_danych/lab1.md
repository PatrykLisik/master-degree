# Zaliczenie 
Prowadzący — Bartosz Zieliński 
zadanie praktyczne na koniec 

# Mięso
### Mongo 
- prowadzący nie lubi mongo
- baza dokumentowa 
- przechowuje dane w formacie podobnym do jsona 
- model hierarchiczny 
- jeśli chcemy przechowywać dane jako json to należy poczekać aż nam przejdzie 
- json dobry gdy przechowujmy dane o różnej scheme'ie 
- większość relacyjnych baz danych pozwala na przechowywanie i operacje na jsonach z ACID i elementrami relacyjnymi 
- wolniejsze niż Postgres przy operacjach na json
- skalowanie prostsze niż przy bazach sql
- jeśli się nie postaramy to mongo nie daje transakcji na wielu dokumentach  
- transakcje tylko w grupach replikacji 
- jeśli nie replikujmy mongo to nie potrzebujemy mongo 
- wiedza o mnongo jest tylko po to, żeby móc nim pogardzać 
- część stosu MERN 

### Maszyna

#### Docker na szybko
- Docker pozwala na lepszą izolację niż procesy 
- tańszy niż maszyny wirtualne 
- nie ma ryzyka konfliktów z tym, co jest w systemie
- wygodny z administracyjengo punktu widzenia 
- obrazy są dzielona pomiędzy kontenerami => efektywne wykorzystanie dysku 

Poza grafowymi bazami danych otrzymujemy uboższy model danych w zamian dostajemy skalowalność.
Replikacja Rozpraszanie horozyzontalne 



```commandline
ssh root@127.0.0.1 -p 2002
```

hasło: student

instalujemy mongo 
```commandline
docker run -d --name mongo mongo:4.4.6
```

shell mongo
```commandline
docker exec -it mongo mongo
```

komendy w mongo shell 

tworzenie bazy danych
```javascript
db.createCollection('books_by_author');
```

```javascript
db.books_by_authors.insertOne({
    _id: 1, 
    "author": 'H.P. Lovecraft',
    "books": [
        {
            "title": 'Call of Cthulu',
            type: 'short story',
            pages: 20,
            genre: 'horror'
        },
        {
            title: 'At the montains of madness',
            type: 'novel',
            pages: 200
        }
    ]
});
```

```
db.books_by_authors.insertMany([
    {
        _id: 2, 
        author: 'G.H. Chesterton',
        books: [
            {
                title: 'Adventures of father Brown',
                type: 'short story collection',
                pages: 100
            }
        ]
    },
    {
        _id: 3,
        author: 'Tolkien',
        books: [
            {
                title: 'Hobbit'
            }
        ]
    }
]);
```

```javascript
db.books_by_authors.createIndex({author: 1}, {unique: true});
```

```javascript
db.books_by_authors.find({author: 'Tolkien'});
```

```javascript
db.books_by_authors.find({_id: 1}, {author: 1});
```

```javascript
db.books_by_authors.find({"books.title":"Call of Cthulu"}, {author: 1});
```

```
db.books_by_authors.deleteOne({author:'A. Christie'});

db.books_by_authors.updateOne({_id: 1}, {$set: {price: 100.00}});

db.books_by_authors.updateOne({_id: 1}, {$unset: {price: 1}});

db.books_by_authors.updateOne({_id: 1}, {$set: {"books.0.price": 200.00, "books.1.price": 300.00}});
```


### Zdanie
- Wstawić dokumenty opisujące bazę fotografii.
- Jeden dokument - jedna fotografia
- Dla każdej fotografii dokument powinien zawierać: identyfikator, nazwę pliku, opis, tablicę kategorii, datę i miejsce, oraz dokument z szerokością i wysokością w pikselach
- Wstawić kilka przykładowych dokumentów
- Podać zapytanie, które wyszukuje fotografie z danej kategorii.
- Zmodyfikować opis w wybranej fotografii
- Podać zapytanie, które wyszukuje fotografie o szerokości większej niż 1000 i wysokości większej niż 800


```
db.photos.insertMany([
    {
        _id: 5, 
        "file_name": 'G.H. Chesterton',
        "categories": ["aaa", "bbb:"],
        "date": "05.11.22",
        "place": "Łódź",
        "size": {
            "height":480,
            "width": 800
            }
    },
    {
        _id: 6, 
        "file_name": "ddddd",
        "categories": ["bbb:"],
        "date": "05.11.22",
        "place": "Łódź",
        "size": {
            "height": 1000,
            "width": 2000
            }
    },
    {
        _id: 3, 
        "file_name": "ddddd2",
        "categories": ["bbb:"],
        "date": "05.11.22",
        "place": "Łódź",
        "size": {
            "height": 1000,
            "width": 2000
            }
    },
    {
        _id: 4, 
        "file_name": "ddddd3",
        "categories": ["aaa"],
        "date": "05.11.22",
        "place": "Łódź",
        "size": {
            "height": 1000,
            "width": 2000
            }
    },

]);
```