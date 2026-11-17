from pybaseball import schedule_and_record

# Game-by-game results from the Yankees' 1927 season
data = schedule_and_record(1927, "NYY")

# Results and upcoming schedule for the Phillies' current season (2017 at the time of writing)
data = schedule_and_record(2017, "PHI")
print(data)