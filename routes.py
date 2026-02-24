from fastapi import APIRouter
from db import getDbConnection   #  yeh humne password ki encryption krna k liya library install ki hai
from psycopg2.extras import RealDictCursor
import bcrypt                    # bcrypt is only used for one way hased it can't be reversed
                                 # to decrypt and encrypt both use import fernet it's two way encryption
from jose import jwt             # used to create and verify tokens
from datetime import datetime, timedelta     # datetime  -> to get current time, timedelta -> to add time(like 24 hours form now)
import uuid


secretKey = "your-secret-key"
algorithm = "HS256"              # HS256 is an algorithm used to generate random tokens

def createToken(data : dict):    # yahan hum aik function bana raha hai or data k aik variable bhhi create kiya hai 
    # or hume data ko dictionary is liya rakha hai q k jwt.encode only takes dict as input
    expire = datetime.utcnow() + timedelta(hours = 24)    # utcnow humain current date and time deta hai
    # and timedelta (hours = 24) ye utctime main 24 hours add krta hai so it expires after 24
    data.update({"exp" : expire})  # data main already id and email hai so .update usme exp bhi add kr raha hai
    token = jwt.encode(data, secretKey, algorithm = algorithm)
    return token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup")
def signup(username : str, email : str, password : str):
    conn = getDbConnection()
    cursor = conn.cursor()

    try:
        userid = str(uuid.uuid4())
        
        hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        checkQuery = "select * from users where email = %s"
        cursor.execute(checkQuery,(email,))
        existingUser = cursor.fetchone()

        if existingUser:
            return{"message" : "User already exists with this email. Please Login"}

        insertQuery = "insert into users (uuid, username, email, password) values (%s, %s, %s, %s)" 
        cursor.execute(insertQuery,(userid, username, email, hashedPassword))
        conn.commit()
        return {"message" : "User created successfully" }

    except Exception as e:
        return {"error", e}
    
    finally:
        cursor.close()
        conn.close()
    
@router.post("/signin")
def signin(email: str, password: str):
    conn = getDbConnection()
    # Use RealDictCursor to allow accessing columns by name like user['password']
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        # 1. Fetch user by email
        query = query = "SELECT id, username, email, password FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if not user:
            return {"message": "Email not found"}

        # 2. Get the hash from DB (Postgres returns it as a string)
        stored_hash = user['password']
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode('utf-8')

        # 3. Verify the password
        user_password_bytes = password.encode('utf-8')

        if bcrypt.checkpw(user_password_bytes, stored_hash):
            token = createToken({"id" : user["id"], "email" : user["email"]})
            return {
                "message" : "Login successful",
                "token" : token,
                "user" : {
                    "id" : user["id"],
                    "username" : user["username"],
                    "email" : user["email"]
                }


            }
        else:
            return {"message": "Invalid credentials"}

    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()
        