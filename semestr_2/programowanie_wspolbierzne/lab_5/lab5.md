## Rabit MQ 

```shell
docker run -d --name rabbit -h rabbit -p 5672:5672 -p 8080:15672 rabbitmq:3-management
```

```shell
pip install pika
```

Wysłanie wiadomości przez Rabbit MQ
```shell
$ python ./rabbit_hello_world.py recive 
Start consuming

```

```shell
$ python ./rabbit_hello_world.py send "Hello world" 
Message Hello world published
```

```shell
$ python ./rabbit_hello_world.py recive 
Start consuming
Received message b'Hello world'
```

## Prefetch 

Domyślnie przy wielu konsumentach `rabbit mq` przydziela wiadomości gdy wchodzą one do kolejki. 
Jest to problem gdy chcemy równoważyć obciążenie. 
