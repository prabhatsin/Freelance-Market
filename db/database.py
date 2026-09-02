
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv()


db_url=os.getenv("DATABASE_URL")

engine=create_engine(url=db_url)


my_session=sessionmaker(
    bind=engine
)

def  get_db():
    db=my_session()
    try:
        yield db

    finally:
        db.close()


class Base(DeclarativeBase):
    pass
