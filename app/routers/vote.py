from fastapi import Response, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, oauth2, schemas

router = APIRouter(
    prefix='/votes',
    tags=['Votes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), authenticated_user = Depends(oauth2.get_current_user)):
    """
    """
    post = db.query(
                models.Post
            ).filter(
                models.Post.id == vote.post_id
            ).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {vote.post_id} does not exist"   
        )
    vote_query = db.query(
                models.Vote
            ).filter(
                models.Vote.user_id == authenticated_user.id, 
                models.Vote.post_id == vote.post_id
            )
    found_vote = vote_query.first()
    
    if vote.like:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail=f'User {authenticated_user.id} has alread voted on post {vote.post_id}'
            )
        new_vote = models.Vote(
                post_id = vote.post_id, 
                user_id = authenticated_user.id
            )
        db.add(new_vote)
        db.commit()
        
        return {"message": "successfully added vote"} 
    
    else: # Deleting a "like"
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Vote does not exist"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        
        return {"message": "successfully deleted vote"}