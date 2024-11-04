# RestApi-Flask-MongoDB-Docker

# About
This is an Assignment for CoRider, Made By Madhur Aggarwal.

I've used Python and Flask to create Rest APIs which connect to MongoDB Database. The Entire App is then Containerized using Docker.
The App stores username, email and passwords of each user alongwith a unique userID.

In this Flask app, bson.objectid is used for providing a unique ObjectID.
The Library werkzeug is used for hashing the passwords
The Library pymongo is used for connecting the python app to MongoDB database

# To Run
Ensure you have Docker (and pip) Installed. Make Sure That MongoDB is available and running on default MongoDB port (localhost:27017). 
Clone The Repository from GitHub.

Go Inside The "flaskcrudapp/restapi.py" file. In this file, on the top the lines (8-11) of python code: 
```
database_data = {
    "database": "Users",
    "collection": "user",
}
```
Specify the database and the collection inside that database the app will connect to. Create a new Database & Collection (or use some already existing one) in MongoDB for this app as per your choice. Update the name of the database & collection in this file.

 Finally, Navigate The Command Prompt Inside the "flaskcrudapp" Folder, and then Run the Command: 
```
docker-compose up
```
The dependencies specified in "requirements.txt" will automatically install. After the dependencies are installed, the app would connect to mongoDB from port 27017 and would start running on port 5001.

<img width="899" alt="image" src="https://github.com/MadhurAggarwal/RestApi-Flask-MongoDB-Docker/assets/113705764/1fc02a77-13ee-4bff-a7e4-280bda7dcf4e">


# Ports configurations
To change the port on which mongoDB is running, make changes to the "flaskcrudapp/docker-compose.yml" file:
```
    mymongo_1:
        image: "mongo"
        ports:
            - "27017:27017"
```
and also, add the corresponding change to the connection string in the "flaskcrudapp/restapi.py" file, in the class MongoAPI at line 16:
```
self.client = MongoClient("mongodb://mymongo_1:27017/")
```

Similarly, to change the port on which the app runs from 5001, edit the configuration in the "flaskcrudapp/docker-compose.yml" file:
```
    myreader:
        build: .
        depends_on: 
            - mymongo_1
        ports:
            - "5001:5001"
```
and also, add the corresponding code to the 'EXPOSE' command in the "flaskcrudapp/Dockerfile" file
```
# Exposing an internal port
EXPOSE 5001
```

This way, the ports can be changed as per requirements.

# Rest Api Mapping:
The following APIs are mapped to "localhost:5001/" port:

## 0. (default) "localhost:5001/"
```
This is a default port, to check if the app is running or not.
On successfully running the app, the port gets a default output.
with status = 'up' and a message explaing different routes available.

The default output is:
{
    "Status": "UP",
    "Message": "This Is HomePage of RestAPI Application.",
    "Routes": {
        "POST-new_user": "/users",
        "GET-all_users": "/users",
        "GET-unique_user": "/users/<id>",
        "PUT-unique_user": "/users/<id>",
        "DELETE-unique_user": "/users/<id>"
    }
}
```
## 1. GET "localhost:5001/users"
```
This API endpoint returns a list of all the users stored in the database.
If There is no user data stored in DB, it returns an empty list []
Otherwise, it returns the users with 'id', 'username', 'email', and 'password' fields.
(The passwords are hashed for security, and can even be excluded from output if required)

Here's a Sample output for this:
[
    {
        "_id": {
            "$oid": "64e8e937d28f01e6bdde1657"
        },
        "name": "Madhur Aggarwal",
        "email": "madhuraggarwal@gmail.com",
        "password": "pbkdf2:sha256:600000$dGKX6B3DGOcMooKV$585123bbe75b2adb1fbc7f762097cce22d88422c8103855c6836524c28dcc013"
    },
    {
        "_id": {
            "$oid": "64e8e984d28f01e6bdde1659"
        },
        "name": "Harry Potter",
        "email": "harrypotter@gmail.com",
        ....
    }
....
]

```
Here's a screenshot for this output:

<img width="600" alt="image" src="https://github.com/MadhurAggarwal/RestApi-Flask-MongoDB-Docker/assets/113705764/8e45e0af-7fa0-494e-9d2f-fcf43c8a1bf0">

