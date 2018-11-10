from flask import Flask, render_template, request, redirect, url_for, send_file, Response,jsonify
import json, redis

app = Flask(__name__)

DB_POOL = redis.ConnectionPool(host='api_redis', port=6379, db=0)

###############
# Exception
###############

class Error(Exception):
	status_code = 400

	def __init__(self, message, status_code=None, payload=None):
		Exception.__init__(self)
 		self.message = message
		if status_code is not None:
			self.status_code = status_code
		self.payload = payload

	def to_dict(self):
		rv = dict(self.payload or ())
		rv['message'] = self.message
		return rv



#############
# Functions
#############


#
# Retreive the Redis Server acting as a registry for all databases name
#
def getRedisDbRegistryServer():
	return redis.Redis(connection_pool=DB_POOL)

#
# Retreive the Redis Server for a database according to its name
#
def getRedisServer(databaseName,readOnly=False):
	pool = redis.ConnectionPool(host='api_redis', port=6379, db=getDBIndex(databaseName,readOnly))
	return redis.Redis(connection_pool=pool)

#
# Get all entry to Redis Server according to the database Name
#
def getAllDatabases():
	redisServer = getRedisDbRegistryServer()
	return redisServer.keys()


#
# Add a batch of entry as dictionary to a Redis Server according to the database name
#
def setData(databaseName,dictionary):
	redisServer = getRedisServer(databaseName)
	for key in dictionary:
	   redisServer.set(key, dictionary[key])

#
# Get entries to a Redis Server according to the database name and array of keys
#
def getData(databaseName,keys):
	returnValue = {}
	redisServer = getRedisServer(databaseName,True)
	for key in keys:
		returnValue[key] = redisServer.get(key)
	return returnValue

#
# Get all entry to Redis Server according to the database Name
#
def getAllData(databaseName):
	redisServer = getRedisServer(databaseName,True)
	returnValue = getData(databaseName,redisServer.keys())
	return returnValue


#
# Delete a batch of entries to a Redis Server according to the database name and an array of keys
#
def deleteData(databaseName,keys):
	redisServer = getRedisServer(databaseName)
	for key in keys:
		redisServer.delete(key)


#
# Delete all entry to Redis Database according to database name
#
def deleteAllData(databaseName):
	redisServer = getRedisServer(databaseName)
	deleteData(redisServer.keys())




#
# Get the index of a database in the registry of databases
#
def getDBIndex(databaseName,readOnly=False):
	redisServer = getRedisDbRegistryServer()
	returnValue = redisServer.get(databaseName)
	if returnValue == None and not readOnly:
		returnValue = getNextDBIndex()
		redisServer.set(databaseName, returnValue)
	if returnValue == None:
		raise Error('Could not find server with this name', status_code=410)
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
	return jsonify({"message":"Success"});

#############
# Handlers
#############

@app.errorhandler(Error)
def handle_invalid_usage(error):
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

#############
# Routes
#############

@app.route('/status')
def check_status():
	returnValue = {"status":True}
	return jsonify(returnValue)


@app.route("/databases/", methods=['GET'])
def readAllDatabases():
	return jsonify(getAllDatabases())



@app.route("/databases/<databaseName>/data", defaults={'key': None}, methods=['GET'])
@app.route("/databases/<databaseName>/data/<key>", methods=['GET'])
def readData(databaseName,key):
	toRead = []
	if key != None:
		toRead.append(key)
	elif request.args.get('keys'):
		toRead = json.loads(request.args.get('keys'))

	if toRead :
		returnValue = getData(databaseName,toRead)
	else:
		returnValue = getAllData(databaseName)

	return jsonify(returnValue);




@app.route("/databases/<databaseName>/data", methods=['PUT','POST'])
def addData(databaseName):
	toAdd = {}
	if request.args.get('key') and request.args.get('value'):
		toAdd[request.args.get('key')] = request.args.get('value')
	elif request.args.get('data'):
		toAdd = json.loads(request.args.get('data'))

	if toAdd:
		setData(databaseName,toAdd)
	else:
		raise Error('Missing parameters', status_code=410)
	return success()



@app.route("/databases/<databaseName>/data", defaults={'key': None}, methods=['DELETE'])
@app.route("/databases/<databaseName>/data/<key>", methods=['DELETE'])
def removeData(databaseName,key):
	toDelete = []
	if key != None:
		toDelete.append(key)
	elif request.args.get('keys'):
		toDelete = json.loads(request.args.get('keys'))

	if toDelete:
		deleteData(databaseName,toDelete)
	else :
		raise Error('Missing parameters', status_code=410)
	return success()


@app.route("/databases/<databaseName>", methods=['DELETE'])
def removeDB(databaseName):
	deleteAllData(databaseName)
	deleteDBIndex(databaseName)
	return success()





if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
