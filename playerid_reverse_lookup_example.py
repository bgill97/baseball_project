from pybaseball import playerid_reverse_lookup

# Example MLBAM IDs
mlbam_ids = [457705] 

# Reverse lookup using 'mlbam' as the key type
player_data = playerid_reverse_lookup(mlbam_ids, key_type='mlbam')
print(player_data)