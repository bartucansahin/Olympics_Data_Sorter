import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Athlete, Base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

df = pd.read_csv('/code/Merged_Data.csv')

df = df.where(pd.notnull(df), None)

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

session.bulk_save_objects(athletes)
session.commit()
