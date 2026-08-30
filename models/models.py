from db.database import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,Integer, ForeignKey,DateTime
from datetime import datetime
from sqlalchemy import UniqueConstraint
import enum                    # Python's standard library
from sqlalchemy import Enum    # SQLAlchemy's library
from sqlalchemy import Numeric
from sqlalchemy import Date  # DB column type
from datetime import date # the Python value type

# This class that we are defining is purely python based it has nopthing to do db , sqlalchemy 
class UserRole(str,enum.Enum):
    CLIENT="client"
    FREELANCER="freelancer"

class ProjectStatus(str,enum.Enum):
    OPEN="open"
    IN_PROGRESS="in_progress"
    COMPLETED="completed"
    CANCELLED="cancelled"

class ProposalStatus(str,enum.Enum):
    PENDING="pending"
    ACCEPTED="accepted"
    REJECTED="rejected"

class ContractStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


#!------------------Below these are sqlalchemy models , above are python enum class ----------

class User(Base):

    __tablename__='users'
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(nullable=False)
    email:Mapped[str]=mapped_column(unique=True,nullable=False)
    password:Mapped[str]=mapped_column(String(90),nullable=False)
    role:Mapped[UserRole]=mapped_column(Enum(UserRole),nullable=False)
    #SQLAlchemy's Enum is a translator that sits between your Python enum and your database column.
    created_at:Mapped[datetime]=mapped_column(default=datetime.now)
    #TODO:  Explore diffrence between datetime.now and (insert_default=func.now())


class Project(Base):

    __tablename__='projects'
    id:Mapped[int]=mapped_column(primary_key=True)
    client_id:Mapped[int]=mapped_column(ForeignKey("users.id"),nullable=False)
    project_title:Mapped[str]=mapped_column(nullable=False)
    project_description:Mapped[str]=mapped_column(nullable=False)
    category:Mapped[str]=mapped_column(nullable=False)
    budget_min:Mapped[float]=mapped_column(Numeric(10,2),nullable=False)
    budget_max:Mapped[float]=mapped_column(Numeric(10,2),nullable=False)
    deadline:Mapped[date]=mapped_column(Date,nullable=False)
    #Numeric(10, 2) = up to 10 total digits, 2 after the decimal — standard for currency.
    status:Mapped[ProjectStatus]=mapped_column(Enum(ProjectStatus),nullable=False,default=ProjectStatus.OPEN) 
    created_at:Mapped[datetime]=mapped_column(default=datetime.now)

class Proposals(Base):

    __tablename__='proposals'
    __table_args__=(
        UniqueConstraint('project_id','submitted_by'),
    )
    id:Mapped[int]=mapped_column(primary_key=True)
    project_id:Mapped[int]=mapped_column(ForeignKey('projects.id'),nullable=False)
    submitted_by:Mapped[int]=mapped_column(ForeignKey('users.id'),nullable=False)
    proposed_price:Mapped[float]=mapped_column(Numeric(10,2),nullable=False)
    estimated_duration:Mapped[int]=mapped_column(nullable=False)
    status:Mapped[ProposalStatus]=mapped_column(Enum(ProposalStatus),nullable=False,default=ProposalStatus.PENDING) 
    cover_letter:Mapped[str]= mapped_column(nullable=False)
    created_at:Mapped[datetime]=mapped_column(default=datetime.now)


class Contracts(Base):
    __tablename__="contracts"
    id:Mapped[int]=mapped_column(primary_key=True)
    project_id:Mapped[int]=mapped_column(ForeignKey('projects.id'),nullable=False)
    client_id:Mapped[int]=mapped_column(ForeignKey("users.id"),nullable=False)
    freelancer_id:Mapped[int]=mapped_column(ForeignKey('users.id'),nullable=False)
    proposed_price:Mapped[float]=mapped_column(Numeric(10,2),nullable=False)
    status:Mapped[ContractStatus]=mapped_column(Enum(ContractStatus),nullable=False, default=ContractStatus.ACTIVE)
    created_at:Mapped[datetime]=mapped_column(default=datetime.now)







