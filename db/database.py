
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase


# Just add one step here take these values from .env now like this 
db_url=URL.create(
    drivername="postgresql",
    username="prabhat",
    password="centralexchange_123",
    host='localhost',
    port=5432,
    database='todo_db'
)



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


# from sqlalchemy import text

# with engine.connect() as connection:
#     result = connection.execute(
#         text("SELECT current_user, current_database();")
#     )
#     print(result.fetchone())

# from sqlalchemy import text

# with engine.connect() as connection:
#     result = connection.execute(text("""
#         SELECT
#             current_user,
#             current_database(),
#             inet_server_addr(),
#             inet_server_port(),
#             version()
#     """))

#     print(result.fetchone())

#     result = connection.execute(text("""
#         SELECT
#             has_schema_privilege(current_user, 'public', 'CREATE')
#     """))

#     print("Can create:", result.fetchone())