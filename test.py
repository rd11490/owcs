
import pandas as pd
import requests
import json

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)

headers = {
    'authority': 'api.faceit.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'Bearer 564520cf-531e-4443-8893-ca30259bfa2c',
    'faceit-referer': 'new-frontend',
    'origin': 'https://www.faceit.com',
    'referer': 'https://www.faceit.com/',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
}

facit_league_id = '88c7f7ec-4cb8-44d3-a5db-6e808639c232'
season_1_id = '11a95632-c1c6-4835-8ea3-64edcd1708d6'
na_regoin_id = '27b7d979-c6f0-4157-b518-edc260114384'
masters_division_id = '9c935555-f240-4fcd-ab54-cd354978270e'
stage_1_id = '1833d7df-92b9-4021-adfc-e9cf46217ee9'
conference_id = '08411b19-16c4-4eb9-8308-27de3a1904e1'

json_data = {
    'filterBy': {
        'leagueId': facit_league_id,
        'seasonId': season_1_id,
        'regionId': na_regoin_id,
        'divisionId': masters_division_id,
        'stageId': stage_1_id,
    },
    'searchString': '',
    'gameName': 'ow2',
    'offset': 0,
    'limit': 100,
}

response = requests.post(
    'https://www.faceit.com/api/team-leagues/v1/get_teams_by_search',
    headers=headers,
    json=json_data,
)
resp_json = response.json()

teams = resp_json.get('payload', {}).get('teams', [])

team_ids = [t.get('premade_team_id') for t in teams]

json_data = {
    'ids': team_ids
}

response = requests.post('https://www.faceit.com/api/teams/v3/teams/batch-get', headers=headers, json=json_data)

print(json.dumps(response.json()))


