import plotly.graph_objects as go

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
atbat_outcomes['HR'] = atbat_outcomes['events'].isin(['home_run']).astype(int)

grouped = atbat_outcomes.groupby('home_team', as_index=False).agg({'events':'count', '3B':'sum', 'HR':'sum'})
grouped.reset_index(drop=True,inplace=True)
grouped['triples_percentage'] = grouped['3B'] / grouped['events'] * 100
grouped['homers_percentage'] = grouped['HR'] / grouped['events'] * 100
grouped.rename(columns={"events":"plate_appearances", "3B":"triples", "HR":"home runs"}, inplace=True)
print(grouped)

fig = go.Figure()
fig.add_trace(go.Scatter(x=grouped['triples_percentage'], y=grouped['homers_percentage'], mode='text', text=grouped['home_team'], textposition='top center'))
fig.update_layout(title='Triple Percentage x Home Run Percentage by Stadium in 2026', xaxis_title='Triple Percentage', yaxis_title='Home Run Percentage',font=dict(size=18))
fig.show()