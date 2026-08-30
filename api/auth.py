from fastapi import FastAPI
from fastapi import HTTPException

from schema.schema import UserLogin, UserSignup
from db.database import get_db
from fastapi import Depends,APIRouter
from models.models import User,UserRole
from sqlalchemy.orm import Session
from datetime import datetime,timedelta,timezone

from core.security import verify_password,create_jwt_token,hash_password

router=APIRouter()


@router.post('/signup')
def Signup(user_data:UserSignup,db:Session =Depends(get_db)):
    # Creating the instance of User class defined in models.py

    new_user=User(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.password),
        role=UserRole.CLIENT

    )
    existing_user=db.query(User).filter(User.email==user_data.email).first()
    if existing_user is None:
        db.add(new_user)
        db.commit() 
        return {"message: A New User Created Succesfully"}
    else:
        return {"message : User already exist"}


@router.post('/login')
def Login(user_data:UserLogin,db:Session =Depends(get_db)):
    existing_user=db.query(User).filter(User.email==user_data.email).first()
    if existing_user is  None:
        raise HTTPException (status_code=404,detail="User does not exist")
    else:
        # If verify_password retruns false ..
        if not verify_password(user_data.password,existing_user.password):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
    #password verified continue 
    payload={"user_id":str(existing_user.id),"role": existing_user.role,"exp": datetime.now(timezone.utc)+timedelta(minutes=60)}
    token=create_jwt_token(payload)
    return {"access_token":token,"token_type":"bearer"}




