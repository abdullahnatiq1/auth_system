from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from db import getSession
import bcrypt                    # bcrypt is only used for one way hased it can't be reversed
                                 # to decrypt and encrypt both use import fernet it's two way encryption
from utils import createToken
from model import User


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup")
def signup(username : str, email : str, password : str, session : Session = Depends(getSession)):       # yahan humne function banay hai jisme humne types batai hain or hum session ko depend karwa raha hain (getSession)

    existingUser = session.exec(select(User).where (User.email == email)).first()     # humne aik variable banay hai or uska baad session ko execute karwa raha k jahan User hai wahan email == email
    if existingUser:
        return {"message" : "User already exists with this email . Please Login"}      

        
    hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')    # gensalt random string generate kr raha hai to make the password secure

    newUser = User(username = username, email = email, password = hashedPassword)
    session.add(newUser)
    session.commit()
    session.refresh(newUser)

    return{"message" : "User created successfully"}

@router.post("/signin")
def signin(email: str, password: str, Session = Depends(getSession)):
    user = Session.exec(select(User).where(User.email == email)).first()

    if not user:
       return{"message" : "Email not found"}
    stored_hash = user.password.encode('utf-8')
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        token =createToken({"id" : user.id, "email" : user.email})
        return{
            "message" : "Login successful",
            "token" : token,
            "user" : {
                "id" : user.id,
                "username" : user.username,
                "email" : user.email
            }
        }

    else:
        return{"message" : "Invalid Credentials"}
        
        









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
        