# date vs Date
'''
Mapped[date] → type annotation, tells your IDE/type-checker "this Python attribute will hold a datetime.date object"
mapped_column(Date, ...) → tells the actual database "make this column a real DATE type"

'''


#? Must read and understand
'''
In the simplest terms:

SQLAlchemy's Enum (the one used inside mapped_column)is a translator that sits between your Python enum and your database column.

Think of it like this

You have two worlds:

Python world: RoleEnum.client, RoleEnum.freelancer — objects
Database world: 'client', 'freelancer' — just plain text strings stored in a column

These two worlds don't naturally speak the same language. sqlalchemy.Enum is the translator that sits in between and does two jobs:

Tells the database: "Only allow these exact string values in this column, reject anything else" → so the DB creates a real constraint (native ENUM type or CHECK) that blocks bad data.
Translates back and forth automatically: when you save a Python object (RoleEnum.client) it converts it to the string 'client' for storage; when you read a row back, it converts the string 'client' back into the Python object RoleEnum.client for you.

One-line summary

Enum in SQLAlchemy = "take this Python enum, enforce its values as a real constraint in the database, and automatically convert values between Python objects and database strings whenever data moves in either direction."

'''





#!-----------------------------------------------------------------
'''
enum (lowercase) — Python's built-in module

1.This is a Python language feature, nothing to do with databases at all. It's just Python's way
 of defining "a fixed set of named constants." It exists whether or not you're using a database.



python
import enum

class RoleEnum(str, enum.Enum):
    client = "client"
    freelancer = "freelancer"

   
2. Here, enum.Enum is the base class you inherit from, coming from Python's standard library 
enum module. This alone just gives you a Python object — you could use RoleEnum.client 
anywhere in your code, in plain scripts, no DB involved at all. It's a general-purpose Python
tool for representing fixed choices.
'''

# Note: the 'Enum' in enum.Enum and 'Enum' used in mapped_column()

'''
Correct — they are not the same entity, even though they're both spelled Enum and used right 
next to each other. They come from two completely different libraries and do two different 
jobs.

They're imported from different places
python
import enum                    # Python's standard library
from sqlalchemy import Enum    # SQLAlchemy's library

What each one actually is

1.enum.Enum (lowercase enum, the module) → a base class you inherit from to define your own 
enum. When you write class RoleEnum(str, enum.Enum):, you are creating a new class that has 
client and freelancer as fixed attributes. This is pure Python — no database concept involved 
at all.

2.sqlalchemy.Enum (capital Enum, imported directly from sqlalchemy) → a column type, in the 
same family as Integer, String, Boolean. You don't inherit from it — you instantiate it and 
pass it as an argument inside Column(...) or mapped_column(...), to tell SQLAlchemy "generate a 
DB-level enum/check-constraint for this column, using the values from that Python enum I built." 



'''
                                        






# Question Mapped[] vs mapped_column use case 

'''
What Mapped[RoleEnum] actually is

This is a Python type annotation (using Python's typing system) — it exists purely for static 
typing purposes: your IDE, your type-checker (mypy), and SQLAlchemy's own type


What you lose by dropping Mapped[RoleEnum]

Since Mapped[RoleEnum] is purely a typing/annotation layer (as we just established), removing it means:

No static type checking — mypy/pyright won't know that user.role is a RoleEnum; it'll just see it as Any or infer from mapped_column's argument (weaker inference).
No IDE autocomplete for .role — your editor won't confidently suggest RoleEnum.client / RoleEnum.freelancer when you type user.role = .


mapped_column(...)	The actual column definition — this is where DB schema and ORM read/write 
behavior both get configured

nullable=False (inside mapped_column)	Purely DB-side — becomes a NOT NULL constraint in the schema

'''
