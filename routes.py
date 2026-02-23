from fastapi import APIRouter
from db import getDbConnection   #  yeh humne password ki encryption krna k liya library install ki hai
from psycopg2.extras import RealDictCursor
import bcrypt

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup")
def signup(id : int, username : str, email : str, password : str):
    conn = getDbConnection()
    cursor = conn.cursor()

    try:
        hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        checkQuery = "select * from users where email = %s"
        cursor.execute(checkQuery,(email,))
        existingUser = cursor.fetchone()

        if existingUser:
            return{"message" : "User already exists with this email. Please Login"}

        insertQuery = "insert into users (id, username, email, password) values (%s, %s, %s, %s)" 
        cursor.execute(insertQuery,(id, username, email, hashedPassword))
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
        query = "SELECT password FROM users WHERE email = %s"
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
            return {"login": user}
        else:
            return {"message": "Invalid credentials"}

    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()
        