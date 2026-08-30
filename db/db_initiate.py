from db.database import Base,engine
from models import models

def initiate():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("tables created succesfully")


if __name__=="__main__":
    initiate()

