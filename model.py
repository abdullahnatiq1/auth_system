from sqlmodel import SQLModel, Field
import uuid

class User(SQLModel, table = True):
    __tablename__ = "students"
    uuid : str = Field(default_factory = lambda : str(uuid.uuid4()), primary_key = True)
    username : str
    email : str = Field(unique = True)
    password : str






