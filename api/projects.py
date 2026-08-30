from fastapi import FastAPI
from db.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from schema.schema import CreateProject,ProjectResponse
from core.dependencies import get_current_client
from models.models import Project 

app=FastAPI()


# project_request={
#   "project_title": "Build an E-commerce Website",
#   "project_description": "Need a full-stack e-commerce application",
#   "category": "Web Development",
#   "budget_min": 50000,
#   "budget_max": 100000,
#   "deadline": "2026-09-15"
# }
# project_id apne aap db create karegha
# client_id created by user_id who is logged_in
# status defaul is pending while creation , 
# created at created automatically , 

@app.post('/projects',response_model=ProjectResponse)
def create_projects(project_request:CreateProject,
                    current_user=Depends(get_current_client),
                    db:Session=Depends(get_db)):
    
    client_id=int(current_user["user_id"])
    new_project=Project(
        client_id=client_id,
        project_title=project_request.project_title,
        project_description=project_request.project_description,
        category=project_request.category,
        budget_min=project_request.budget_min,
        budget_max=project_request.budget_max,
        deadline=project_request.deadline
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project) # # so new_project.id, .status, .created_at get populated with their actual DB-generated values

    return new_project





#Learning ,=> Any column with a default= set in your model does NOT need to be passed when constructing the Python object
# example , status and created_at  they have  a default value , so they will get filled automatically , 


{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInJvbGUiOiJjbGllbnQiLCJleHAiOjE3ODgwNDMxNDh9.7quLCDlxtYaSDs3MRLoH_eUSvBoPnADBVJNQ3BEsYa0",
  "token_type": "bearer"
}
    

