# RestApi-Flask-MongoDB-Docker

# About
This is an Assignment for CoRider.

I've used Python and Flask to create Rest APIs which connect to MongoDB Database. The Entire App is then Containerised using Docker.

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

## 1. GET Mapping "localhost:5001/users"
```
```
## 2. GET "localhost:5001/users/{userId}"
```
```
