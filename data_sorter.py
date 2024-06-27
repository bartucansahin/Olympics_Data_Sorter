import pandas as pd

df = pd.read_csv('/home/bart/workplace/Olympics_Data_Sorter/olym_data.csv')

all_countries = set(df["Team"].unique())
all_athletes = set(df["Name"].unique())
all_sports = set(df["Sport"].unique())

search_values = all_sports, all_athletes, all_countries


def sort_countries_alphabetically(all_countries):
    return sorted(all_countries, key=lambda country: country.lower())

def sort_athletes_alphabetically(all_athletes):
    return sorted(all_athletes, key=lambda athlete: athlete.lower())

def sort_sports_alphabetically(all_sports):
    return sorted(all_sports, key=lambda sport: sport.lower())


def sort_countries_by_medals(df):
    df = df[df['Medal'].isin(['Gold', 'Silver', 'Bronze'])]
    
    medals_pivot = df.pivot_table(index='Team', columns='Medal', aggfunc='size', fill_value=0)
    medals_pivot['Total'] = medals_pivot[['Gold', 'Silver', 'Bronze']].sum(axis=1)

    sorted_medals = medals_pivot[['Gold', 'Silver', 'Bronze', 'Total']].sort_values(by='Total', ascending=False)
    return sorted_medals

class Search_Bar:
    def __init__(self):
        self.objects = self._initialize_objects()

    def _initialize_objects(self):
        sports = list(all_sports)
        athletes = list(all_athletes)
        countries = list(all_countries)

        return sports + athletes + countries

    def search(self, word):
        word_lower = word.lower()
        matches = [obj for obj in self.objects if word_lower in obj.lower()]
        matches.sort(key=lambda obj: (not obj.lower().startswith(word_lower), obj))

        results = []
        for match in matches:
            if match in all_sports:
                result = {
                    "id": None,
                    "Name": match,
                    "type": 0,
                    "NOC": None
                }
            elif match in all_athletes:
                athlete_info = df[df['Name'].str.lower() == match.lower()].iloc[0]
                result = {
                    "id": int(athlete_info['ID']),
                    "Name": athlete_info['Name'],
                    "type": 1,
                    "NOC": None
                }
            elif match in all_countries:
                result = {
                    "id": None,
                    "Name": match,
                    "type": 2,
                    "NOC": match
                }
            results.append(result)

        return results

def display_info(value):
    if value in df['Name'].values:
        events_attended = set(df[df['Name'] == value]['Event'])
        active_years = sorted(set(df[df['Name'] == value]['Year']))
        years_list = list(active_years)

        gold_medals = df[(df['Name'] == value) & (df['Medal'] == 'Gold')].shape[0]
        silver_medals = df[(df['Name'] == value) & (df['Medal'] == 'Silver')].shape[0]
        bronze_medals = df[(df['Name'] == value) & (df['Medal'] == 'Bronze')].shape[0]

        total_medals = gold_medals + silver_medals + bronze_medals

        attended_olympics = df[df['Name'] == value][['Year', 'City']].drop_duplicates()

        info_dict = {
            "Name": value,
            "events_attended": list(events_attended),
            "active_years": years_list,
            "gold_medals": gold_medals,
            "silver_medals": silver_medals,
            "bronze_medals": bronze_medals,
            "total_medals": total_medals,
            "attended_olympics": attended_olympics.to_dict(orient='records')
        }

        return info_dict

    elif value in df['Team'].values:
        team_df = df[df['Team'] == value]
        total_attendance = len(team_df['Games'].unique())
        unique_athletes = len(team_df['Name'].unique())

        team_gold_medals = team_df[team_df['Medal'] == 'Gold'].shape[0]
        team_silver_medals = team_df[team_df['Medal'] == 'Silver'].shape[0]
        team_bronze_medals = team_df[team_df['Medal'] == 'Bronze'].shape[0]
        team_total_medals = team_gold_medals + team_silver_medals + team_bronze_medals

        top_sports = (team_df[team_df['Medal'].notna()]
                      .groupby('Sport')
                      .size()
                      .sort_values(ascending=False)
                      .head(5)
                      .index)

        top_sports_medals = {sport: {
            "gold": team_df[(team_df['Sport'] == sport) & (team_df['Medal'] == 'Gold')].shape[0],
            "silver": team_df[(team_df['Sport'] == sport) & (team_df['Medal'] == 'Silver')].shape[0],
            "bronze": team_df[(team_df['Sport'] == sport) & (team_df['Medal'] == 'Bronze')].shape[0],
        } for sport in top_sports}

        team_info_dict = {
            "Team": value,
            "total_attendance": total_attendance,
            "unique_athletes": unique_athletes,
            "gold_medals": team_gold_medals,
            "silver_medals": team_silver_medals,
            "bronze_medals": team_bronze_medals,
            "total_medals": team_total_medals,
            "top_sports_medals": top_sports_medals
        }

        return team_info_dict

    elif value in df['Sport'].values:
        sport_df = df[df['Sport'] == value]

        top_athletes = (sport_df[sport_df['Medal'].notna()]
                        .groupby('Name')
                        .size()
                        .sort_values(ascending=False)
                        .head(5)
                        .index)

        top_athletes_medals = {
            athlete: {
                "gold": sport_df[(sport_df['Name'] == athlete) & (sport_df['Medal'] == 'Gold')].shape[0],
                "silver": sport_df[(sport_df['Name'] == athlete) & (sport_df['Medal'] == 'Silver')].shape[0],
                "bronze": sport_df[(sport_df['Name'] == athlete) & (sport_df['Medal'] == 'Bronze')].shape[0],
                "total": sport_df[(sport_df['Name'] == athlete) & (sport_df['Medal'].isin(['Gold', 'Silver', 'Bronze']))].shape[0]
            }
            for athlete in top_athletes
        }


        unique_events = sport_df['Event'].value_counts().index.tolist()

        sport_info_dict = {
            "Sport": value,
            "top_athletes_medals": top_athletes_medals,
            "unique_events": unique_events
        }

        return sport_info_dict

def main():

    print(display_info("Sailing"))


if __name__ == "__main__":
    main()
