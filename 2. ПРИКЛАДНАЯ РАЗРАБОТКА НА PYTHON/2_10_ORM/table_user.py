from sqlalchemy import Column, Integer, String, select, func

from database import Base, SessionLocal


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    city = Column(String)
    country = Column(String)
    exp_group = Column(Integer)
    gender = Column(Integer)
    os = Column(String)
    source = Column(String)


if __name__ == "__main__":
    session = SessionLocal()
    results = session.execute(
        select(User.country, User.os, func.count(User.id))
            .filter(User.exp_group == 3)
            .group_by(User.country, User.os)
            .having(func.count(User.id) > 100)
            .order_by(func.count(User.id).desc())
    )
    print(list(results))
