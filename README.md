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

- Populate
  - [POST /populate/](#post-populate)
  - [POST /populate/v2/](#post-populatev2)
- Auth
  - [POST /auth/](#post-auth)
  - [POST /register/](#post-register)
- Users
  - [GET /users/](#get-users)
  - [GET /users/{id}/](#get-usersid)
  - [PUT /users/{id}/](#put-usersid)
  - [DEL /users/{id}/](#del-usersid)
- Properties
  - [GET /properties/](#get-properties)
  - [POST /properties/](#post-properties)
  - [PUT /properties/{id}/](#put-properties)
  - [GET /properties/{id}/](#get-propertiesid)
  - [DEL /properties/{id}/](#del-propertiesid)
  - [GET /properties/{id}/node/](#get-propertiesidnode)
  - [PUT /properties/{id}/node/](#put-propertiesidnode)
  - [GET /properties/{id}/managers/](#get-propertiesidmanagers)
  - [POST /properties/{id}/managers/{id}/](#post-propertiesidmanagersid)
  - [DEL /properties/{id}/managers/{id}/](#del-propertiesidmanagersid)
- Spaces
  - [GET /spaces/](#get-spaces)
  - [POST /spaces/](#post-spaces)
  - [GET /spaces/{id}/](#get-spacesid)
  - [PUT /spaces/{id}/](#put-spacesid)
  - [DEL /spaces/{id}/](#del-spacesid)
  - [GET /spaces/{id}/restrictions/](#get-spacesidrestrictions)
  - [POST /spaces/{id}/restrictions/](#post-spacesidrestrictions)
  - [PUT /spaces/{id}/restrictions/{id}/](#put-spacesidrestrictionsid)
  - [DEL /spaces/{id}/restrictions/{id}/](#del-spacesidrestrictionsid)
- Plants
  - [GET /plants/](#get-plants)
  - [GET /plants/{id}](#get-plantsid)
- Subspaces
  - [GET /subspaces/](#get-subspaces)
  - [POST /subspaces/](#post-subspaces)
  - [GET /subspaces/{id}/](#get-subspacesid)
  - [PUT /subspaces/{id}/](#put-subspacesid)
  - [DEL /subspaces/{id}/](#del-subspacesid)

- Plans
  - [GET /plans/](#get-plans)
  - [POST /plans/](#post-plans)
  - [GET /plans/{id}/](#get-plansid)
  - [DEL /plans/{id}/](#get-plansid)
- Irrigations
  - [GET /irrigations/](#get-irrigations)
  - [POST /irrigations/](#post-irrigations)
  - [GET /irrigations/{id}/](#get-irrigationsid)
  - [PUT /irrigations/{id}/](#put-irrigationsid)
  - [DEL /irrigations/{id}/](#del-irrigationsid)
- Embedded systems
  - [GET /embeddedsys/](#get-embeddedsys)
  - [POST /embeddedsys/](#post-embeddedsys)
  - [GET /embeddedsys/{id}/](#get-embeddedsysid)
  - [PUT /embeddedsys/{id}/](#put-embeddedsysid)
  - [DEL /embeddedsys/{id}/](#del-embeddedsysid)
- Sensors
  - [GET /sensors/](#get-sensors)
  - [POST /sensors/](#post-sensors)
  - [GET /sensors/{id}/](#get-sensorsid)
  - [PUT /sensors/{id}/](#put-sensorsid)
  - [DEL /sensors/{id}/](#del-sensorsid)
- Reads
  - [GET /reads/](#get-reads)
  - [POST /reads/](#post-reads)
  - [GET /reads/{id}/](#get-readsid)
- Warnings
  - [GET /warnings/](#get-warnings)
  - [POST /warnings/](#post-warnings)
- Operability
  - [~~POST /node/{i}/poweroff/~~](#post-nodeipoweroff)

---

### POST /populate/
Povoa a BD com alguns registos de utilizadores, espaços, etc... Apenas para ambiente de desenvolvimento.

### POST /populate/v2/
Nova versao

### POST /auth/
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

### POST /register/
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

### GET /users/
#### Response
```json
[
  {
    "email": "john@gmail.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_superuser": true,
    "is_active": true,
    "date_joined": "2017-12-22T00:09:12.694391Z"
  }
]
```
### GET /users/{id}/
O id  é o email.\
Resposta: ver [GET /users/](#get-users) - é igual, só que apenas um utilizador é devolvido.
### PUT /users/{id}/
O put é usado para fazer update. Apenas os atributos que forem no pedido são alterados; o que não for indicado fica igual. O email pode ir na mensagem mas não pode ser alterado.

### DEL /users/{id}/
Resposta: OK

### GET /properties/
#### Query Parameters
- *ownerid*: filter by owner id
- *managerid*: filter by manager id

### Response
```json
[
    {
        "prop_id": 1,
        "prop_name": "Property name",
        "prop_description": "Property description",
        "prop_address": "Property address",
        "prop_owner": "john@gmail.com"
    }
]
```

### POST /properties/
#### Body
```json
{
  "prop_name": "Prop name",
  "prop_description": "Prop description",
  "prop_address": "Prop address",
  "prop_owner": "john@gmail.com"
}
```

#### Response
Igual ao pedido, mais o identificador: *prop_id*.

### GET /properties/{id}/
Resposta: semelhante a [GET /properties/](#get-properties)

### PUT /properties/{id}/
Atualiza apenas os atributos indicados; o id pode ir na mensagem mas é ignorado.

### DEL /properties/{id}/
Response: OK

### GET /properties/{id}/node/
O nodo central não tem id próprio. A chave é igual ao id da respetiva propriedade.

#### Response
```json
{
  "node_ip": "123.123.123.123",
  "node_local_lat": -70.0,
  "node_local_long": 150.0,
  "node_local_alt": 20,
  "node_property": 1,
  "node_network_name": "LAN",
  "node_network_password": "password"
}
```
Ou
> 'That property doesn't have a central node' (Codigo 200 OK)

### PUT /properties/{id}/node/
Criação ou update

```json
{
  "node_ip": "123.123.123.123",
  "node_local_lat": -70.0,
  "node_local_long": 150.0,
  "node_local_alt": 20,
  "node_network_name": "LAN",
  "node_network_password": "password"
}
```

### GET /properties/{id}/managers/
Resposta: lista de utilizadores. Igual a [GET /users/](#get-users)

### POST /properties/{id}/managers/{id}/
O corpo da mensagem pode (e deve) ir vazio.\
A resposta são os dados do utilizador que se inseriu como manager.

### DEL /properties/{id}/managers/{id}/
Resposta: OK

### GET /spaces/
#### Query Parameters
- *ownerid*: filter by owner id
- *managerid*: filter by manager id
- *propertyid*: filter by property id

#### Response
```json
[
    {
        "space_id": 1,
        "space_name": "Space name",
        "space_description": "Space description",
        "space_irrigation_hour": 23,
        "space_property": 2,
        "space_plant_type": {
          "plant_type_id": "grass",
          "plant_type_name_eng": "grass",
          "plant_type_name_por": "relva"
        }
    },
]
```

### POST /spaces/

#### Body
```json
{
    "space_name": "Space name",
    "space_description": "Space description",
    "space_irrigation_hour": 23,
    "space_property": 2,
    "space_plant_type": "grass"
}
```
O tipo de planta tem é case sensitive.

### GET /spaces/{id}/
Ver [GET /spaces/](#get-spaces)
### PUT /spaces/{id}/
...
### DEL /spaces/{id}/
...

### GET /spaces/{id}/restrictions/
#### Response
```json
[
    {
        "time_restriction_id": 1,
        "time_restriction_begin": "2017-12-23T00:00:00Z",
        "time_restriction_end": "2017-12-23T00:23:00Z",
        "time_restriction_space": 3
    }
]
```
### POST /spaces/{id}/restrictions/
#### Body
```json
{
	"time_restriction_begin": "2018-01-11T13:00:00Z",
	"time_restriction_end": "2018-01-12T01:00:00Z",
	"time_restriction_space": 3
}
```

### PUT /spaces/{id}/restrictions/{id}/
...
### DEL /spaces/{id}/restrictions/{id}/
...

### GET /plants/
#### Response
```json
[
    {
        "plant_type_id": "grass",
        "plant_type_name_eng": "grass",
        "plant_type_name_por": "relva",
        "plant_param1": "Parametros para o algoritmo de rega",
        "plant_param2": "Para ja nao estao implementados"
    },
]
```
### GET /plants/{id}
...

### GET /subspaces/
#### Reponse
```json
[
    {
        "sub_id": 5,
        "sub_name": "SubEspa22222ço 23",
        "sub_description": "Ao lado da1 estatua do ze",
        "sub_space_id": 3
    },
]
```
#### Parameters
- *propertyid*: filter by property id
- *spaceid*: filter by space id

### POST /subspaces/
#### Body
```json
{
    "sub_name": "SubEspa22222ço 23",
    "sub_description": "Ao lado da1 estatua do ze",
    "sub_space_id": 3
}
```

### GET /subspaces/{id}/
...
### PUT /subspaces/{id}/
...
### DEL /subspaces/{id}/
...

### GET /plans/
#### Response
```json
[
    {
        "dayplan_id": 2,
        "dayplan_gen_time": "2018-01-11T16:51:23.819500Z",
        "dayplan_time": "2017-12-22T00:03:00Z",
        "dayplan_water_qty": 21,
        "dayplan_water_qty_unit": "L",
        "dayplan_sub": 2
    },
]
```

#### Query parameters
- *propertyid*: filter by property
- *spaceid*: fiter by space
- *subspaceid*: fiter by subspace
- *begin_date*: fiter by date > begin_date
- *end_date*: fiter by date < end_date

### POST /plans/
#### Body
```json
{
  "dayplan_time": "2017-12-22T00:03:00Z",
  "dayplan_water_qty": 21,
  "dayplan_sub": 2
}
```

A unidade é o Litro.

### GET /plans/{id}/
...

### GET /irrigations/
#### Response
```json
[
    {
        "irrigation_time_id": 5,
        "irrigation_time_date": "2018-01-02T00:00:00Z",
        "irrigation_time_qty": 10,
        "irrigation_time_qty_unit": "L",
        "irrigation_time_sub": 4
    },
]
```
#### Query parameters
- *propertyid*: filter by property
- *spaceid*: fiter by space
- *subspaceid*: fiter by subspace
- *begin_date*: fiter by date > begin_date
- *end_date*: fiter by date < end_date

### POST /irrigations/

#### Body
```json
{
  "irrigation_time_date": "2018-01-02T00:00:00Z",
  "irrigation_time_qty": 10,
  "irrigation_time_sub": 4
}
```

A unidade é o Litro.

### GET /irrigations/{id}/
...
### PUT /irrigations/{id}/
Está feito, mas será que faz sentido editar isto?

### DEL /irrigations/{id}/
...

### GET /embeddedsys/
#### Response
```json
{
    "esys_id": 1,
    "esys_local_long": 150.0,
    "esys_local_lat": -75.0,
    "esys_local_alt": 5,
    "esys_sub": 1,
    "esys_state": 1,
    "esys_name": "Name"
},
```
#### Parameters
- *subspaceid*: filter by subspace id

### POST /embeddedsys/
#### Body
```json
{
  "esys_local_long": 150.0,
  "esys_local_lat": -75.0,
  "esys_local_alt": 5,
  "esys_sub": 1,
  "esys_state": 1,
  "esys_name": "Name"
}
```

### GET /embeddedsys/{id}/
...
### PUT /embeddedsys/{id}/
...
### DEL /embeddedsys/{id}/
...

### GET /sensors/
```json
[
    {
        "sensor_id": 2,
        "sensor_name": "Name",
        "sensor_state": 1,
        "sensor_esys": 2,
        "sensor_timerate": 101,
        "sensor_depth": 201,
        "sensor_type": {
            "sensor_type_name_eng": "humidity",
            "sensor_type_name_por": "humidade",
            "sensor_type_unit": "ml"
        }
    },
]
```
#### Parameters
- *subspaceid*: filter by subspace id
- *embeddedsysid*: filter by embedded system id

### POST /sensors/
No tipo do sensor, tem que ir exatamente a string "humidity" (Case sensitive). No futuro, teriamos "temperature", etc. A unidade para cada tipo de sensor é estática. No caso da humidade é ml ou mm ou o que for, tem que se ver, mas não é definida pelo utilizador - é estática.

#### Body
```json
{
    "sensor_name": "Name",
    "sensor_state": 1,
    "sensor_esys": 2,
    "sensor_timerate": 101,
    "sensor_depth": 201,
    "sensor_type": "humidity"
}
```

### GET /sensors/{id}/
...
### PUT /sensors/{id}/
...
### DEL /sensors/{id}/
...

### GET /reads/

#### Response
```json
[
    {
        "read_id": 2,
        "read_timestamp": "2018-01-11T16:51:23.860205Z",
        "read_value": 100,
        "read_sensor": 2,
    },
]
```
A unidade da leitura está associada ao sensor.

#### Parameters
- *subspaceid*: filter by subspace id
- *embeddedsysid*: filter by embedded system id
- *sensorid*: filter by sensor id

### POST /reads/
#### Body
```json
{
  "read_timestamp": "2018-01-11T16:51:23.860205Z",
  "read_value": 100,
  "read_sensor": 2,
}
```

### GET /reads/{id}/
...

### GET /warnings/
#### Parameters
- *propertyid*: filter by property id

#### Response
```json
[
  {
      "warning_id": "id",
      "warning_description": "description",
      "warning_property": 1
  },
]
```

### POST /warnings/
Estes warnings são para coisas do género: um sensor deixa de funcionar ou o sistema de metereologia não responde. Ainda não está bem definido.

#### Body
```json
{
    "warning_description": "description",
    "warning_property": 1
}
```

#### Query Parameters
- *propertyid*: filter by property


### POST /node/{id}/poweroff/
Desliga totalmente o nodo central. Depois a ativação teria que ser manual? **PRIORIDADE BAIXA**
#### Body
> Empty body
