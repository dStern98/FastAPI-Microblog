from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import connectDB, users, posts, login, votes
import uvicorn
from .models import Settings
"""
Uvicorn is run programatically using an app factory
"""
settings = Settings()


def create_app() -> FastAPI:

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    tuple(
        app.include_router(router) for router in
        (connectDB.router, users.router, posts.router, votes.router, login.router)
    )

    return app


"""
When using a Uvicorn App Factory, pass in the factory=True flag.
"""


def invoke_app():
    return uvicorn.run(f"{__name__}:create_app", factory=True, **settings.get_uvicorn_settings())


if __name__ == "__main__":
    invoke_app()
