# Password_Hashing

import bcrypt
from dotenv import load_dotenv
from jose import jwt
from datetime import datetime ,timedelta,timezone
import os 
load_dotenv()

def hash_password(password):
    password_bytes=password.encode()
    hashed=bcrypt.hashpw(password_bytes,bcrypt.gensalt())
    return  hashed.decode()
    # decode it before storing inside the database 

#! small mistake
'''
hashed is bytes, but your DB column will likely be String. Store it 
as hashed.decode('utf-8')

'''
def verify_password(password,hashed_password):
    '''
    # We are doing this encoding step because the password in db is  in string format
    # and this .checdkpw needed enoded password
    #bcrypt library, both arguments to bcrypt.checkpw() need to be bytes, not Python str.
    '''
    encoded_hash=hashed_password.encode()
    return bcrypt.checkpw(password.encode(),encoded_hash)
    # Note: bcrypt.checkpw returns  Boolean (True/False)

secret_key=os.environ.get("SECRET_KEY")
def create_jwt_token(payload):

    token=jwt.encode(payload,secret_key,algorithm='HS256')

    return token

#TODO: Dependency to protect routes:





























#TODO: Explore the JWE part ,JSON Web Encryption
'''
JWT
 │
 ├── JWS → signing → integrity/authenticity
 │
 └── JWE → encryption → confidentiality

'''



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