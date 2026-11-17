import requests
import pandas as pd
import json

#{"springLeague":{"id":115,"name":"Grapefruit League","link":"/api/v1/league/115","abbreviation":"GL"},"allStarStatus":"N","id":111,"name":"Boston Red Sox","link":"/api/v1/teams/111","season":2026,"venue":{"id":3,"name":"Fenway Park","link":"/api/v1/venues/3"},"springVenue":{"id":4309,"link":"/api/v1/venues/4309"},"teamCode":"bos","fileCode":"bos","abbreviation":"BOS","teamName":"Red Sox","locationName":"Boston","firstYearOfPlay":"1901","league":{"id":103,"name":"American League","link":"/api/v1/league/103"},"division":{"id":201,"name":"American League East","link":"/api/v1/divisions/201"},"sport":{"id":1,"link":"/api/v1/sports/1","name":"Major League Baseball"},"shortName":"Boston","franchiseName":"Boston","clubName":"Red Sox","active":True}

team_info_url = 'https://statsapi.mlb.com/api/v1/teams?sportId=1'
team_info_response = requests.get(team_info_url, timeout=10)
team_info_dict = team_info_response.json()
#print(team_info_dict)

dict_fields = ['id','abbreviation']
team_ids = {team['abbreviation']: team['id'] for team in team_info_dict['teams']}

print("Team IDs:")
print(team_ids)

def team_triples(team_id, year):
    url = f"https://statsapi.mlb.com/api/v1/teams/{team_id}/stats"
    params = {"stats": "season", "group": "hitting", "season": year}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()["stats"][0]["splits"][0]["stat"]["triples"]

appended_data = []

for team in ['ATH','BOS']:
    for y in range(2000,2027):
        rows = [{team, y, team_triples(team_ids.get(team), y)}]
        appended_data.append(rows)
        print(appended_data)
appended_data = pd.DataFrame(appended_data)
print(appended_data)

#need to iterate through all teams and years to get a full dataset of triples by year and team