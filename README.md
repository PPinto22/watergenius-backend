# aquasmart-bakend
Backend

## Iniciar a aplicação
neste momento o docker não está a iniciar o django, apenas a db e o angular.

para inicar o django uma primeira vez no vosso ambiente é preciso fazer o seguinte.

Iniciar o docker-compose no projeto principal e depois executar o seguinte

```
docker-compose exec db bash

psql -h localhost -U postgres

CREATE DATABASE watergenius;

python3.5 manage.py makemigrations

python3.5 manage.py migrate

python3.5 manage.py runserver
```