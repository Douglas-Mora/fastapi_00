from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

password = "@MspudD7!"
encoded_password = quote_plus(password)
SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:{encoded_password}@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Next used just to test the connection.
def test_connection():
    try:
        connection = engine.connect()
        print("Connection successful!")
        connection.close()
    except Exception as e:
        print(f"Connection error: {e}")

#if __name__ == "__main__":
#    test_connection()


