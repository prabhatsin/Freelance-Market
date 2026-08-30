
from fastapi import FastAPI, Header, Depends
from fastapi import HTTPException, status
from jose import jwt,JWTError

app = FastAPI()

SECRET_KEY = "your-secret-key-here"   # same one you used when creating the token at login
ALGORITHM = "HS256"                    # same one you used when creating the token at login


def get_current_user(authorization: str = Header()):
    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return payload

def get_current_client(current_user:dict=Depends(get_current_user)):
    if current_user["role"]!='client':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only clients can perform this action")
    return current_user


def get_current_freelancer(current_user:dict=Depends(get_current_user)):
    if current_user["role"]!='freelancer':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only freelancer can perform this action")
    return current_user



@app.get("/test-auth")
def test_auth(current_user: dict = Depends(get_current_freelancer)):
    return {"you_are": current_user}



#! Explain this "authorization: str = Header()"
# Here "=Header()" is just an instance of fastapis internal headers class which is basically a flag
# saying fastapi that pull this (authorization) value from the headers section of the incoming request

#! Note: usually the argument name is just a naming convention , nothing literal , but here in this particular case 
# dont name this anything else because the headers json has few values like "Authorization","User-Agent" ,.....
# so it literally looks up the value for the name u mentioned in the argument of the function 



#! Get Clarity
'''
= Header() is just a default value, in plain Python terms

Strip away the FastAPI-specific meaning for a second, and look at the function signature purely as 
Python:

python
def get_current_user(authorization: str = Header()):

Structurally, this is no different from:

python
def some_function(x: int = 5):

Header() is simply an object — when Python evaluates this function definition, it calls Header() once, 
gets back some object (an instance of FastAPI's internal Header class), and sets that as the default 
value for the authorization parameter, exactly like 5 would be the default for x in the simpler example.

'''



#? FLOW : 
'''

Real HTTP request arrives, containing header: Authorization: Bearer eyJ...
        ↓
FastAPI needs to call your get_current_user function to handle this request
        ↓
Before calling it, FastAPI checks: "what does this function need?"
   (this was pre-computed at startup via signature inspection)
        ↓
It sees: parameter "authorization", marked as Header()
        ↓
FastAPI goes to the incoming request's actual headers dictionary,
looks up the key "Authorization" (converted from your param name),
finds the value "Bearer eyJ..."
        ↓
FastAPI NOW calls your function, passing that extracted string in:
   get_current_user(authorization="Bearer eyJ...")
        ↓
Your function runs completely normally from here — same as your manual test

'''