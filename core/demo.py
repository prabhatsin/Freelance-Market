# from jose import jwt
# from fastapi import Header

# SECRET_KEY = "your-secret-key-here"   # same one you used when creating the token at login
# ALGORITHM = "HS256"                    # same one you used when creating the token at login


# def get_current_user(authorization: str = Header()):
#     token = authorization.replace("Bearer ", "")
#     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     return payload



from fastapi import FastAPI, Header, Depends
from jose import jwt

app = FastAPI()

SECRET_KEY = "your-secret-key-here"   # same one you used when creating the token at login
ALGORITHM = "HS256"                    # same one you used when creating the token at login


def get_current_user(authorization: str = Header()):
    token = authorization.replace("Bearer ", "")
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload


@app.get("/test-auth")
def test_auth(current_user: dict = Depends(get_current_user)):
    return {"you_are": current_user}

