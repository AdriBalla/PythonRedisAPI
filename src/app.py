from flask import Flask, render_template, request, redirect, url_for, send_file, Response,jsonify
import json, redis

app = Flask(__name__)


# DATABASE NAME POOL
DB_POOL = redis.ConnectionPool(host='api_redis', port=6379, db=0)

#
# Retreive the Redis Server acting as a registry for all databases name
#
def getRedisDbRegistryServer():
	return redis.Redis(connection_pool=DB_POOL)

#
# Retreive the Redis Server for a database according to its name
#
def getRedisServer(databaseName):
	pool = redis.ConnectionPool(host='api_redis', port=6379, db=getDBIndex(databaseName))
	return redis.Redis(connection_pool=pool)

#
# Add an entry to a Redis Server according to the database name
#
def setData(databaseName,key,value):
	redisServer = getRedisServer(databaseName)
	return redisServer.set(key, value)

#
# Add an entry to a Redis Server according to the database name and the key
#
def getData(databaseName,key):
	redisServer = getRedisServer(databaseName)
	return redisServer.get(key)


#
# Delete an entry to a Redis Server according to the database name and the key
#
def deleteData(databaseName,key):
	redisServer = getRedisServer(databaseName)
	return redisServer.delete(key)


#
# Get all entry to Redis Server according to the database Name
#
def getAllData(databaseName):
	returnValue = {}
	redisServer = getRedisServer(databaseName)
	for key in redisServer.keys():
		returnValue[key] = redisServer.get(key)
	return returnValue

#
# Delete all entry to Redis Database according to database name
#
def deleteAllData(databaseName):
	redisServer = getRedisServer(databaseName)
	for key in redisServer.keys():
		redisServer.delete(key)


#
# Get all entry to Redis Server according to the database Name
#
def getAllDatabases():
	returnValue = {}
	redisServer = getRedisDbRegistryServer()
	for key in redisServer.keys():
		returnValue[key] = redisServer.get(key)
	return returnValue

#
# Get the index of a database in the registry of databases
#
def getDBIndex(databaseName):
	redisServer = getRedisDbRegistryServer()
	returnValue = redisServer.get(databaseName)
	if (returnValue == None):
		returnValue = getNextDBIndex()
		redisServer.set(databaseName, returnValue)
	return returnValue


#
# Get the available index in the registry database for a new database
#
def getNextDBIndex():
	returnValue = None
	dbIndexs = []
	redisServer = getRedisDbRegistryServer()
	for key in redisServer.keys():
		dbIndexs.append(int(redisServer.get(key)))
	for x in range (1,15):
		if not (x in dbIndexs):
			returnValue = x
			break
	return returnValue


#
# Remove a database from the registry database
#
def deleteDBIndex(databaseName):
	redisServer = getRedisDbRegistryServer()
	return redisServer.delete(databaseName)


#
# Routes
#
@app.route('/status')
def check_status():
	returnValue = {"status":"true"}
	return json.dumps(returnValue)


@app.route("/databases/", defaults={'key': None,'databaseName' : None}, methods=['GET'])
@app.route("/databases/<databaseName>", defaults={'key': None}, methods=['GET'])
@app.route("/databases/<databaseName>/<key>", methods=['GET'])
def readData(databaseName,key):
	if (databaseName == None):
		return json.dumps(getAllDatabases())
	if (key != None):
		return json.dumps({key:getData(databaseName,key)})
	else:
		return json.dumps(getAllData(databaseName))



@app.route("/databases/<databaseName>/", methods=['PUT','POST'])
def addData(databaseName):
	key = request.args.get('key')
	value = request.args.get('value')
	return json.dumps(setData(databaseName,key,value))



@app.route("/databases/<databaseName>", defaults={'key': None}, methods=['DELETE'])
@app.route("/databases/<databaseName>/<key>", methods=['DELETE'])
def removeData(databaseName,key):
	if (key != None):
		return json.dumps(deleteData(databaseName,key))
	else:
		deleteAllData(databaseName)
		return json.dumps(deleteDBIndex(databaseName))



if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
