import os
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Athlete, Base
from data_sorter import sort_countries_alphabetically, sort_athletes_alphabetically, sort_sports_alphabetically, sort_countries_by_medals, Search_Bar, display_info
import pandas as pd

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root:U628DgZS=ZW7@db/olympics')

print(f"DATABASE_URL: {DATABASE_URL}")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/athletes', methods=['GET'])
def get_athletes():
    all_athletes = session.query(Athlete.name).distinct().all()
    all_athletes = [athlete[0] for athlete in all_athletes]
    athletes_list = sort_athletes_alphabetically(all_athletes)
    return jsonify(athletes_list)

@app.route('/countries', methods=['GET'])
def get_countries():
    all_countries = session.query(Athlete.team).distinct().all()
    all_countries = [country[0] for country in all_countries]
    countries_list = sort_countries_alphabetically(all_countries)
    return jsonify(countries_list)

@app.route('/sports', methods=['GET'])
def get_sports():
    all_sports = session.query(Athlete.sport).distinct().all()
    all_sports = [sport[0] for sport in all_sports]
    sports_list = sort_sports_alphabetically(all_sports)
    return jsonify(sports_list)

@app.route('/countries/medals', methods=['GET'])
def get_countries_by_medals():
    query = session.query(Athlete.team, Athlete.medal).all()
    
    data = [{'Team': team, 'Medal': medal} for team, medal in query]
    df = pd.DataFrame(data)
    
    sorted_medals = sort_countries_by_medals(df)
    return sorted_medals.to_json(orient='records')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    search_bar = Search_Bar()
    results = search_bar.search(query)
    return jsonify(results)

@app.route('/info', methods=['GET'])
def get_info():
    value = request.args.get('value', '')
    info = display_info(value)
    return jsonify(info)

if __name__ == '__main__':
    app.run(debug=True)
