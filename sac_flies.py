#Spray chart for sac flies in 2026 for each team at their home stadium

from pybaseball import statcast_batter, spraychart, plot_teams, team_batting, statcast


data = statcast('2026-03-26', '2026-09-28')
data.dropna(subset=['events'], inplace=True)

home_teams = data['home_team'].unique()

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

for home_team in home_teams:
    team_name = team_dict.get(home_team)
    if team_name is None:
        print(f"No data found for home team: {home_team}")
        continue
    sac_flies = data[(data['home_team'] == home_team) & (data['events'] == 'sac_fly')]
    try:
        spraychart(sac_flies, team_dict.get(home_team), title=f'All 2026 Sac Flies at the {team_dict.get(home_team)} stadium')
    except IndexError:
        print(f"No sac flies found for home team: {home_team}")
        continue

# data = team_batting(2023)

# plot_teams(data, "HR", "BB")

#events = sac_fly
#triple
