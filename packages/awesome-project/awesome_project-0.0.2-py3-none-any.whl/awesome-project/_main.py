from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
import psycopg2
from psycopg2.extras import RealDictCursor





# try:
#     # Connect to your postgres DB
#     conn = psycopg2.connect(host = 'localhost', database= 'postgres', user='kartikkumar', password = 'kartikkumar50fin', cursor_factory=RealDictCursor)
#     print("Database connection is successful")
# # Open a cursor to perform database operations
#     cur = conn.cursor()

# # Execute a query
#     cur.execute("SELECT * FROM posts")

# # Retrieve query results
#     records = cur.fetchall()

# except  Exception as error: 
#     print(error)


# @app.get("/")
# async def root():
#     return {"message": "wlecome to home"} 


# # retruning a bunch of socila media posts 
# # lets try to define the base model of the posts 
# class Post(BaseModel):
#     title: str 
#     content: str
#     published: bool = True # the default value is True

# @app.get("/posts/")
# async def get_posts():
#     cur.execute("SELECT * FROM posts")
#     posts = cur.fetchall()
#     print(posts)
    
#     return {"posts": posts}

# @app.post("/create_post")
# async def create_posts(post:Post):
#     cur.execute("""
#                     INSERT INTO posts
#                     (title, content, published)
#                     VALUES (%s,%s,%s) RETURNING *;
#                    """, (post.title, post.content, post.published ))
#     conn.commit()
#     new_post = cur.fetchone()
#     return {"post created" : new_post}








# from sqlalchemy import create_engine
# from sqlalchemy.engine import URL
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import Column, Integer, String, Boolean
# from sqlalchemy.orm import declarative_base


# url = URL.create(
#     drivername="postgresql",
#     username="kartikkumar",
#     password="kartikkumar50fin",
#     host="localhost",
#     database="postgres",
#     port=5432
# )


# engine = create_engine(url)
# Session = sessionmaker(bind=engine)
# session = Session()



# Base = declarative_base()

# class Todo(Base):
#     __tablename__ = "todos"

#     id = Column(Integer, primary_key=True)
#     text = Column(String)
#     is_done = Column(Boolean, default=False)


# Base.metadata.create_all(engine)

# @app.post("/create")
# async def create_todo(text: str, is_complete: bool = False):
#     todo = Todo(text=text, is_done=is_complete)
#     session.add(todo)
#     session.commit()
#     return {"todo added": todo.text}



