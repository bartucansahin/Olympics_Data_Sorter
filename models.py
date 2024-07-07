from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()

class Athlete(Base):
    __tablename__ = 'athletes'
    surrogate_id = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Integer)
    name = Column(String(255))
    sex = Column(String(255))
    age = Column(Integer)
    height = Column(Float)
    weight = Column(Float)
    team = Column(String(255))
    noc = Column(String(10))
    games = Column(String(255))
    year = Column(Integer)
    season = Column(String(255))
    city = Column(String(255))
    sport = Column(String(255))
    event = Column(String(255))
    medal = Column(String(10))

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
