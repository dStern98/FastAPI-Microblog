This is a MicroBlog App built using FastAPI, MongoDB, and Motor (an Async MongoDB driver for Python).
Security is implemented using JWT Tokens (python-jose), and password hashing using bcrypt. 
Users must create an account, then login to get a token. The token can be used to create/edit/delete posts, 
as well as liking/disliking posts. 

To use, see the Settings class in the file ./app/models, which details the environmental variables that must be set for use.
