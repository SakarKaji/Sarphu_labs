from fastapi import FastAPI
from .database import Base, engine
from .auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Take Home Assignment",
    description="A simple JWT based auth server that lets user to register, login and fetch user profile.",
    version="1.0.0"
)

app.include_router(auth_router.router)