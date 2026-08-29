# Password_Hashing

#TODO: Explore the JWE part ,JSON Web Encryption
'''
JWT
 │
 ├── JWS → signing → integrity/authenticity
 │
 └── JWE → encryption → confidentiality

'''




import bcrypt
from dotenv import load_dotenv
load_dotenv()

def hash_password(password):
    password_bytes=password.encode()
    hashed=bcrypt.hashpw(password_bytes,bcrypt.gensalt())
    return  hashed
    # decode it before storing inside the database 


#! small mistake
'''
hashed is bytes, but your DB column will likely be String. Store it 
as hashed.decode('utf-8')

'''
def verify_password(password,hashed_password):
    # This is binary password
    # !hashed_password=hash_password(password) 
    encoded_hash=hash_password.encode()
    if bcrypt.checkpw(password.encode(),hashed_password):
        # print("It matched")
        return {"message":"Its matched"}
    else:
        return{"message":"Password did not match"}


# This hashed passowrd in above function is directly c alled from the db\
# dont call the hashing function internally , 
## --------------------------------------------------------------------------------------------##

#TODO: Dependency to protect routes:

from jose import jwt
'''
token=jwt.encode(
    PAYLOAD / CLAIMS,
    SECRET KEY,
    SIGNING ALGORITHM
)


means:

Take these claims/payload → sign them using this secret → using this algorithm → give me a JWT.
'''

# PAYlOAD /claims
# The main info u are putting inside the JWT 

# for example 

payload={
    "user_id":12,
    "role": "client",
    "exp": 1788000000
}
from datetime import datetime ,timedelta,timezone

Payload={
    "user_id":12,
    "role": "client",
    "exp": datetime.now(timezone.utc)+timedelta(minutes=60)
}

SECRET_KEY="my_super_secret_key"
# In production  we get this using random generators like 

algorithm="HS256"  #HMAC + SHA-256

#Header : Header — metadata about the token

# eg:{ "alg": "HS256", "typ": "JWT" }

'''
Signature — this is the actual security. The server computes:

signature = HMAC-SHA256(base64(header) + "." + base64(payload), SECRET_KEY)

'''

token=jwt.encode(
    payload,
    SECRET_KEY,
    algorithm='HS256'
)
# print(token)
# print(type(token))
import os 
secret_key=os.environ.get(SECRET_KEY)

def create_jwt_token(payload):

    token=jwt.encode(payload,secret_key,algorithm='HS256')

    return token





Payload={
    "user_id":12,
    "role": "client",
    "exp": datetime.now(timezone.utc)+timedelta(minutes=60)
}
SECRET_KEY="my_super_secret_key"


# print(create_jwt_token(Payload,SECRET_KEY))








#! Decoding experiment 

# import base64

# header = b"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"

# decoded_header = base64.urlsafe_b64decode(header)

# print(decoded_header.decode())







# import base64

# PAYLOADS = b"eyJ1c2VyX2lkIjoxMiwicm9sZSI6ImNsaWVudCIsImV4cCI6MTc4ODAwMDAwMH0"

# padding = b"=" * (-len(PAYLOADS) % 4)

# decoded = base64.urlsafe_b64decode(PAYLOADS + padding)

# print(decoded.decode())