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
localhost:5000/status|GET||Return the status of the API
localhost:5000/databases|GET||Return a Json dictionary of all databases names available
localhost:5000/databases/{databaseName}/data|GET||Return a Json dictionary of all entry in a database
localhost:5000/databases/{databaseName}/data|GET|keys (Json encoded array of keys) |Return a Json dictionary of the entry responding to keys in a database
localhost:5000/databases/{databaseName}/data/{key}|GET||Return a Json dictionary of the key value in the database
localhost:5000/databases/{databaseName}/data|POST,PUT|key,value|Insert or update the key value couple in a database
localhost:5000/databases/{databaseName}/data|POST,PUT|data (Json encoded dictionary)|Insert or update the key value couples encoded in a Json dictionary into a database
localhost:5000/databases/{databaseName}/data/{key}|DELETE||Delete a key value couple from a database
localhost:5000/databases/{databaseName}|DELETE||Delete a whole database

## Result

If an operation is a success, the default result is "true".

Every returned data is Json encoded as a dictionary of key => value couple.

## Accessing Redis Commander

```
localhost:8081
```

## Kill the Project

```
make up
```