## 2. GET "localhost:5001/users/<Id>"
```
This API endpoint first checks if the ID id valid, and finds the user with specified ID, if any.
Then, it returns the user with the specified userID.

The Sample output for this Endpoint is:
Endpoint:
    "localhost:5001/users/64e8e937d28f01e6bdde1657"
Output:
{
    "_id": {
        "$oid": "64e8e937d28f01e6bdde1657"
    },
    "name": "Madhur Aggarwal",
    "email": "madhuraggarwal@gmail.com",
    "password": "pbkdf2:sha256:600000$dGKX6B3DGOcMooKV$585123bbe75b2adb1fbc7f762097cce22d88422c8103855c6836524c28dcc013"
}
```

The Output on Postman:

<img width="602" alt="image" src="https://github.com/MadhurAggarwal/RestApi-Flask-MongoDB-Docker/assets/113705764/08ecf92c-c1e8-41d3-b624-8ec91d1ef09b">

## 3. POST "localhost:5001/users"
```
This API endpoint adds a new user to the database.
The name, email and password of the user are passed as raw (json) format in the request
The App generates a unique ObjectID and assigns it to the new user & stores in the DB.

The Output for this API Endpoint is of the form:
Sample message body:
{
    "name": "Harry Potter",
    "email": "harrypotter@gmail.com",
    "password": "platform934"
}

Sample Output:
{
    "id": "64e8e984d28f01e6bdde1659",
    "message": "User Added Successfully"
}
The User Has Now been Added to the database.
```
Using Postman, the output looks like this:

<img width="602" alt="image" src="https://github.com/MadhurAggarwal/RestApi-Flask-MongoDB-Docker/assets/113705764/96806dad-8461-4b61-a313-01f6bfbb8b2e">


<img width="617" alt="image" src="https://github.com/MadhurAggarwal/RestApi-Flask-MongoDB-Docker/assets/113705764/eebd49df-c13c-43ca-8e1b-08f3c8e632a0">

## 4. PUT "localhost:5001/users/<Id>"
```
This API Endpoint updates the specified userID to the new values of name, email, password
which are passed as raw json format in the request body.

The ouput is the updated user & response, for example:
Endpoint:
    localhost:5001/users/64e8e937d28f01e6bdde1657
Input Body:
{
    "name": "Random Person",
    "email": "randomperson@gmail.com",
    "password": "RandomPassword"
}
Output:
{
    "message": "User Updated"
}
```

Postman Output for this API Endpoint:

<img width="608" alt="image" src="https://github.com/MadhurAggarwal/RestApi-Flask-MongoDB-Docker/assets/113705764/76232c73-8935-40a3-9d44-2c68013fc927">

## 5. DELETE "localhost:5001/users/<Id>"
```
This API Endpoint takes in a userID, validates it and then deletes the user with specified ID
from the DB. For example:
Endpoint:
    localhost:5001/users/64e8e984d28f01e6bdde1659
Output:
{
    "message": "Successfully Deleted"
}

If we try to delete it again, it would return:
{
    "message": "No Such User Found"
}

Incase the userId is invalid, we get the error:
Endpoint: localhost:5001/users/1234
Error:
{
    "message": "Invalid ObjectId"
}
```

Ouput on Postman:

<img width="606" alt="image" src="https://github.com/MadhurAggarwal/RestApi-Flask-MongoDB-Docker/assets/113705764/39d1f1a8-2b0e-4b47-b74b-f4d1a1fa1810">


<img width="603" alt="image" src="https://github.com/MadhurAggarwal/RestApi-Flask-MongoDB-Docker/assets/113705764/03bab0db-8336-4f36-b63e-21a48053bc0e">


There is an additional API endpoint I've created, for validating the password (to ensure that hash functions are working appropriately):
## 6. GET "localhost:5001/checkpassword/<Id>"
```
This API endpoint takes in the userID as path and password specified in raw json in the request body.
Then, it attempts to validate the password from the hashed value stored in the DB at the specified ID.
For Example:

Endpoint:
    localhost:5001/checkpassword/64e8e984d28f01e6bdde1659

Message Body:
{
    "password": "platform934"
}
Output:
{
    "message": "Correct Password"
}

Trying this with an incorrect password, we get
{
    "password": "somewrongpassword"
}
{
    "message": "Incorrect Password"
}
```

Postman Output for this API Endpoint:

<img width="599" alt="image" src="https://github.com/MadhurAggarwal/RestApi-Flask-MongoDB-Docker/assets/113705764/27e4b53c-08c4-4deb-9680-10d8e4ca59fd">


<img width="613" alt="image" src="https://github.com/MadhurAggarwal/RestApi-Flask-MongoDB-Docker/assets/113705764/a7d532e7-3e86-4e09-a40c-60b106f3afe5">

