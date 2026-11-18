#What are attendance numbers like at every ballpark? Do certain teams draw more fans on the road than others? What matchups draw the most fans?

from utils import game_outcomes
import numpy as np
import pandas as pd

#set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

#setting up df
games = game_outcomes(2026)
games.drop_duplicates(subset=['Date','Win','Loss','Time','Attendance'], keep='first', inplace=True)
games.reset_index(drop=True, inplace=True)

#refactor df for home and away teams
is_away = games['Home_Away'] == '@'
games['away'] = np.where(is_away, games['Tm'], games['Opp'])
games['home'] = np.where(is_away, games['Opp'], games['Tm'])
games.drop(columns=['Tm','Opp','Home_Away'], inplace=True)

#filter out unnecessary columns
games = games[['Date','away','home','W/L','R','RA','Inn','W-L','Rank','GB','Win','Loss','Save','Time','D/N','Attendance','cLI','Streak','Orig. Scheduled']]

neutral_site_games = [
    ('2026-09-27', 'BOS'),
    ('2026-08-13', 'MIN'),
    ('2026-08-23', 'MIL'),
    ('2026-06-08', 'ATH'),
    ('2026-06-09', 'ATH'),
    ('2026-06-10', 'ATH'),
    ('2026-06-12', 'ATH'),
    ('2026-06-13', 'ATH'),
    ('2026-06-14', 'ATH'),
]

key = pd.MultiIndex.from_frame(games[['Date', 'home']])
games['neutral_site'] = key.isin(neutral_site_games)
games = games[~games['neutral_site']]
print('2026 MLB games dataset:')
print(games)

#define ballpark capacities
ballpark_capacities = {
    'ARI': 48330,
    'ATH': 10624,
    'ATL': 41084,
    'BAL': 44487,
    'BOS': 37755,
    'CHC': 41000,
    'CHW': 40615,
    'CIN': 43500,
    'CLE': 34820,
    'COL': 46897,
    'DET': 41083,
    'HOU': 41168,
    'KCR': 37903,
    'LAA': 45517,
    'LAD': 56000,
    'MIA': 37000,
    'MIL': 41900,
    'MIN': 38544,
    'NYM': 41922,
    'NYY': 46537,
    'PHI': 42901,
    'PIT': 38747,
    'SDP': 39860,
    'SEA': 47368,
    'SFG': 41331,
    'STL': 44383,
    'TBR': 42735,
    'TEX': 40300,
    'TOR': 39150,
    'WSN': 41373,}

#define home norms
home_team_attendance_norms = games.groupby('home')['Attendance'].agg(['mean','std','min','max']).reset_index()
home_team_attendance_norms['capacity'] = home_team_attendance_norms['home'].map(ballpark_capacities)
home_team_attendance_norms['pct_capacity'] = home_team_attendance_norms['mean'] / home_team_attendance_norms['capacity']
print('Attendance norms for home teams:')
print(home_team_attendance_norms.sort_values(by='pct_capacity', ascending=False))

#define road norms
road_team_attendance_norms = games.groupby('away')['Attendance'].agg(['mean','std','min','max']).reset_index()
print('Attendance norms for road teams:')
print(road_team_attendance_norms.sort_values(by='mean', ascending=False))

#matchup attendance splits
matchup_attendance_splits = games.groupby(['home','away'])['Attendance'].agg(['count','mean','std','min','max']).reset_index()
print('Attendance splits by matchup:')
print(matchup_attendance_splits.sort_values(by='mean', ascending=False))

#merged df for delta between matchup attendance and home team attendance norms
home_norms_x_matchup = pd.merge(matchup_attendance_splits, home_team_attendance_norms, on='home', how='inner', suffixes=('_matchup','_home_norm'))
home_norms_x_matchup['delta_vs_home_norm'] = home_norms_x_matchup['mean_matchup'] - home_norms_x_matchup['mean_home_norm']
home_norms_x_matchup.drop(columns=['std_matchup','min_matchup','max_matchup','std_home_norm','min_home_norm','max_home_norm'], inplace=True)
home_norms_x_matchup.rename(columns={'pct_capacity':'pct_capcity_home_norm'}, inplace=True)

print('Attendance splits by matchup with home team attendance norms:')
print(home_norms_x_matchup.sort_values(by='delta_vs_home_norm', ascending=False))

# Filtering on just a specific team to see their lowest attended road games

road_team = input('Enter a road team (3-letter abbreviation): ').upper()
if road_team not in ballpark_capacities.keys():
    raise ValueError(f"This is not a valid 3-letter team abbreviation. Please enter a valid one from the following list: {list(ballpark_capacities.keys())}")
home_norms_x_matchup_filtered = home_norms_x_matchup[home_norms_x_matchup['away'] == road_team]
print(f"Attendance splits by matchup with home team attendance norms for {road_team}")
print(home_norms_x_matchup_filtered.sort_values(by='delta_vs_home_norm', ascending=True))