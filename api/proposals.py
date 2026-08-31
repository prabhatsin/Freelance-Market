from fastapi import FastAPI
from db.database import get_db
from fastapi import Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select,func
from schema.schema import CreateProposals,ProposalResponse
from core.dependencies import get_current_freelancer
from models.models import Project ,Proposals,ProjectStatus
from fastapi import HTTPException,status

router=APIRouter()

'''
{
  "cover_letter": "I have 3 years of experience building web applications.",
  "proposed_price": 75000,
  "estimated_duration": 20
}

'''


# why {} this bracket and whats the purpose 
# Here this project_id is path parameter 


'''
### Must handle

- Project doesn't exist
- Project isn't open
- User isn't a freelancer
- Freelancer already submitted a proposal
- Invalid request body

'''
'''
    **Freelancer only**
    Submit a proposal.
'''


@router.post("/projects/{project_id}/proposals",response_model=ProposalResponse)
def sumbit_proposals(proposal_request:CreateProposals,
                     project_id:int,
                     current_freelancer=Depends(get_current_freelancer),
                     db:Session=Depends(get_db)):
    # step1: check project does exist
    statement=select(Project).where(Project.id==project_id)
    # result=db.execute(statement).first()  # This gives a row not an Project Object
    result=db.execute(statement).scalars().first()

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="The requested project is not present")
    # step 2 if project exist ,check if status is open , 
    if result.status!=ProjectStatus.OPEN:
        raise HTTPException (status_code=status.HTTP_400_BAD_REQUEST,detail="PROJECT_NOT_OPEN")
    # step 3 check if freelancer hadnt already proposed on this project
    freelancer_id=int(current_freelancer["user_id"]) # We use this int here because user_id is str in payload in Login endpoint
    # search the proposals table using both this freelancer_id and project_id
    statement1=select(Proposals).where(Proposals.submitted_by==freelancer_id ,Proposals.project_id==project_id )
    result1=db.execute(statement1).scalars().first()
    if result1 is not None:
        raise HTTPException (status_code=status.HTTP_409_CONFLICT,detail="Proposal already submitted by the freelancer")

    # final create proposal request body and inser in the db
    new_proposal=Proposals(
        project_id=project_id,
        submitted_by=freelancer_id,
        proposed_price=proposal_request.proposed_price,
        estimated_duration=proposal_request.estimated_duration,
        cover_letter=proposal_request.cover_letter,
    )
    db.add(new_proposal)
    db.commit()
    db.refresh(new_proposal)
    return new_proposal




    
#! Learning(IMPORTANT)
'''
when we used to do "existing_user=db.query()............"
in the old querying style this existing user used to be a an instance of the User model

but 

in this select style of querying , when we write "result=db.execute(statement).first()"
this gives us the complete "row" not the Project instance , in order to get that instance use .scalars()


'''
