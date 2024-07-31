import requests

headers = {
    'authority': 'api.faceit.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'Bearer ba6944f0-eb6b-487a-af4f-5b4a2658d66a',
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

def check_response(response):
    status = response.status_code
    if status < 200 or status >= 300:
        try:
            print(response.status_code)
            print(response.json())
        except:
            print('Failed to print')
        return False
    return True


def pull_teams(stage_id, offset=0, limit=20):
    params = {
        'limit': limit,
        'offset': offset,
    }

    response = requests.get(
        f'https://api.faceit.com/championships/v1/championship/{stage_id}/subscription',
        params=params,
        headers=headers,
    )

    if check_response(response):
        return response.json()
    return None


def pull_matches_swiss(stage_id, offset=0, limit=20):
    params = {
        'entityId': stage_id,
        'entityType': 'championship',
        'group': '1',
        'offset': offset,
        'limit': limit,
    }

    response = requests.get('https://api.faceit.com/match/v3/match', params=params, headers=headers)
    if check_response(response):
        return response.json()
    return None


def pull_match_data(match_id):
    response = requests.get(f'https://api.faceit.com/match/v2/match/{match_id}', headers=headers)
    if check_response(response):
        return response.json()
    return None


def pull_player_stats(match_id):
    response = requests.get(f'https://api.faceit.com/stats/v1/stats/matches/{match_id}', headers=headers)
    if check_response(response):
        return response.json()
    return None

def pull_stat_mapping():
    response = requests.get('https://api.faceit.com/stats/v1/stats/configuration/ow2', headers=headers)
    if check_response(response):
        return response.json()
    return None

def pull_map_voting(match_id):
    response = requests.get(f'https://www.faceit.com/api/democracy/v1/match/{match_id}/history', headers=headers)
    if check_response(response):
        return response.json()
    return None