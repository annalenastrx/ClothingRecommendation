import pandas as pd
import random

path = "Clothing.csv"
df = pd.read_csv(path)

rand = random.randint(0, 9970)

def get_random():
    return df.ClassName[rand]

def get_random(clothes):
    items = df.loc[df['DepartmentName'].str.contains(clothes, na=False), 'ClassName']
    piece_random = random.randint(0, items.count()-1)
    return items.iloc[piece_random]

# Dress -> summer, Dress + Jacket -> summer/spring/autumn, Top + Bottom -> summer/spring/autumn, Top + Bottom + Jacket -> winter/autumn

#depending on the season and adjective the user mentiones, a recommendation is given
#the parameter clothes decides the which combination piece is selected
#which piece is returned depends on a random row number
def get_adj_season(season, adjective, clothes):
    season_piece = df.loc[df['Seasons'].str.contains(season, na=False) & df['Adjectives'].str.contains(adjective, na=False) & df['DepartmentName'].str.contains(clothes, na=False), 'ClassName']
    if season_piece.empty:
        season_piece = df.loc[df['Seasons'].str.contains(season, na=False)  & df['DepartmentName'].str.contains(clothes, na=False), 'ClassName']
    piece_random = random.randint(0, season_piece.count()-1)
    print(season_piece.count())
    return season_piece.iloc[piece_random] 

#depending on the season the user mentiones, a recommendation is given
#the parameter clothes decides the which combination piece is selected
#which piece is returned depends on a random row number
def get_season(season, clothes):
    season_piece = df.loc[df['Seasons'].str.contains(season, na=False) & df['DepartmentName'].str.contains(clothes, na=False), 'ClassName']
    if season_piece.empty:
        season_piece = df.loc[df['Seasons'].str.contains(season, na=False)  & df['DepartmentName'].str.contains(clothes, na=False), 'ClassName']
    print(season_piece.count())
    
    piece_random = random.randint(0, season_piece.count()-1)
    return season_piece.iloc[piece_random] 

def get_event(event, clothes):
    if clothes == "":
        event_piece = df.loc[df['Nouns'].str.contains(event, na=False), 'ClassName']
        if event_piece.empty:
            return get_random()
    else:
        event_piece = df.loc[df['Nouns'].str.contains(event, na=False) & df['DepartmentName'].str.contains(clothes, na=False), 'ClassName']
        if event_piece.empty:
            return get_random(clothes)
    piece_random = random.randint(0, event_piece.count()-1)
    return event_piece.iloc[piece_random]

def get_adj_event(event, adjective, clothes):
    if clothes == "":
        event_piece = df.loc[df['Nouns'].str.contains(event, na=False) & df['Adjectives'].str.contains(adjective, na=False), 'ClassName']
        if event_piece.empty:
            event_piece =  df.loc[df['Nouns'].str.contains(event, na=False), 'ClassName']
    else:
        event_piece = df.loc[df['Nouns'].str.contains(event, na=False) & df['Adjectives'].str.contains(adjective, na=False) & df['DepartmentName'].str.contains(clothes, na=False), 'ClassName']
        if event_piece.empty:
            return get_event(event, clothes)
    piece_random = random.randint(0, event_piece.count()-1)
    return event_piece.iloc[piece_random]


def get_adj(adjective):
    if df[df['Adjectives']].str.contains(adjective):
        return df.ClassName


