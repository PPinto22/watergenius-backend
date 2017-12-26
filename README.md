# aquasmart-bakend
Backend

## Iniciar a aplicação
neste momento o docker não está a iniciar o django, apenas a db e o angular.

para inicar o django uma primeira vez no vosso ambiente é preciso fazer o seguinte.

Iniciar o docker-compose no projeto principal e depois executar o seguinte

```
docker-compose exec db bash

psql -h localhost -U postgres -d watergenius

CREATE DATABASE watergenius;

exit

pip3.6 install -r requirements/docker.txt --upgrade

python3.6 manage.py makemigrations

python3.6 manage.py migrate

python3.6 manage.py runserver
```

## API

- Auth
  - [POST /auth](#post-auth)
  - [POST /register](#post-register)

- Users
  - [GET /users](#get-users)
  - [GET /users/{id}](#get-usersid)
  - [PUT /users/{id}](#put-usersid)
  - [DEL /users/{id}](#del-usersid)
- Properties
  - [GET /properties](#get-properties)
  - [PUT /properties](#put-properties)
  - [POST /properties/{id}](#post-properties)
  - [GET /properties/{id}](#get-propertiesid)
  - [DEL /properties/{id}](#del-propertiesid)
  - [GET /properties/{id}/node](#get-propertiesidnode)
  - [POST /properties/{id}/node](#post-propertiesidnode)
  - [PUT /properties/{id}/node](#put-propertiesidnode)
  - [GET /properties/{id}/managers/](#get-propertiesidmanagers)
  - [PUT /properties/{id}/managers/{id}](#post-propertiesidmanagersid)
  - [DEL /properties/{id}/managers/{id}](#del-propertiesidmanagersid)
- Spaces
  - [GET /spaces](#get-spaces)
  - [POST /spaces](#post-spaces)
  - [GET /spaces/{id}](#get-spacesid)
  - [PUT /spaces/{id}](#put-spacesid)
  - [DEL /spaces/{id}](#del-spacesid)
  - [GET /spaces/{id}/restrictions](#get-spacesidrestrictions)
  - [PUT /spaces/{id}/restrictions](#post-spacesidrestrictions)
  - [POST /spaces/{id}/restrictions/{id}](#put-spacesidrestrictionsid)
  - [DEL /spaces/{id}/restrictions/{id}](#del-spacesidrestrictionsid)
- Plants
  - [GET /plants](#get-plants)
- Subspaces
  - [GET /subspaces](#get-subspaces)
  - [~~POST /subspaces~~](#post-subspaces)
  - [~~GET /subspaces/{id}~~](#get-subspacesid)
  - [~~PUT /subspaces/{id}~~](#put-subspacesid)
  - [~~DEL /subspaces/{id}~~](#del-subspacesid)
- Plans
  - [GET /plans](#get-plans)
  - [~~POST /plans~~](#post-plans)
  - [~~GET /plans/{id}~~](#get-plansid)
- Irrigations
  - [GET /irrigations](#get-irrigations)
  - [~~POST /irrigations~~](#post-irrigations)
  - [~~GET /irrigations/{id}~~](#get-irrigationsid)
  - [~~PUT /irrigations/{id}~~](#put-irrigationsid)
  - [~~DEL /irrigations/{id}~~](#del-irrigationsid)
- Embedded systems
  - [GET /embeddedsys](#get-embeddedsys)
  - [~~POST /embeddedsys~~](#post-embeddedsys)
  - [~~GET /embeddedsys/{id}~~](#get-embeddedsysid)
  - [~~PUT /embeddedsys/{id}~~](#put-embeddedsysid)
  - [~~DEL /embeddedsys/{id}~~](#del-embeddedsysid)
- Sensors
  - [GET /sensors](#get-sensors)
  - [~~POST /sensors~~](#post-sensors)
  - [~~GET /sensors/{id}~~](#get-sensorsid)
  - [~~PUT /sensors/{id}~~](#put-sensorsid)
  - [~~DEL /sensors/{id}~~](#del-sensorsid)
- Reads
  - [GET /reads](#get-reads)
  - [~~POST /reads~~](#post-reads)
  - [~~GET /reads/{id}~~](#get-readsid)
- Warnings
  - [GET /warnings](#get-warnings)
  - [~~POST /warnings~~](#post-warnings)
- Operability
  - [~~POST /node/{i}/poweroff~~](#post-nodeipoweroff)

---

### POST /auth
A autenticação é feita por JWT. Esta rota recebe as credenciais do utilizador (email e password) e devolve um token que deve ir em todas as próximas mensagens no campo Authorization do cabeçalho HTTP, da seguinte forma:

> JWT &lt;Token>


#### Body
```json
{
  "email": "john@gmail.com",
  "password": "password"
}
```

#### Response
```json
{
  "token": "eyJ0p.eyJ1c.u8vNO"
}
```

#### Exceptions
- **Bad Request (400)** - Invalid credentials

Em comunicações posteriores à autenticação, quando o token não for válido:
- **Unauthorized (401)**

### POST /register
#### Body
```json
{
  "email": "john@gmail.com",
  "password": "password",
  "first_name": "John",
  "last_name": "Doe",
  "is_superuser": true
}
```
O campo "is_superuser" define se o utilizador a ser criado é admin ou não. Não é obrigatório ir na mensagem, tomando o valor ``false`` por defeito. Só um admin é que tem permissões para criar outro admin **(Isto ainda não está implementado)**.

#### Response
Igual ao Body - a chave é o email.

#### Exceptions
- **Bad Request (400)** -
```json
{
  "email": ["user with this email already exists."],
  "password": ["This field is required."],
  "etc..."
}
```

### GET /users
#### Response
```json
[
  {
    "email": "john@gmail.com",
    "password": "password",
    "first_name": "John",
    "last_name": "Doe",
    "is_superuser": true
  }
]
```
### GET /users/{id}
### PUT /users/{id}
### DEL /users/{id}

### GET /properties
#### Parameters
- *owner*: filter by owner id
- *manager*: filter by manager id

### POST /properties
#### Body
```json
{
  "user": 1,
  "..."
}
```
### GET /properties/{id}
### PUT /properties/{id}
### DEL /properties/{id}

### GET /properties/{id}/node
### POST /properties/{id}/node
### PUT /properties/{id}/node

### GET /properties/{id}/managers

### POST /properties/{id}/managers/{id}
#### Body
> Empty body

### DEL /properties/{id}/managers/{id}

### GET /spaces
#### Parameters
- *owner*: filter by owner id
- *manager*: filter by manager id
- *property*: filter by property id

### POST /spaces
#### Body
```json
{
  "property": 1,
  "..."
}
```

### GET /spaces/{id}
### PUT /spaces/{id}
### DEL /spaces/{id}

### GET /spaces/{id}/restrictions
### POST /spaces/{id}/restrictions

### PUT /spaces/{id}/restrictions/{id}
### DEL /spaces/{id}/restrictions/{id}

### GET /plants
Ainda está por decidir se isto é para fazer. A ideia é para ter um auto-complete ou algo do género quando o utilizador for inserir o tipo de planta num espaço. **PRIORIDADE BAIXA**

### GET /subspaces
#### Parameters
- *property*: filter by property id
- *space*: filter by space id

### POST /subspaces

### GET /subspaces/{id}
### PUT /subspaces/{id}
### DEL /subspaces/{id}

### GET /plans
#### Parameters
- *property*: filter by property id
- *space*: filter by space id
- *subspace*: filter by subspace id
- *begin_date*: filter by time interval (datetime)
- *end_date*: filter by time interval (datetime)

### POST /plans
#### Body
```json
{
  "subspace": 1,
  "..."
}
```

### GET /plans/{id}

### GET /irrigations
#### Parameters
- *property*: filter by property id
- *space*: filter by space id
- *subspace*: filter by subspace id
- *begin-date*: filter by time interval (datetime)
- *end-date*: filter by time interval (datetime)

### POST /irrigations
#### Body
```json
{
  "subspace": 1,
  "..."
}
```

### GET /irrigations/{id}
### PUT /irrigations/{id}
### DEL /irrigations/{id}

### GET /embeddedsys
#### Parameters
- *subspace*: filter by subspace id

### POST /embeddedsys
#### Body
```json
{
  "subspace": 1,
  "..."
}
```

### GET /embeddedsys/{id}
### PUT /embeddedsys/{id}
### DEL /embeddedsys/{id}

### GET /sensors
#### Parameters
- *subspace*: filter by subspace id
- *embeddedsys*: filter by embedded system id

### POST /sensors
#### Body
```json
{
  "embeddedsys": 1,
  "..."
}
```

### GET /sensors/{id}
### PUT /sensors/{id}
### DEL /sensors/{id}

### GET /reads
#### Parameters
- *subspace*: filter by subspace id
- *embeddedsys*: filter by embedded system id
- *sensor*: filter by sensor id

### POST /reads
#### Body
```json
{
  "sensor": 1,
  "..."
}
```

### GET /reads/{id}

### GET /warnings
#### Parameters
- *property*: filter by property id

### POST /warnings
Estes warnings são para coisas do género: um sensor deixa de funcionar ou o sistema de metereologia não responde. Este POST é muito questionável ... a discutir melhor. **PRIORIDADE BAIXA**

#### Body
```json
{
  "property": 1,
  "error_code": "001",
}
```

### POST /node/{id}/poweroff
Desliga totalmente o nodo central. Depois a ativação teria que ser manual? **PRIORIDADE BAIXA**
#### Body
> Empty body
