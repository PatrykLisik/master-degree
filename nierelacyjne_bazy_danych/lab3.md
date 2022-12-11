# Replikacja 

Wspólna sieć dla kontenerów

``` 
docker network create -d bridge nosqlnet
```

Kontenery mongo

```
docker run -d --name mongo0 --network nosqlnet mongo:4.4.6 --replSet myrs
docker run -d --name mongo1 --network nosqlnet mongo:4.4.6 --replSet myrs
docker run -d --name mongo2 --network nosqlnet mongo:4.4.6 --replSet myrs
```

`docker exec -it mongo0 mongo`

w mongo 0
```
rs.initiate({
 _id: "myrs", 
 members: [
 {_id: 0, host: "mongo0"},
 {_id: 1, host: "mongo1"}, 
 {_id: 2, host: "mongo2"}
 ]
});
```

`db.createCollection("rs1")`

`db.rs1.insertMany([{_id:1},{_id:2},{_id:3}]);`


W mongo1

 `db.getMongo().setReadPref("primaryPreferred")`
 
 `db.rs1.find()` - mamy dane z primary(mongo0)

```
db.rs1.insertMany([{_id:5},{_id:4}]);
myrs:SECONDARY> db.rs1.find()
{ "_id" : 3 }
{ "_id" : 1 }
{ "_id" : 2 }
```


`docker kill mongo0` zabijamy primary 

```
 "members" : [
                {
                        "_id" : 0,
                        "name" : "mongo0:27017",
                        "health" : 0,
                        "state" : 8,
                        "stateStr" : "(not reachable/healthy)",
                        "uptime" : 0,
                        "optime" : {
                                "ts" : Timestamp(0, 0),
                                "t" : NumberLong(-1)
                        },
                        "optimeDurable" : {
                                "ts" : Timestamp(0, 0),
                                "t" : NumberLong(-1)
                        },
                        "optimeDate" : ISODate("1970-01-01T00:00:00Z"),
                        "optimeDurableDate" : ISODate("1970-01-01T00:00:00Z"),
                        "lastHeartbeat" : ISODate("2022-12-11T10:31:37.127Z"),
                        "lastHeartbeatRecv" : ISODate("2022-12-11T10:31:24.879Z"),
                        "pingMs" : NumberLong(0),
                        "lastHeartbeatMessage" : "Couldn't get a connection within the time limit of 486ms",
                        "syncSourceHost" : "",
                        "syncSourceId" : -1,
                        "infoMessage" : "",
                        "configVersion" : 1,
                        "configTerm" : 1
                },
                {
                        "_id" : 1,
                        "name" : "mongo1:27017",
                        "health" : 1,
                        "state" : 2,
                        "stateStr" : "SECONDARY",
                        "uptime" : 1400,
                        "optime" : {
                                "ts" : Timestamp(1670754682, 1),
                                "t" : NumberLong(1)
                        },
                        "optimeDate" : ISODate("2022-12-11T10:31:22Z"),
                        "syncSourceHost" : "",
                        "syncSourceId" : -1,
                        "infoMessage" : "",
                        "configVersion" : 1,
                        "configTerm" : 1,
                        "self" : true,
                        "lastHeartbeatMessage" : ""
                },
                {
                        "_id" : 2,
                        "name" : "mongo2:27017",
                        "health" : 1,
                        "state" : 1,
                        "stateStr" : "PRIMARY",
                        "uptime" : 1185,
                        "optime" : {
                                "ts" : Timestamp(1670754682, 1),
                                "t" : NumberLong(1)
                        },
                        "optimeDurable" : {
                                "ts" : Timestamp(1670754682, 1),
                                "t" : NumberLong(1)
                        },
                        "optimeDate" : ISODate("2022-12-11T10:31:22Z"),
                        "optimeDurableDate" : ISODate("2022-12-11T10:31:22Z"),
                        "lastHeartbeat" : ISODate("2022-12-11T10:31:36.957Z"),
                        "lastHeartbeatRecv" : ISODate("2022-12-11T10:31:37.129Z"),
                        "pingMs" : NumberLong(0),
                        "lastHeartbeatMessage" : "",
                        "syncSourceHost" : "",
                        "syncSourceId" : -1,
                        "infoMessage" : "",
                        "electionTime" : Timestamp(1670754695, 1),
                        "electionDate" : ISODate("2022-12-11T10:31:35Z"),
                        "configVersion" : 1,
                        "configTerm" : 1
                }
```

zostaje wybrany nowy primary 
```
"members" : [
                {
                        "_id" : 0,
                        "name" : "mongo0:27017",
                        "health" : 0,
                        "state" : 8,
                        "stateStr" : "(not reachable/healthy)",
                        "uptime" : 0,
                        "optime" : {
                                "ts" : Timestamp(0, 0),
                                "t" : NumberLong(-1)
                        },
                        "optimeDurable" : {
                                "ts" : Timestamp(0, 0),
                                "t" : NumberLong(-1)
                        },
                        "optimeDate" : ISODate("1970-01-01T00:00:00Z"),
                        "optimeDurableDate" : ISODate("1970-01-01T00:00:00Z"),
                        "lastHeartbeat" : ISODate("2022-12-11T10:32:34.127Z"),
                        "lastHeartbeatRecv" : ISODate("2022-12-11T10:31:24.879Z"),
                        "pingMs" : NumberLong(0),
                        "lastHeartbeatMessage" : "Couldn't get a connection within the time limit of 1000ms",
                        "syncSourceHost" : "",
                        "syncSourceId" : -1,
                        "infoMessage" : "",
                        "configVersion" : 1,
                        "configTerm" : 1
                },
                {
                        "_id" : 1,
                        "name" : "mongo1:27017",
                        "health" : 1,
                        "state" : 2,
                        "stateStr" : "SECONDARY",
                        "uptime" : 1467,
                        "optime" : {
                                "ts" : Timestamp(1670754757, 1),
                                "t" : NumberLong(2)
                        },
                        "optimeDate" : ISODate("2022-12-11T10:32:37Z"),
                        "syncSourceHost" : "mongo2:27017",
                        "syncSourceId" : 2,
                        "infoMessage" : "",
                        "configVersion" : 1,
                        "configTerm" : 2,
                        "self" : true,
                        "lastHeartbeatMessage" : ""
                },
                {
                        "_id" : 2,
                        "name" : "mongo2:27017",
                        "health" : 1,
                        "state" : 1,
                        "stateStr" : "PRIMARY",
                        "uptime" : 1251,
                        "optime" : {
                                "ts" : Timestamp(1670754757, 1),
                                "t" : NumberLong(2)
                        },
                        "optimeDurable" : {
                                "ts" : Timestamp(1670754757, 1),
                                "t" : NumberLong(2)
                        },
                        "optimeDate" : ISODate("2022-12-11T10:32:37Z"),
                        "optimeDurableDate" : ISODate("2022-12-11T10:32:37Z"),
                        "lastHeartbeat" : ISODate("2022-12-11T10:32:43.669Z"),
                        "lastHeartbeatRecv" : ISODate("2022-12-11T10:32:43.139Z"),
                        "pingMs" : NumberLong(0),
                        "lastHeartbeatMessage" : "",
                        "syncSourceHost" : "",
                        "syncSourceId" : -1,
                        "infoMessage" : "",
                        "electionTime" : Timestamp(1670754695, 1),
                        "electionDate" : ISODate("2022-12-11T10:31:35Z"),
                        "configVersion" : 1,
                        "configTerm" : 2
                }
        ],

```