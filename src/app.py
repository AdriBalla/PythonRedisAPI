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
# Return the result success
#
def success():
	return json.dumps("true");

#
# Routes
#
@app.route('/status')
def check_status():
	returnValue = {"status":"true"}
	return json.dumps(returnValue)


@app.route("/databases/", methods=['GET'])
def readAllDatabases():
	return json.dumps(getAllDatabases())


@app.route("/databases/<databaseName>/data", defaults={'key': None}, methods=['GET'])
@app.route("/databases/<databaseName>/data/<key>", methods=['GET'])
def readData(databaseName,key):
	if (key == None):
		if request.args.get('keys'):
			returnValue = {}
			for key in json.loads(request.args.get('keys')):
				returnValue[key] = getData(databaseName,key)
			return json.dumps(returnValue)
		else:
			return json.dumps(getAllData(databaseName))
	else:
		return json.dumps({key:getData(databaseName,key)})


@app.route("/databases/<databaseName>/data", methods=['PUT','POST'])
def addData(databaseName):
	if request.args.get('key') and request.args.get('value'):
		setData(databaseName,request.args.get('key'),request.args.get('value'))
	elif request.args.get('data'):
		data = json.loads(request.args.get('data'))
		for key in data:
			setData(databaseName,key,data[key])
	return success()

@app.route("/databases/<databaseName>/data/<key>", methods=['DELETE'])
def removeData(databaseName,key):
	deleteData(databaseName,key)
	return success()

@app.route("/databases/<databaseName>", methods=['DELETE'])
def removeDB(databaseName):
	deleteAllData(databaseName)
	deleteDBIndex(databaseName)
	return success()





if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
