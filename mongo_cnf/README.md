## Step 1: Запуск контейнеров

- выполнить команду в терминале ```$ docker-compose up```

## Step 2: Создание кластера

 последовательно выполните команды в терминале:
- ```$ docker exec -it mongocfg1 sh -c "mongosh < /scripts/mongocfg1.js"```
- ```$ docker exec -it mongors1n1 sh -c "mongosh < /scripts/mongors1n1.js"```
- ```$ docker exec -it mongors2n1 sh -c "mongosh < /scripts/mongors2n1.js"```
- ```$ docker exec -it mongos1 sh -c "mongosh < /scripts/mongos1.js"```

## Step 3: Создание db

последовательно выполните команды в терминале:
- ```$ docker exec -it mongors1n1 bash -c 'echo "use ugc_db" | mongosh'"```
- ```$ docker exec -it mongos1 sh -c "mongosh < /scripts/ugc_db.js"```


[reference](https://github.com/minhhungit/mongodb-cluster-docker-compose)