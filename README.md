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

If running the app using Docker in development mode, use the command `docker compose -f docker-compose.dev.yml -d`.
If in production, use the command `docker compose -f docker-compose.prod.yml -d`. Note that the docker-compose files expect
a `.env` file to be present in the root. The dev build uses a bind mount to allow for the container to immediately update with new
code. No environment variables are expressly written in the docker-compose files. Instead, the `.env` file is mounted into the container,
and Pydantic automatically creates the environment variables.
