from fastapi import FastAPI
from db.database import get_db
from fastapi import Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select,func
from schema.schema import CreateProject,ProjectResponse,ProjectListItem
from core.dependencies import get_current_user,get_current_client
from models.models import Project ,User,Proposals



router=APIRouter()

@router.post('/projects',response_model=ProjectResponse)
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


'''
    id:int
    project_title: str
    project_description: str
    category: str
    budget_min: PositiveFloat
    budget_max: PositiveFloat
    deadline: date
    status: ProjectStatus
    client_name:str
    proposal_count:int


'''


# Here we have to perfrom join operation in order to get client_name , proposal_count

@router.get("/projects",response_model=list[ProjectListItem])
def list_projects(current_user=Depends(get_current_user),db:Session=Depends(get_db)):
    # Authenticated user meaning , get_current user only (via jwt verification)
    # It shouldnt be client/freelancer based anyone can see it
    statement=(
        select(Project.id,
               Project.project_title,
               Project.project_description,
               Project.category,
               Project.budget_min,
               Project.budget_max,
               Project.deadline,
               Project.status,
               User.name.label("client_name"),
               func.count(Proposals.id).label("proposal_count") 
               )
        .join(User,Project.client_id==User.id)
        .outerjoin(Proposals,Project.id==Proposals.project_id)
        .where(Project.status=='OPEN')
        .group_by(Project.id,User.name)
               )
        
    print(statement)
    result=db.execute(statement).all()
    return result




#! LEARNING

#--------------------------------------------------------------------------------------------------
#? IMPORTANT NOTE:
# db.query , This the legacy style of querying the db , described in legacy document (v1) 
# modern style is , described in version 2 

'''
stmt = (
    select(User)
    .join(User.addresses)
)

'''
'''
SQLAlchemy 2.x has standardized around:

select()
   ↓
db.execute()
   ↓
Result
------------------
The older:

db.query()

'''

'''
Joins in ORM two famous styles 
1. defined relationship in tyhe models 
2. explicitly use on , just like SQl queries 


'''
#Why .join at one place and .Outerjoint at other 

'''
1. join here means inner join ,

It means:
"Only return a project if its client exists."

2. Outerjoin (Same left join in mysql queries)

 "Return the project even if there is no matching proposal."

'''



#-----------------------------------------------------------------------------------------------------
















#! Question: We didnt needed ,"ProjectResponse.model_validate(new_project)" in our first api observe ??

'''
Your current flow(the first api)


Database
   ↓
SQLAlchemy Project object
   ↓
return new_project
   ↓
FastAPI sees response_model=ProjectResponse
   ↓
Pydantic converts/validates it
   ↓
JSON response

#!When would you actually use model_validate() yourself?

Suppose you're doing something inside your Python code, not simply returning the object from a FastAPI endpoint:

You need model_validate() manually when you want to explicitly convert a SQLAlchemy/other object into a Pydantic
model inside your Python code,(i.e u need the json .dict format in ur code) before returning or passing it elsewhere.

If you're simply returning the ORM object from a FastAPI endpoint with response_model=..., FastAPI performs 
this conversion for you, so manual model_validate() isn't needed.

'''








#Learning ,=> Any column with a default= set in your model does NOT need to be passed when constructing the Python object
# example , status and created_at  they have  a default value , so they will get filled automatically , 


{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInJvbGUiOiJjbGllbnQiLCJleHAiOjE3ODgwNDMxNDh9.7quLCDlxtYaSDs3MRLoH_eUSvBoPnADBVJNQ3BEsYa0",
  "token_type": "bearer"
}
    











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