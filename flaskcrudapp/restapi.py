from flask import Flask, request, json, Response
from pymongo import MongoClient
import logging as log
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

database_data = {
    "database": "Users",
    "collection": "user",
}

class MongoAPI:
    def __init__(self, data):
        # self.client = MongoClient("mongodb://localhost:27017/")  
        self.client = MongoClient("mongodb://mymongo_1:27017/")
        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data

    def getAllUsers(self):
        response = dumps(self.collection.find())
        return Response(response=response,
                        status=200,
                        mimetype='application/json')

    def getOneUser(self, id):
        if ObjectId.is_valid(id):
            userdata = self.collection.find_one({'_id': ObjectId(id)})
            response = dumps(userdata)
            return Response(response=response,
                            status=200,
                            mimetype='application/json')
        else:
            response = json.dumps({
                    'message': "Invalid ObjectId"
                })
            return Response(response=response,
                            status=404,
                            mimetype='application/json')

    def createNewUser(self, name,email,password):
        # log.info('Writing Data')
        hashedpassword = generate_password_hash(password)
        result = self.collection.insert_one({
                        'name': name,
                        'email': email,
                        'password': hashedpassword
                    })
        response = json.dumps({
                        "message" : "User Added Successfully",
                        "id": str(result.inserted_id)
                    })
        return Response(response=response,
                        status=200,
                        mimetype='application/json')

    def updateUser(self,id,name,email,password):
        # log.info('Updating Data')
        if ObjectId.is_valid(id):
            hashedpassword = generate_password_hash(password)
            response = self.collection.update_one(
                        {'_id': ObjectId(id['$oid']) if '$oid' in id else ObjectId(id)},
                        {'$set':
                            {'name': name,
                            'email': email,
                            'password': hashedpassword
                            }
                        }
                    )
            if response.modified_count > 0:
                return Response(response=json.dumps({'message': 'User Updated'}),
                                status=200,
                                mimetype='application/json')
            else:
                return Response(response=json.dumps({'message': 'No User Updated'}),
                                status=200,
                                mimetype='application/json')
        else:
            response = json.dumps({
                             'message': "Invalid ObjectId"
                            })
            return Response(response=response,
                    status=404,
                    mimetype='application/json')
        
    def deleteOneUser(self, id):
        # log.info('Deleting Data Of User: '+id)
        if ObjectId.is_valid(id):
            response = self.collection.delete_one({'_id':ObjectId(id)})
            if response.deleted_count > 0:
                output = json.dumps({'message': 'Successfully Deleted'})
                return Response(response=output,
                                status=200,
                                mimetype='application/json')
            else:
                output = json.dumps({'message': 'No Such User Found'})
                return Response(response=output,
                                status=404,
                                mimetype='application/json')
        else:
            response = json.dumps({
                             'message': "Invalid ObjectId"
                            })
            return Response(response=response,
                    status=404,
                    mimetype='application/json')

    def checkPassword(self,id, entered_pwd):
        if ObjectId.is_valid(id):
            try:
                userdata = self.collection.find_one({'_id': ObjectId(id)})
                hashed_pwd = userdata['password']
                val = check_password_hash(hashed_pwd,entered_pwd)
                if val:
                    return Response(response= json.dumps({'message':'Correct Password'}),
                            status=200,
                            mimetype='application/json')
                else:
                    return Response(response= json.dumps({'message':'Incorrect Password'}),
                            status=200,
                            mimetype='application/json')
            except:
                return Response(response=json.dumps({'message':'Incorrect Input Entered'}),
                                status=200,
                                mimetype='application/json')
        else:
            response = json.dumps({
                             'message': "Invalid ObjectId"
                            })
            return Response(response=response,
                    status=404,
                    mimetype='application/json')

app = Flask(__name__)

@app.route('/')
def base():
    return Response(response=json.dumps({
                            "Status": "UP",
                            "Message": "This Is HomePage of RestAPI Application.",
                            "Routes": {
                                "POST-new_user": "/users",
                                "GET-all_users": "/users",
                                "GET-unique_user": "/users/<id>",
                                "PUT-unique_user": "/users/<id>",
                                "DELETE-unique_user": "/users/<id>"
                                }
                            }),
                    status=200,
                    mimetype='application/json')

@app.route('/users', methods=['GET'])
def mongo_read():
    return MongoAPI(database_data).getAllUsers()

@app.route("/users/<id>", methods=['GET'])
def getUserWithId(id):
    return MongoAPI(database_data).getOneUser(id)

@app.route("/users/<id>", methods=['DELETE'])
def deleteUserWithId(id):
    return MongoAPI(database_data).deleteOneUser(id)

@app.route("/users", methods=['POST'])
def createNewUser():
    inputjson = request.json
    name = inputjson['name']
    email = inputjson['email']
    password = inputjson['password']

    if request.method=='POST' and name and email and password:
        return MongoAPI(database_data).createNewUser(name,email,password)
    else:
        response = json.dumps({
            "message": "Data Not Found At /users",
            "id": None
        })
        return Response(response=response,
                        status=404,
                        mimetype='application/json')

@app.route("/users/<id>", methods=['PUT'])
def updateUserId(id):
    inputjson = request.json
    name = inputjson['name']
    email = inputjson['email']
    password = inputjson['password']

    if id and name and email and password and request.method=='PUT':
        return MongoAPI(database_data).updateUser(id,name,email,password)
    else:
        response = json.dumps({"message": "Data Not Found"})
        return Response(response=response,
                        status=404,
                        mimetype='application/json')

@app.route("/checkpassword/<id>", methods=['GET'])
def checkPassword(id):
    inputjson = request.json
    entered_pwd = inputjson['password']

    if entered_pwd:
        return MongoAPI(database_data).checkPassword(id,entered_pwd)
    else:
        response = json.dumps({"message": "No Password Entered"})
        return Response(response=response,
                        status=404,
                        mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')

    