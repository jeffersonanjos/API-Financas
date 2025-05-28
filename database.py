from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///financas.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)