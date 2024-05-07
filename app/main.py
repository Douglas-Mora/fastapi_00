from fastapi import FastAPI
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database="fastapi", user="postgres", password="@MspudD7!", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Successfully connected to database!")
        break
    except Exception as error:
        print("Connection error occurred!")
        print(f"Error: {error}")
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message":"Hello, world!"}