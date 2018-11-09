# Dockerized Scalable Redis - Python API

This API allows you to dynamically add data to several redis servers. 

Each server can be identified by a name and its automatically created when data is added through the API.


It is composed of three containers : 

*    api_python         : Debian with Python Flask
*    api_redis          : The Redis server
*    api_rediscommander : GUI for Redis


## Getting Started

Clone the project by using the following command :

```
git clone https://github.com/AdriBalla/PythonRedisAPI.git
```

## Run the Project

```
make up
```

## Endpoints of the API

|URL|Method|Attributes|Description|
---|---|---|---|
localhost:5000/databases|GET||Displays all databases
localhost:5000/databases/{databaseName}/data|GET||Displays all entry in a database
localhost:5000/databases/{databaseName}/data/{key}|GET||Displays the value of the key from a database
localhost:5000/databases/{databaseName}/data|POST,PUT|key,value|Insert or update the key value couple in a database
localhost:5000/databases/{databaseName}/data/{key}|DELETE||Delete a key value couple from a database
localhost:5000/databases/{databaseName}|DELETE||Delete a whole database


## Accessing Redis Commander

```
localhost:8081
```

## Kill the Project

```
make up
```


