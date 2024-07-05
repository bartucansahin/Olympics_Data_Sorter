import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Athlete, Base
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database connection URL
DATABASE_URL = os.getenv('DATABASE_URL')

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create all tables in the database which are defined by Base's subclasses such as Athlete
Base.metadata.create_all(engine)

# Create a new session
Session = sessionmaker(bind=engine)
session = Session()

# Load and preprocess the CSV data
df = pd.read_csv('/code/Merged_Data.csv')

# Replace NaN with None for proper insertion
df = df.where(pd.notnull(df), None)

# Insert data
athletes = []
for index, row in df.iterrows():
    athlete = Athlete(
        id=row['ID'],
        name=row['Name'],
        sex=row['Sex'],
        age=row['Age'],
        height=row['Height'],
        weight=row['Weight'],
        team=row['Team'],
        noc=row['NOC'],
        games=row['Games'],
        year=row['Year'],
        season=row['Season'],
        city=row['City'],
        sport=row['Sport'],
        event=row['Event'],
        medal=row['Medal']
    )
    athletes.append(athlete)

# Bulk save all the athlete objects
session.bulk_save_objects(athletes)
session.commit()
