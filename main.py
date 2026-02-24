from fastapi import FastAPI
from routes import router as user_router
from db import createDBandTables

app = FastAPI()

@app.on_event("startup")
def onStartup():
    createDBandTables()


app.include_router(user_router)

