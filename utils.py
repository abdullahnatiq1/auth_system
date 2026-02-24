from jose import jwt             # used to create and verify tokens
from datetime import datetime, timedelta     # datetime  -> to get current time, timedelta -> to add time(like 24 hours form now)
secretKey = "your-secret-key"
algorithm = "HS256"              # HS256 is an algorithm used to generate random tokens


def createToken(data : dict):    # yahan hum aik function bana raha hai or data k aik variable bhhi create kiya hai 
    # or hume data ko dictionary is liya rakha hai q k jwt.encode only takes dict as input
    expire = datetime.utcnow() + timedelta(hours = 24)    # utcnow humain current date and time deta hai
    # and timedelta (hours = 24) ye utctime main 24 hours add krta hai so it expires after 24
    data.update({"exp" : expire})  # data main already id and email hai so .update usme exp bhi add kr raha hai
    token = jwt.encode(data, secretKey, algorithm = algorithm)
    return token