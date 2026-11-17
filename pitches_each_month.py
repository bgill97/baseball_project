#Are pitchces getting slower as the year progresses? Are certain pitches being thrown more?

from utils import get_players_played_in_year, all_pitches
import pandas as pd


everyone_df = get_players_played_in_year(2026)

all_pitches_df = all_pitches('2026-03-26', '2026-09-28')

all_pitches_df = all_pitches_df[['pitch_name','game_date','release_speed','batter','pitcher']].copy()

all_pitches_df['game_month'] = pd.to_datetime(all_pitches_df['game_date']).dt.month

pitch_types = all_pitches_df['pitch_name'].unique()

for pitch_type in pitch_types:
    all_pitches_pitch_type = all_pitches_df[all_pitches_df['pitch_name'] == pitch_type]

    grouped = all_pitches_pitch_type.groupby('game_month').agg({'release_speed': ['mean','count']}).reset_index()

    print(f"Average release speed for {pitch_type} by month:")
    print(grouped[['game_month', 'release_speed']])

print('End of script.')