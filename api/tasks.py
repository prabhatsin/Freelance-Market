from fastapi import FastAPI

from schema.schema import CreateTask
from db.database import get_db
from fastapi import Depends
from models.models import Task
from sqlalchemy.orm import Session

app=FastAPI()



@app.post("tasks")

def create_task(task:CreateTask,db:Session=get_db):
    current_user=db.filter()
    new_task=Task(
        task_name=task.task_name,
        # here the user_id of logged in user should come
        created_by=current_user.id



    )

    