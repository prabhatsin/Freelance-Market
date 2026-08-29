# This script is used to implement , auth-check function
# i.e ,All APIs except signup/login require authentication.  this part 
#! There are tywo concepts here in fastapi middleware (@app.middleware and Depends())

'''
for our use case 
Conclusion: Use FastAPI Dependencies (Depends()), not @app.middleware("http")

#? Refrer doc: Depends Vs Middleware

'''

#! Step1: Understand what header is , what is it used for , 

'''

What is an HTTP header, really?

# When your browser/Postman/any client sends a request to a server, that request isn't just 
"the URL." It's actually structured like a letter with two parts:

1.Metadata about the request — sent as a set of key-value pairs, called headers
2.The actual content/payload — called the body (this is where your JSON, like {"email": "...", "password": "..."}, goes)


'''

# Example :
# A raw HTTP request literally looks something like this on the wire (simplified): 
'''

POST /api/projects HTTP/1.1
Host: myapi.com
Content-Type: application/json
Authorization: Bearer eyJhbGc...
User-Agent: PostmanRuntime/7.32

{"title": "Build a website", "description": "..."}



Everything above the blank line is headers — metadata describing the request (what format the body 
is in, who's making the request, what client software is being used, etc.). Everything below is 
the body — the actual data payload.

'''

'''

Notice: your JWT token is not meant to go in the request body alongside your actual data (like project title/description)
 — it goes in a header, because it's metadata about who's making the request, not part of the actual 
 content you're asking the server to process. This is a very deliberate, universal convention across 
 virtually all APIs — auth tokens live in headers, specifically the Authorization header, by 
 long-standing web convention.


'''

from jose import jwt
from fastapi import Header

SECRET_KEY = "your-secret-key-here"   # same one you used when creating the token at login
ALGORITHM = "HS256"                    # same one you used when creating the token at login


def get_current_user(authorization: str = Header()):
    token = authorization.replace("Bearer ", "")
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload