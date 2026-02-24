import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file. Check your configuration")

engine = create_engine(DATABASE_URL, echo  = True)

def createDBandTables():         # creatDBandTables k aik func hai o
    """
    Initializes the databse schema based on your SQLModel classes.     
    """
    SQLModel.metadata.create_all(engine)     # """ Doc Strings """ 

def getSession():
    """
    Provides a databse session to your toutes and ensures it closes after use
    """
    with Session(engine) as session:
        yield session

