from fastapi import FastAPI

from schema.schema import UserLogin, UserSignup
from db.database import get_db
from fastapi import Depends
from models.models import User
from sqlalchemy.orm import Session

app=FastAPI()

@app.post('/signup')
def Signup(user_data:UserSignup,db:Session =Depends(get_db)):
    # Creating the instance of User class defined in models.py
    new_user=User(
        username=user_data.username,
        password=user_data.password
    )
    existing_user=db.query(User).filter(User.username==user_data.username).first()
    if existing_user is None:
        db.add(new_user)
        db.commit() 
        return {"message: A New User Created Succesfully"}
    else:
        return {"message : User already exist"}


@app.post('/login')
def Login(user_data:UserSignup,db:Session =Depends(get_db)):
    existing_user=db.query(User).filter(User.username==user_data.username).first()
    if existing_user is  None:
        return {"message: user does not exist"}
    else:
        if user_data.password==existing_user.password:
            return {"message: User Logged in Successfully"}
        return {"message: Wrong Password"}
, 