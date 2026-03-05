import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase

load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL")


class Base(DeclarativeBase):
    pass

# Create database engine
# Echo = True would print all sql queries (useful for debugging.)

engine=create_engine(
    url=DATABASE_URL,
    echo=False, #Set to True to see SQL queries
    future=True # Use SQLAlchemt 2.0 style.,
)

SessionLocal=sessionmaker(
    bind=engine,
    autoflush=False, #Dont automtically flush changes.
    autocommit=False, #Dont autometically commit.
    future=True 
)