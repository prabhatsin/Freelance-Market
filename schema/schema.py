from pydantic import BaseModel,PositiveFloat,model_validator,field_validator,ConfigDict
from datetime import date,datetime
from models.models import ProjectStatus ,ProposalStatus,UserRole
class UserSignup(BaseModel):
    name:str
    email:str
    password:str
    role:UserRole

class UserLogin(BaseModel):
    email:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class CreateProject(BaseModel):
    project_title:str
    project_description:str
    category:str
    budget_min:PositiveFloat
    budget_max:PositiveFloat
    deadline:date
    @model_validator(mode="after")
    def budget_max_check(self):
        if self.budget_max<self.budget_min:
            raise ValueError("budget_max should be greater than or equal to  budget min") 
        return self


    @field_validator('deadline',mode="after")
    @classmethod
    def deadline_check(cls,value:date):
        if value <=date.today():
            raise ValueError("The deadline should be in future")
        return value

#This schema is used to return created_project output from the db
class ProjectResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id: int
    client_id: int
    project_title: str
    project_description: str
    category: str
    budget_min: PositiveFloat
    budget_max: PositiveFloat
    deadline: date
    status: ProjectStatus
    created_at: datetime


class ProjectListItem(BaseModel):
    #This parameter is mostly used for response model 
    model_config=ConfigDict(from_attributes=True)
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



class  CreateProposals(BaseModel):
    cover_letter:str
    proposed_price:PositiveFloat
    estimated_duration:int

class ProposalList(BaseModel):
    proposal_id:int
    freelancer_id:int
    freelancer_name:str
    cover_letter:str
    proposed_price:float
    estimated_duration:int
    status:str
    created_at:datetime


'''
 project_id=project_id,
        submitted_by=freelancer_id,
        proposed_price=proposal_request.proposed_price,
        estimated_duration=proposal_request.estimated_duration,
        cover_letter
'''

class ProposalResponse(BaseModel):
    id:int
    project_id:int
    submitted_by:int
    proposed_price:PositiveFloat
    estimated_duration:int
    cover_letter:str
    status:ProposalStatus
    created_at:datetime


# Not needed 
# class CreateContract(BaseModel):
#     project_id:int
#     client_id:int
#     freelancer_id:int
#     proposed_price:float
#     status:str





























'''
from_attributes=True tells Pydantic that it is allowed to build a Pydantic model by reading 
attributes from an object, such as a SQLAlchemy ORM object.


1. Usually what happens is normally  pydantic expects data to look like json/dictionary 

{
    "id": 1,
    "name": "Akansha",
    "email": "akansha@example.com",
    "role": "client"
}

2. When we query db using orm be get (existing_projects/existing_user , ... these are orm objects),

So you need to tell Pydantic:

"Don't only look for dictionary keys. You can also look at the object's attributes."

thats exactly what 'model_config = ConfigDict(from_attributes=True)' used for 


'''














#Question:Note to implement this one ,  budgetMax >= budgetMin using pydantic, How do we do this ??? 

'''

Field validator
       ↓
Validate a particular field

Model validator
       ↓
Validate relationships between fields

'''

'''
Is the validation about ONE field?
        │
        └── Yes → field_validator

Is the validation about RELATIONSHIP
between multiple fields?
        │
        └── Yes → model_validator
'''

# Question , explain mode="after" and return self meaning , ?? 

'''
Run this validator AFTER Pydantic has validated the fields and created the model.
i.e 
1.First individual fields are validated , 
2.Then model is created  , what does it mean by model is created ??

Suppose you send:

Project(
    budgetMin="1000",
    budgetMax="5000"
)
first Pydantic can convert the strings:

"1000" → 1000
"5000" → 5000
 Secondly

Then it creates the model:

self = Project(
    budgetMin=1000,
    budgetMax=5000
)

After this validator runs

'''
#! return self

'''
returning self -->

in a general class what is self , it represents the instance of the class , 
similarly 

Here When Pydantic creates 
Project(
    budgetMin=1000,
    budgetMax=5000
)

self
 ↓
Project(
    budgetMin=1000,
    budgetMax=5000
)


Why do we return self?

Because an "after" model_validator is expected to return the validated model.

"Let me inspect this model."

        ↓

Is budgetMax >= budgetMin?

        ↓

YES

        ↓

"Everything is okay.
Here is the model; continue with it."


return self

'''

#!Whebn too use mode = before / after 

'''
mode="before"

Use it when your validator needs the raw input before Pydantic validates the fields.


mode="after"

Use it when your validator needs the fully validated model.

'''