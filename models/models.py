from db.database import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String, Integer, ForeignKey,DateTime
from datetime import datetime
class User(Base):

    __tablename__='user'
    id:Mapped[int]=mapped_column(primary_key=True)
    username:Mapped[str]=mapped_column(unique=True,nullable=False)
    password:Mapped[str]=mapped_column(String(30),nullable=False)

class Task(Base):
    __tablename__='task'
    task_id:Mapped[int]=mapped_column(primary_key=True, nullable=False)
    task_name:Mapped[str]
    created_by:Mapped[int]=mapped_column(
        ForeignKey("user.id")
    )
    # Add a default time 
    created_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=True)
    )
    status:Mapped[str]


