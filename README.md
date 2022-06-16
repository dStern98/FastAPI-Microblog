This is a MicroBlog App built using FastAPI, MongoDB, and Motor (an Async MongoDB driver for Python).
Security is implemented using JWT Tokens (python-jose), and password hashing using bcrypt (passlib).
Users must create an account, then login to get a token. The token can be used to create/edit/delete posts,
as well as liking/disliking posts.
The voting logic is such that if a user "likes" a page a second time, that corresponds to unliking the page,
and the same for disliking.
Tests are in the tests/ folder and use pytest.
To use, see the Settings class in the file ./app/models, which details the environmental variables that must be set for use.
