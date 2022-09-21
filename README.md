# Summary

This is a MicroBlog App built using FastAPI, MongoDB, and Motor (an Async MongoDB driver for Python).
Security is implemented using JWT Tokens (python-jose), and password hashing using bcrypt (passlib).
Users must create an account, then login to get a token. The token can be used to create/edit/delete posts,
as well as liking/disliking posts.
The voting logic is such that if a user "likes" a page a second time, that corresponds to unliking the page,
and the same for disliking.
Tests are in the `tests/` folder and use pytest.
To use, see the Settings class in the file `./app/models`, which details the environmental variables that must be set for use.

## Docker

If running the app using Docker in development mode, use the command `docker compose -f docker-compose.dev.yml up -d`.
If in production, use the command `docker compose -f docker-compose.prod.yml up -d`. Note that the docker-compose files expect
a `.env` file to be present in the root. The dev build uses a bind mount to allow for the container to immediately update with new
code. No environment variables are expressly written in the docker-compose files. Instead, the `.env` file is mounted into the container,
and Pydantic automatically creates the environment variables. Use the commands `docker compose -f docker-compose.dev.yml down` or
`docker compose -f docker-compose.prod.yml down` to spin down the containers.

## Valid .env

For reference, a valid .env is shown below. This would be valid for running in a Docker container, but not valid
if using Mongo Atlas.

```
mongodb_host = "mongo_db"
mongodb_user = "david"
mongodb_password = "somepassword"
mongodb_database = "somedatabase"
mongodb_driver = "mongodb"
mongodb_port = 27017
mongodb_params = '{"serverSelectionTimeoutMS": "2000"}'
mongodb_useAtlas = False
uvicorn_host = "0.0.0.0"
uvicorn_port = 8001
uvicorn_reload = False
auth_secret_key = "some_secret_key"
auth_algorithm = "HS256"
auth_token_expiration_minutes = 15
```
