import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils import game_outcomes

#initialization
games = game_outcomes(2026)
games.reset_index(drop=True, inplace=True)

#convert CLI to foat
games['cLI'] = games['cLI'].astype(float)

#only keep home games
games = games[games['Home_Away'] == 'Home'].copy()

#refactor df for home and away teams
games = games.rename(columns={'Tm': 'home', 'Opp': 'away'})
games = games.drop(columns=['Home_Away','W/L','R','RA','Inn','Win','Loss','Save','Time','Orig. Scheduled'])


#reorder columns horizontally and vertically
cols = ['away','home','date','game_num'] + [col for col in games.columns if col not in ['away','home','date','game_num']]
games = games[cols].sort_values(['date', 'game_num']).reset_index(drop=True)

print(games)

for team in games['home'].unique():
    team_home_games = games[games['home'] == team]
    team_home_games.reset_index(drop=True, inplace=True)
    print(team_home_games.sort_values(by='date', ascending=True))
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=team_home_games['cLI'],
            y=team_home_games['Attendance'],
            mode='markers',
            customdata=team_home_games[["date", "away"]].to_numpy(),
            hovertemplate=(
            '<b>X:</b> %{x}<br>'
            '<b>Y:</b> %{y}<br>'
            '<b>Date:</b> %{customdata[0]}<br>'
            '<b>Opponent:</b> %{customdata[1]}'
            '<extra></extra>'
        ),))
    fig.update_layout(title=f"Attendance x Championship Leverage Index for {team} in 2026", xaxis_title='Championship Leverage Index', yaxis_title='Home Attendance',font=dict(size=18))
    fig.update_layout(yaxis_rangemode='tozero')
    fig.show()