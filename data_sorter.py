import pandas as pd

df = pd.read_csv("/home/bart/workplace/Olympics_Data_Sorter/Merged_Data.csv")

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
        self.all_sports_lower = {sport.lower(): sport for sport in all_sports}
        self.all_athletes_lower = {athlete.lower(): athlete for athlete in all_athletes}
        self.all_countries_lower = {country.lower(): country for country in all_countries}
        
        self.df_lower_name_map = self._create_name_map(df)

    def _create_name_map(self, df):
        name_map = {}
        for _, row in df.iterrows():
            name_lower = row['Name'].lower()
            if name_lower not in name_map:
                name_map[name_lower] = []
            name_map[name_lower].append(row)
        return name_map

    def search(self, word):
        word_lower = word.lower()
        results = []

        def add_result(name_map, obj_type, noc_value=None):
            for key, value in name_map.items():
                if word_lower in key:
                    if obj_type in (0, 2):
                        results.append({
                            "id": None,
                            "Name": value,
                            "type": obj_type,
                            "NOC": noc_value(value) if noc_value else None
                        })
                    else:
                        athlete_infos = self.df_lower_name_map.get(key, [])
                        for athlete_info in athlete_infos:
                            results.append({
                                "id": int(athlete_info['ID']),
                                "Name": athlete_info['Name'],
                                "type": obj_type,
                                "NOC": athlete_info['NOC']
                            })

        add_result(self.all_sports_lower, 0)
        add_result(self.all_athletes_lower, 1)
        add_result(self.all_countries_lower, 2, lambda x: x)

        results.sort(key=lambda obj: (not obj['Name'].lower().startswith(word_lower), obj['Name']))
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

    elif value in df['Event'].values:
        event_df = df[df['Event'] == value]

        last_5_gold_winners = (event_df[event_df['Medal'] == 'Gold']
                               .sort_values(by='Year', ascending=False)
                               .head(5)[['Name', 'Year', 'Team']])

        last_5_silver_winners = (event_df[event_df['Medal'] == 'Silver']
                                 .sort_values(by='Year', ascending=False)
                                 .head(5)[['Name', 'Year', 'Team']])

        last_5_bronze_winners = (event_df[event_df['Medal'] == 'Bronze']
                                 .sort_values(by='Year', ascending=False)
                                 .head(5)[['Name', 'Year', 'Team']])

        event_info_dict = {
            "Event": value,
            "last_5_gold_winners": last_5_gold_winners.to_dict(orient='records'),
            "last_5_silver_winners": last_5_silver_winners.to_dict(orient='records'),
            "last_5_bronze_winners": last_5_bronze_winners.to_dict(orient='records')
        }

        return event_info_dict

        



def main():

    search_bar = Search_Bar()
    results = search_bar.search("John")
    print(results)

if __name__ == "__main__":
    main()
