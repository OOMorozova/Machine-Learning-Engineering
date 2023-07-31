from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.dialects import postgresql

from database import SessionLocal
from table_user import User
from table_post import Post
from table_feed import Feed
from schema import PostGet, UserGet, FeedGet
from fastapi import HTTPException

app = FastAPI()


def get_db():
    with SessionLocal() as db:
        return db

#Информация о пользователе
@app.get("/user/{id}", response_model=UserGet)
def get_user(id: int, db: Session = Depends(get_db)):
    results = db.query(User).filter(User.id == id).first()
    if results is None:
        raise HTTPException(404, detail='user not found')
    return results

#Информация о публикации
@app.get("/post/{id}", response_model=PostGet)
def get_user(id: int, db: Session = Depends(get_db)):
    results = db.query(Post).filter(Post.id == id).first()
    if results is None:
        raise HTTPException(404, detail='post not found')
    return results

# Действия пользователя (последние)
@app.get("/user/{id}/feed", response_model=List[FeedGet])
def get_user_feed(id: int, limit: int = 10, db: Session = Depends(get_db)):
    results = db.query(Feed).filter(Feed.user_id == id).order_by(Feed.time.desc()).limit(limit).all()
    if results is None:
        results = []
    return results

#Действия с публикацией (последние)
@app.get("/post/{id}/feed", response_model=List[FeedGet])
def get_post_feed(id: int, limit: int = 10, db: Session = Depends(get_db)):
    results = db.query(Feed).filter(Feed.post_id == id).order_by(Feed.time.desc()).limit(limit).all()
    if results is None:
        results = []
    return results

# Необходимо подсчитать количество лайков для каждого поста, отсортировать по убыванию 
# и выдать первые limit записей постов (их id, text и topic). 
@app.get("/post/recommendations/", response_model=List[PostGet])
def get_post_feed(id: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    results = db.query(Post).join(Feed).filter(Feed.action == "like").group_by(Post.id).order_by(func.count(Post.id).desc()).limit(limit).all()
    # if results is None:
    #     results = []
    return results
