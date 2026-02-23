import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file. Check your configuration")

def getDbConnection():
    """
    Creates and returns a new connection object
    """
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory = RealDictCursor)
        return conn
    
    except Exception as e:
        print(f"Error connection to the database : {e}")
        raise
