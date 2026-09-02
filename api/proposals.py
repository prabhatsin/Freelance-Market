from fastapi import FastAPI
from db.database import get_db
from fastapi import Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select,func
from schema.schema import CreateProposals,ProposalResponse,ProposalList
from core.dependencies import get_current_freelancer,get_current_client
from models.models import Project,Proposals,User,ProjectStatus,ProposalStatus,Contracts,ContractStatus
from fastapi import HTTPException,status

router=APIRouter()

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


@router.get("/projects/{project_id}/proposals",response_model=list[ProposalList])
def list_proposals(project_id:int,current_client=Depends(get_current_client),db:Session=Depends(get_db)):

    # step1 : check existing_client. i.e ,A client must not be able to view proposals belonging to someone else's project
    # first check if the project exist,
    stmt=select(Project).where(Project.id==project_id)
    result1=db.execute(stmt).scalars().first()
    if result1 is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="This Project does not exist")
    if result1.client_id!=int(current_client["user_id"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="The Project deos not belong to this client")

    statement=select(
                    Proposals.id.label("proposal_id"),
                    Proposals.submitted_by.label("freelancer_id"),
                    User.name.label("freelancer_name"),
                    Proposals.cover_letter,
                    Proposals.proposed_price,
                    Proposals.estimated_duration,
                    Proposals.status,
                    Proposals.created_at).join(User,User.id==Proposals.submitted_by).where(Proposals.project_id==project_id)

    result=db.execute(statement).all()
    return result



#! Learn Atomicity Before moving ahead with the last api (Contract Creation)


'''

Atomicity is a fundamental database property ensuring that a transaction is treated as a single, indivisible 
unit of work, meaning all operations within the transaction must succeed completely, or none are applied at all.

'''


@router.put("/proposals/{proposal_id}/accept")
def accept_proposal(proposal_id:int,current_client=Depends(get_current_client),db:Session=Depends(get_db)):
    # There is no condition(price/time/anything else) for the client to accept a proposal , any proposal can be accepted
    # But for a particular project only one proposal can be accepted !

    #check1: if the proposal even exist
    stmt=select(Proposals).where(Proposals.id==proposal_id)
    result=db.execute(stmt).scalars().first()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="PROPOSAL_NOT_FOUND")

    prop_status=result.status
    if prop_status != ProposalStatus.PENDING:
        raise  HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="PROPOSAL_ALREADY_PROCESSED")
    
    
    #check2: Does this proposal belong to Project owned by client making request
    proj_id=result.project_id # extract the project_id corresponding to this proposal

    # Now we check  the owner of this project from project table
    stmt_2=select(Project).where(Project.id==proj_id)
    result2=db.execute(stmt_2).scalars().first()
    current_client_id=int(current_client["user_id"])
    if result2.client_id!=current_client_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="This project does not belong to this client")


    try:
        # Now if all the above checks are marked , accept the proposal
        result.status=ProposalStatus.ACCEPTED 
        # get all the proposals corresponding to Project of this Proposal and mark theri status as rejected
        proposals_stmt=select(Proposals).where(Proposals.project_id==proj_id)
        proposals_result=db.execute(proposals_stmt).scalars().all() 
        #!Learning : # when we do .all() the object we get is iterable 
        for proposal in proposals_result:
            if proposal.status==ProposalStatus.ACCEPTED:
                continue
            proposal.status= ProposalStatus.REJECTED 
        # Set the status of project corresponding to this proposal as 'IN_PROGRESS
        result2.status=ProposalStatus.IN_PROGRESS
        # extract necessary field for contract object construction
        freelancer_id=result.submitted_by
        proposed_price=result.proposed_price
    
        stmt3=select(Contracts).where(Contracts.project_id==proj_id)
        contr=db.execute(stmt3).scalars().first()
        if contr is  not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Contract already exist')
        # Create a New Contract:
        new_contract=Contracts(
            project_id=proj_id,
            client_id=current_client_id,
            freelancer_id=freelancer_id,
            proposed_price=proposed_price,
            status=ContractStatus.ACTIVE
        )

        db.add(new_contract)
        db.commit()
        db.refresh(new_contract)
        return new_contract
    
    except Exception :
        db.rollback()
        raise # "Raise the exact same exception that was just caught."



#TODO: what exactly to return from this api , ??

'''
Two reasonable options

Option A — just return the contract

python
return new_contract

Simple, matches your existing pattern (return new_project, return new_proposal). The frontend gets the contract's data, but would need separate calls to re-fetch the proposal/project if it wants to show their updated status too.

Option B — return a combined response with all three pieces
Since the doc explicitly says the frontend needs to show updated proposal status, project status, and the contract — a single custom response schema bundling all three avoids the frontend needing extra round-trips right after this action:

python
{
  "proposal": {...},
  "project": {...},
  "contract": {...}
}





'''















'''
Atomicity,(Rollback) use case 
What does the rollback actually accomplish?
Imagine later your code becomes:

try:
    db.add(new_contract)

    # operation 1
    new_contract.status = "active"

    # operation 2
    some_other_record.status = "completed"

    # operation 3
    db.commit()

except Exception:
    db.rollback()
    raise

Suppose:

operation 1 → succeeds
operation 2 → succeeds
operation 3 → FAILS

Before commit(), those changes are part of the current database transaction.

So:

db.rollback()

basically says:

"Discard the uncommitted changes made in this transaction."

Result:

Operation 1 → rolled back
Operation 2 → rolled back
Operation 3 → failed

That's atomicity:

All operations succeed together, or none of them take effect.

'''
















































#! Learning(IMPORTANT)
'''
when we used to do "existing_user=db.query()............"
in the old querying style this existing user used to be a an instance of the User model

but 

in this select style of querying , when we write "result=db.execute(statement).first()"
this gives us the complete "row" not the Project instance , in order to get that instance use .scalars()

Explore more about .scalar , also when we did 'select(Proposals)' that selected all the columns of table we needed .scalalars
and when we choose invidual columns like in seconds api we didnt , ...
#! explore why

'''
