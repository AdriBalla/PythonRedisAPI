# Dockerized Scalable Redis - Python API

This API allows you to dynamically add data to several redis servers. 

Each server can be identified by a name and its automatically created when data is added using the API.


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

## Accessing the API

```
API address : localhost:5000
```

|URL|Method|Attributes|Description|
---|---|---|---|
/status|GET||Return the status of the API
/databases|GET||Return a Json dictionary of all databases names available
/databases/{databaseName}/data|GET||Return a Json dictionary of all entry in a database
/databases/{databaseName}/data|GET|keys (Json encoded array of keys) |Return a Json dictionary of the entry responding to keys in a database
/databases/{databaseName}/data/{key}|GET||Return a Json dictionary of the key value in the database
/databases/{databaseName}/data|POST,PUT|key,value|Insert or update the key value couple in a database
/databases/{databaseName}/data|POST,PUT|data (Json encoded dictionary)|Insert or update the key value couples encoded in a Json dictionary into a database
/databases/{databaseName}/data/{key}|DELETE||Delete a key value couple from a database
/databases/{databaseName}/data|DELETE|keys (Json encoded array of keys)|Delete a batch of key value couple from a database
/databases/{databaseName}|DELETE||Delete a whole database

## Result

If the operation is a success the API returns { message : Success }

If the operation is a failure, the Api returns { message : Description of the failure ]

Every returned data is Json encoded as a dictionary of key => value couple.

## Accessing Redis Commander

```
localhost:8081
```

## Kill the Project

```
make up
```


