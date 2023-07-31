from fastapi import FastAPI, Depends
from datetime import datetime, timedelta, date
from loguru import logger
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException

app = FastAPI()


class User(BaseModel):
    name: str
    surname: str
    age: int
    registration_date: date


class PostResponse(BaseModel):
    id: int
    text: str
    topic: str

    class Config:
        orm_mode = True

#Данные по подключению к базе
def get_db():
    conn = psycopg2.connect(
        database="",
        user="", 
        password="",
        host="", 
        cursor_factory=RealDictCursor,
        port=6432)
    return conn


@app.get("/")
def s(a: int, b: int) -> int:
    return a + b

#Увеличить текущую дату на offset дней
@app.get("/sum_date")
def sum_date(current_date: date, offset: int) -> date:
    return current_date + timedelta(days=offset)

#Валидация данных пользователя
@app.post("/user/validate")
def validate_user(user: User):
    logger.info(user.dict())
    return "Will add user: {name} {surname} with age {age}"

# Информация о пользователе
@app.get("/user/{id}")
def user_id(id: int, db=Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute(
            """
                select gender, age, city
                  from "user"
                where id = %s
        """, (id,))
        f = cursor.fetchone()
    if f is None:
        raise HTTPException(404, detail="user not found")
    return f

#Информация о публикации
@app.get("/post/{id}", response_model=PostResponse)
def post_id(id: int, db=Depends(get_db)) -> PostResponse:
    with db.cursor() as cursor:
        cursor.execute(
            """
                select id, text, topic
                  from "post"
                where id = %s
        """, (id,))
        f = cursor.fetchone()
    if f is None:
        raise HTTPException(404, detail='post not found')
    return PostResponse(**f)
