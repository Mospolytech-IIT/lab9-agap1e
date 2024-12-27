"""Лабораторная № 9"""
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship
from sqlalchemy import  Column, Integer, String, Text, ForeignKey, create_engine

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
db = SessionLocal()

#Создание

alex = Users(username = "Cro", email = "dasda@gmail.com", password = "3237")
bob = Users(username = "qsIs", email = "qsIs@gmail.com", password = "nd8As")
scott = Users(username = "ttoCs", email = "ttoCs@gmail.com", password = "gior2")

alex_post = Posts(title = "Book", content = "IDK", user_id = 1)
bob_post = Posts(title = "Movie", content = "Hello", user_id = 2)
bob_post_2 = Posts(title = "Snack", content = "Table", user_id = 2)
scott_post = Posts(title = "Magazine", content = "Bye", user_id = 3)

db.add_all([alex,bob,scott, alex_post, bob_post, scott_post, bob_post_2])
db.commit()

#Вывод

users = db.query(Users).all()
for i in users:
    print(f"ID: {i.id}; Username: {i.username}; Email: {i.email}; Password: {i.password}")
posts = db.query(Posts).all()
for i in posts:
    print(f"ID: {i.id}; Title: {i.title}; Content: {i.content}; Creator: {i.user.username}")

posts = db.query(Posts).filter(Posts.user_id == 2).all()
for i in posts:
    print(f"Creator: {i.user.username}; Title: {i.title}; Content: {i.content}")

#Обновление

alex = db.query(Users).filter(Users.id == 1).first()
alex.email = "se21@yandex.ru"

scott_post = db.query(Posts).filter(Posts.id == 3).first()
scott_post.content = "Hi"

db.commit()

#Удаление

alex_post = db.query(Posts).filter(Posts.id == 1).first()
db.delete(alex_post)

bob = db.query(Users).filter(Users.id == 2).first()
db.delete(bob)

db.commit()