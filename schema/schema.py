from pydantic import BaseModel,PositiveFloat,model_validator,field_validator,ConfigDict
from datetime import date,datetime
from models.models import ProjectStatus 
class UserSignup(BaseModel):
    name:str
    email:str
    password:str

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