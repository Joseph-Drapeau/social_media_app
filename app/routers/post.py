from xml.dom.minidom import Attr
from fastapi import Response, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from ..database import get_db
from .. import models, oauth2
from ..schemas import Post, PostCreate, PostOut
from sqlalchemy.inspection import inspect

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

# @router.get('/', response_model=list[Post])
@router.get('/', response_model=list[PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, 
    search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    ## posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get('/{id}', response_model=PostOut)
def get_post(id: int, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    # print(post2.__dict__)
    print(type(post.Post))

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
            detail=f'post with id: {id} was not found')
    
    if post.Post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized to perform requested action")
    
    return post

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= 'post with {id} does not exist')
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)
    
@router.put('/{id}', response_model=Post) # , status_code=status.HTTP_)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    update_post = post_query.first()
    
    if update_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= 'post with {id} does not exist')

    if update_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit() 
    return post_query.first()