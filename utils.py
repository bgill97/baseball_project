import pandas as pd
import traceback
import time
from pybaseball.playerid_lookup import get_lookup_table

team_dict = {
    'ATH': 'athletics',
    'ARI': 'diamondbacks',
    'ATL': 'braves',
    'BAL': 'orioles',
    'BOS': 'red_sox',
    'CHC': 'cubs',
    'CIN': 'reds',
    'CLE': 'guardians',
    'COL': 'rockies',
    'CHW': 'white_sox',
    'DET': 'tigers',
    'HOU': 'astros',
    'KCR': 'royals',
    'LAA': 'angels',
    'LAD': 'dodgers',
    'MIA': 'marlins',
    'MIL': 'brewers',
    'MIN': 'twins',
    'NYM': 'mets',
    'NYY': 'yankees',
    'OAK': 'athletics',
    'PHI': 'phillies',
    'PIT': 'pirates',
    'SDP': 'padres',
    'SEA': 'mariners',
    'SFG': 'giants',
    'STL': 'cardinals',
    'TBR': 'rays',
    'TEX': 'rangers',
    'TOR': 'blue_jays',
    'WSN': 'nationals'}

def get_players_played_in_year(year):
    """
    Returns a dataframe of all players who played in a given year.
    """
    df = get_lookup_table()
    df = df[df['mlb_played_last'] == float(year)]
    return df

def get_player_name(player_id):
    df = get_lookup_table()
    player_row = df[df['key_mlbam'] == player_id]
    if not player_row.empty:
        return player_row.iloc[0]['name_first'] + ' ' + player_row.iloc[0]['name_last']
    return "Player not found"

def atbat_outcomes(start_date, end_date):
    """
    Returns a dataframe of all at-bat outcomes between the given start and end dates.
    """
    from pybaseball import statcast
    atbat_outcomes = statcast(start_date, end_date)
    atbat_outcomes.reset_index(drop=True,inplace=True)
    atbat_outcomes.dropna(subset=['events'], inplace=True)
    return atbat_outcomes

def all_pitches(start_date, end_date):
    """
    Returns a dataframe of all pitches thrown between the given start and end dates.
    """
    from pybaseball import statcast
    pitches = statcast(start_date, end_date)
    pitches.reset_index(drop=True,inplace=True)
    return pitches

def game_outcomes(year: int):
    """
    Returns a dataframe of all game outcomes between the given start and end dates.
    """
    from pybaseball import schedule_and_record
    frames = []
    for team in team_dict.keys():
        time.sleep(2)
        if year >= 2025 and team == 'OAK':
            code = 'ATH'
        elif year < 2025 and team == 'ATH':
            code = 'OAK'
        else:
            code = team
        try:
            games = schedule_and_record(year, code)
        except Exception as e:
            print(f"Error fetching data for {code} in {year}: {e}")
            traceback.print_exc()
            continue
        frames.append(games)
    games_df = pd.concat(frames, ignore_index=True)
    games_df['game_num'] = (
        games_df['Date'].str.extract(r'\((\d+)\)$')[0].fillna(1).astype(int)
    )
    clean = games_df['Date'].str.replace(r'\s*\(\d+\)$', '', regex=True)
    games_df['date'] = pd.to_datetime(clean + f', {year}', format="%A, %b %d, %Y")
    games_df.drop(columns=['Date'],inplace=True)
    return games_df