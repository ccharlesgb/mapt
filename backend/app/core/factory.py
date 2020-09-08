from fastapi import FastAPI
from app.api import router
from fastapi.middleware.cors import CORSMiddleware

origins = ["http://localhost:3000"]

def create_app():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)
    return app
