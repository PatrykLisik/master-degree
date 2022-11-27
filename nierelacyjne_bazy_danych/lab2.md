# Lab2 - Potoki agregacji 

tworzenie bazy danych
```javascript
db.createCollection('at');
```

wstawiamy dane testowe 

```javascript
for(let i=1;i<201;i++){
 db.at.insertOne({
        _id: i,
         val1: 100*Math.random(),
         val2: 10*Math.random(),
         gr: Math.floor(10*Math.random())
     });}
// informacja zwrotna z mongo
{ "acknowledged" : true, "insertedId" : 200 }
```
Wiele operatorów wystęuje w dwóch wersjach: dla wszystkich operacji i dla potoków agregacji.

Wypisz obiekty gdzie val1 jest większe niż 30
```javascript
db.at.aggregate([{$match: {val1: {$gt: 30}}}]);
```
wypisz obiekty gdzie val2 jest większy niż val1
```javascript
db.at.aggregate([{$match: {$expr: {$lt: ["$val1", "$val2"]}}}]);
```


Agregacja per grupa i sumy wartośći val1 i val2

```javascript 
db.at.aggregate([{$match: {val1: {$gt: 30}}}, {$group: {_id: "$gr", sum1: {$sum: "$val1"}, sum2: {$sum: "$val2"}}}]);
```

Wypisanie wyników potoku do nowej tabeli result
```javascript
db.at.aggregate([{$match: {val1: {$gt: 30}}}, {$group: {_id: "$gr", sum1: {$sum: "$val1"}, sum2: {$sum: "$val2"}}}, {$sort: {_id: -1}}, {$out: "result"}]);
```

```javascript 
db.at.aggregate([{$match: {val1: {$gt: 30}}}, {$group: {_id: "$gr", sum1: {$sum: "$val1"}, sum2: {$sum: "$val2"}}}, {$sort: {_id: -1}}]);
```

```javascript 
db.result.aggregate([{$set: {total: {$sum: ["$sum1", "$sum2"]}}}, {$project: {total: true}}]);
```

```javascript
db.result.aggregate([{$set: {total: {$sum: ["$sum1", "$sum2"]}}}, {$project: {total: true}}, {$group: {_id: {$mod: ["$_id", 3]}, docs: {$push: {gr: "$_id", total: "$total"}}}}]);
```

```javascript
db.at.aggregate([{$match: {val1: {$lt: 50.0}}}, {$out: {db:"test", coll: "at2"}}]);

db.result.aggregate([{$lookup: {from: 'at2', localField: '_id', foreignField: 'gr', as: "docs"}}]);
```

```javascript

```


```javascript

```