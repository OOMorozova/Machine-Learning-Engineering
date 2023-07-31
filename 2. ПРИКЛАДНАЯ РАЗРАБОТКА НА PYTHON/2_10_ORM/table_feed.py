from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Session, relationship

from database import Base, SessionLocal
from table_post import Post
from table_user import User


class Feed(Base):
    __tablename__ = "feed_action"
    __table_args__ = {"schema": "public"}

    post_id = Column(Integer, ForeignKey(Post.id), primary_key=True)
    post = relationship(Post)
    action = Column(String)
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    user = relationship(User)
    time = Column(TIMESTAMP)
