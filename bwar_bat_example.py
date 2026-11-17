#advanced batting stats by player/year combination
from pybaseball import bwar_bat

# get war stats from baseball reference 
data = bwar_bat()

# get war stats plus additional fields from this table 
data = bwar_bat(return_all=True)
print(data)