from fastapi import FastAPI
from routes import router as user_router

from model import User

app = FastAPI()

app.include_router(user_router)

@app.post("/hello_world")
def func(user : User):
    return user