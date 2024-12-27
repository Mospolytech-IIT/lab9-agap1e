"""Веб-приложение"""
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship
from sqlalchemy import  Column, Integer, String, Text, ForeignKey, create_engine
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, Body
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

class Base(DeclarativeBase):
    """Базовая модель"""

class Users(Base):
    """Модель пользователей"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique = True)
    email = Column(String, unique = True)
    password = Column(String)
    posts = relationship("Posts", back_populates="user", cascade="all, delete-orphan")

class Posts(Base):
    """Модель постов"""
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users", back_populates="posts")

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

def get_db():
    """Получение бд"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User(BaseModel):
    """Пользователь(через BaseModel)"""
    username: str
    email: str
    password: str

class Userpost(BaseModel):
    """Пост(через BaseModel)"""
    title: str
    content: str
    username: str

app = FastAPI()

@app.get("/create/user")
def create_user_show():
    """Страница создания пользователя"""
    return FileResponse("public/reg.html")

@app.post("/create/user")
def create_user(user: User, db: Session = Depends(get_db)):
    """Добавление пользователя в бд"""
    user_db = Users(username = user.username, email = user.email, password = user.password)
    db.add(user_db)
    db.commit()
    return user_db

@app.get("/view/users")
def view_users(db: Session = Depends(get_db)):
    """Вывод пользователей"""
    users = db.query(Users).all()
    return users

@app.delete("/delete/user")
def delete_user(data = Body(), db: Session = Depends(get_db)):
    """Удаление пользователя"""
    username = data["username"]
    user = db.query(Users).filter(Users.username == username).first()
    db.delete(user)
    db.commit()
    return {"msg":"Successfully deleted"}

@app.patch("/patch/user")
def patch_user(data = Body(), db: Session = Depends(get_db)):
    """Редактирование пользователя"""
    username = data["username"]
    email = data["email"]
    user = db.query(Users).filter(Users.username == username).first()
    user.email = email
    db.commit()
    return {"msg":"Successfully changed"}


@app.get("/create/post")
def create_post_show():
    """Страница создание поста"""
    return FileResponse("public/post_create.html")

@app.post("/create/post")
def create_post(post: Userpost, db: Session = Depends(get_db)):
    """Добавление постав в бд"""
    user = db.query(Users).filter(Users.username == post.username).first()
    if user is None:
        return JSONResponse(content={"message": "Resource Not Found"}, status_code=404)
    post_db = Posts(title = post.title, content = post.content, user_id = user.id)
    db.add(post_db)
    db.commit()
    return post_db

@app.get("/view/posts")
def view_posts(db: Session = Depends(get_db)):
    """Вывод постов"""
    posts = db.query(Posts).all()
    return posts

@app.delete("/delete/post")
def delete_post(data = Body(), db: Session = Depends(get_db)):
    """Удаление поста"""
    title = data["title"]
    post = db.query(Posts).filter(Posts.title == title).first()
    db.delete(post)
    db.commit()
    return {"msg":"Successfully deleted"}

@app.patch("/patch/post")
def patch_post(data = Body(), db: Session = Depends(get_db)):
    """Редактирование поста"""
    title = data["title"]
    content = data["content"]
    post = db.query(Posts).filter(Posts.title == title).first()
    post.content = content
    db.commit()
    return {"msg":"Successfully changed"}
