#best batters against each pitch type

from pybaseball import statcast, playerid_lookup, cache, statcast_batter,playerid_reverse_lookup
from pybaseball.playerid_lookup import get_lookup_table
from utils import get_players_played_in_year
import pandas as pd

cache.enable()

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

#get all players who played in 2026
everyone_df = get_players_played_in_year(2026)

atbat_outcomes = statcast('2026-03-26', '2026-09-28')
atbat_outcomes.reset_index(drop=True,inplace=True)
atbat_outcomes.dropna(subset=['events'], inplace=True)

atbat_outcomes = atbat_outcomes.dropna(subset=['pitch_name'])

atbat_outcomes = atbat_outcomes[['pitch_name','game_date','release_speed','batter','pitcher','events','description']].copy()

atbat_outcomes = pd.merge(atbat_outcomes, everyone_df, left_on='pitcher', right_on='key_mlbam', how='left')
atbat_outcomes['pitcher_name'] = atbat_outcomes['name_first'] + ' ' + atbat_outcomes['name_last']
atbat_outcomes = atbat_outcomes.drop(columns=['pitcher','key_mlbam','key_retro','key_bbref','key_fangraphs','mlb_played_first','mlb_played_last','name_first','name_last'])
atbat_outcomes = pd.merge(atbat_outcomes, everyone_df, left_on='batter', right_on='key_mlbam', how='left')
atbat_outcomes['batter_name'] = atbat_outcomes['name_first'] + ' ' + atbat_outcomes['name_last']
atbat_outcomes = atbat_outcomes.drop(columns=['batter','key_mlbam','key_retro','key_bbref','key_fangraphs','mlb_played_first','mlb_played_last','name_first','name_last'])


ev = atbat_outcomes['events']
atbat_outcomes['H'] = ev.isin(['single','double','triple','home_run']).astype(int)
atbat_outcomes['BB'] = ev.isin(['walk','intent_walk']).astype(int)
atbat_outcomes['HBP'] = ev.isin(['hit_by_pitch']).astype(int)
atbat_outcomes['SF']  = ev.isin(['sac_fly', 'sac_fly_double_play']).astype(int)
atbat_outcomes['K'] = ev.isin(['strikeout','strikeout_double_play']).astype(int)

non_ab = ev.isin(['walk', 'intent_walk', 'hit_by_pitch', 'sac_fly', 'sac_fly_double_play',
                  'sac_bunt', 'sac_bunt_double_play', 'catcher_interf'])
atbat_outcomes['AB'] = (~non_ab).astype(int)
atbat_outcomes['TB'] = ev.map({'single': 1, 'double': 2, 'triple': 3, 'home_run': 4}).fillna(0).astype(int)

pitch_types = atbat_outcomes['pitch_name'].unique()


for pitch_type in pitch_types:

    #filter for the current pitch type
    atbat_outcomes_pitch_type = atbat_outcomes[atbat_outcomes['pitch_name'] == pitch_type]


    grouped = atbat_outcomes_pitch_type.groupby('batter_name').agg({'H':'sum','BB':'sum','HBP':'sum','K':'sum','SF':'sum','AB':'sum','TB':'sum'})

    #define aggregations for each column
    grouped['AVG'] = grouped['H'] / grouped['AB']
    grouped['OBP'] = (grouped['H'] + grouped['BB'] + grouped['HBP'])/(grouped['AB'] + grouped['BB'] + grouped['HBP'] + grouped['SF'])
    grouped['SLG'] = grouped['TB'] / grouped['AB']
    grouped['OPS'] = grouped['OBP'] + grouped['SLG']

    #filter based on minimum at bats for each pitch type
    min_ab = 50 if pitch_type in ['4-Seam Fastball', 'Sinker', 'Slider', 'Changeup', 'Sweeper' , 'Cutter', 'Curveball', 'Split-Finger', 'Knuckle Curve'] else 5
    grouped = grouped[grouped['AB'] >= min_ab]


    print(f"Best batters against {pitch_type}:")
    print(grouped.sort_values(by='OPS', ascending=False).head(10))
