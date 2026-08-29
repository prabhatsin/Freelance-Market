from fastapi import FastAPI
from fastapi import HTTPException

from schema.schema import UserLogin, UserSignup
from db.database import get_db
from fastapi import Depends
from models.models import User
from sqlalchemy.orm import Session

from core.security import verify_password,create_jwt_token,hash_password


app=FastAPI()

@app.post('/signup')
def Signup(user_data:UserSignup,db:Session =Depends(get_db)):
    # Creating the instance of User class defined in models.py

    new_user=User(
        username=user_data.username,
        password=hash_password(user_data.password)
    )
    existing_user=db.query(User).filter(User.username==user_data.username).first()
    if existing_user is None:
        db.add(new_user)
        db.commit() 
        return {"message: A New User Created Succesfully"}
    else:
        return {"message : User already exist"}


@app.post('/login')
def Login(user_data:UserLogin,db:Session =Depends(get_db)):
    existing_user=db.query(User).filter(User.username==user_data.username).first()
    if existing_user is  None:
        raise HTTPException (status_code=404,detail="User does not exist")
    else:
        # If verify_password retruns false ..
        if not verify_password(user_data.password,existing_user.password):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
    #password verified continue 
    payload={"sub":str(existing_user.id)}
    token=create_jwt_token(payload)
    return {"access_token":token,"token_type":"bearer"}


