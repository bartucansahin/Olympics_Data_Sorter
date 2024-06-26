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

        matches = [obj for obj in self.objects if word in obj]
        matches.sort(key=lambda obj: (not obj.startswith(word), obj))
        
        for match in matches:
            print(match)


def main():

    test = Search_Bar()
    result = test.search("Ald")

if __name__ == "__main__":
    main()
