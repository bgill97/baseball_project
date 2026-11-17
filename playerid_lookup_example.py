from pybaseball import playerid_lookup

# find the ids of all players with last name Jones (returns 1,314 rows)
data = playerid_lookup('jones')

# only return the ids of chipper jones (returns one row)
data = playerid_lookup('jones','chipper')

# Will return all players named Pedro Martinez (returns *2* rows)
data = playerid_lookup("martinez", "pedro", fuzzy=True)

# Will return the 5 closest names to "yadi molina" (returns 5 rows)
# First row will be Yadier Molina
data = playerid_lookup("molina", "yadi", fuzzy=True)