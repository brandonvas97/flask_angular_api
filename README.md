# FULL STACK CODE TEST
This project needs docker to be executed, you can download it from: https://www.docker.com/

# BUILD DOCKER IMAGE
Once you have installed docker in your PC open the terminal in this root of the project and use this command:

docker-compose build --no-cache

# RUN CONTAINERS
Now use this command to start the containers and the project:

docker-compose up

When you see this message in the terminal: 

frontend  | ✔ Compiled successfully.

You'll know the project is running succesfully

# Swagger
You can access to the swagger documentation in this link:

http://localhost:5000/apidocs/

# Pytest
You can execute all the integration tests with pytest using the command in other terminal:

docker exec -it backend pytest /app/test_api.py

# Postman collection 
With the postman collection named: Book-api.postman_collection.json, you can use the endpoints and it includes regression tests for all the endpoints