from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

Base = declarative_base()

class Athlete(Base):
    __tablename__ = 'athletes'
    surrogate_id = Column(Integer, primary_key=True, autoincrement=True)  # Surrogate primary key
    id = Column(Integer)  # Original ID from the dataset
    name = Column(String(255))  # Assuming the maximum length for name is 255
    sex = Column(String(255))  # Set appropriate length for sex
    age = Column(Integer)
    height = Column(Float)
    weight = Column(Float)
    team = Column(String(255))  # Assuming the maximum length for team is 255
    noc = Column(String(10))  # Set appropriate length for noc
    games = Column(String(255))  # Assuming the maximum length for games is 255
    year = Column(Integer)
    season = Column(String(255))  # Set appropriate length for season
    city = Column(String(255))  # Assuming the maximum length for city is 255
    sport = Column(String(255))  # Assuming the maximum length for sport is 255
    event = Column(String(255))  # Assuming the maximum length for event is 255
    medal = Column(String(10))  # Set appropriate length for medal

# Database connection URL from environment variables
DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
