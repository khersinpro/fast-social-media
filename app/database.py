from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load the environment variables
load_dotenv()

SQLALCHEMY_DATABASE_URL  = os.getenv("DATABASE_URL")

# Database connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Session for database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declaring all the models to be used in the database
Base = declarative_base()

