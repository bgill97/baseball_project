import matplotlib.pyplot as plt

from utils import atbat_outcomes
from pybaseball import spraychart

atbat_outcomes = atbat_outcomes('2026-03-26', '2026-09-28')

home_teams = atbat_outcomes['home_team'].unique()

team_dict = {
    'ATH': 'athletics',
    'AZ': 'diamondbacks',
    'ATL': 'braves',
    'BAL': 'orioles',
    'BOS': 'red_sox',
    'CHC': 'cubs',
    'CIN': 'reds',
    'CLE': 'indians',
    'COL': 'rockies',
    'CWS': 'white_sox',
    'DET': 'tigers',
    'HOU': 'astros',
    'KC': 'royals',
    'LAA': 'angels',
    'LAD': 'dodgers',
    'MIA': 'marlins',
    'MIL': 'brewers',
    'MIN': 'twins',
    'NYM': 'mets',
    'NYY': 'yankees',
    'PHI': 'phillies',
    'PIT': 'pirates',
    'SD': 'padres',
    'SEA': 'mariners',
    'SF': 'giants',
    'STL': 'cardinals',
    'TB': 'rays',
    'TEX': 'rangers',
    'TOR': 'blue_jays',
    'WSH': 'nationals'}



# for home_team in home_teams:
#     team_name = team_dict.get(home_team)
#     if team_name is None:
#         print(f"No data found for home team: {home_team}")
#         continue
#     triples_at_home = atbat_outcomes[(atbat_outcomes['home_team'] == home_team) & (atbat_outcomes['events'] == 'triple')]
#     try:
#         spraychart(triples_at_home, team_name, title=f'All 2026 Triples at the {team_name} stadium')
#     except IndexError:
#         print(f"No triples found for home team: {home_team}")
#         continue

atbat_outcomes['3B'] = atbat_outcomes['events'].isin(['triple']).astype(int)

grouped = atbat_outcomes.groupby('home_team', as_index=False).agg({'events':'count', '3B':'sum'})
grouped.reset_index(drop=True,inplace=True)
grouped['triples_percentage'] = grouped['3B'] / grouped['events'] * 100
grouped.rename(columns={"events":"plate_appearances", "3B":"triples"}, inplace=True)
grouped.sort_values(by='triples_percentage', ascending=False, inplace=True)
print(grouped)

grouped.plot.bar(x='home_team',y='triples_percentage',rot=90, title='Triples Percentage by Stadium in 2026', legend=False,colormap='viridis')
plt.ylabel('Triples Percentage')
plt.xlabel('Home Stadium')
plt.show()