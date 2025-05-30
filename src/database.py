import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

if os.getenv('ENVIRONMENT') == 'prod':
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL_PROD")
else: 
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL_LOCAL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
