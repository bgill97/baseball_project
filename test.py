import pybaseball, os, pandas as pd

path = os.path.join(os.path.dirname(pybaseball.__file__), 'data', 'mlbstadiums.csv')
print(sorted(pd.read_csv(path)['team'].unique()))