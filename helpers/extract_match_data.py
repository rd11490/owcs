from helpers.general_utils import parse_event
from services.facit_api import pull_match_data


def extract_map_list(match):
    maps = match.get('maps', [])
    map_dict = {}
    for map_info in maps:
        map_dict[map_info.get('game_map_id')] = map_info.get('name')
    return map_dict


def extract_maps_played(match, map_dict):
    map_picks = match.get('voting', {}).get('map', {}).get('pick', [])
    out = []
    for i, pick in enumerate(map_picks):
        out.append({
            'map_id': pick,
            'map_name': map_dict[pick],
            'map_number': i
        })
    return out


def extrat_teams(match):
    teams = match.get('teams', {})
    return {
        'team1_id': teams.get('faction1', {}).get('id'),
        'team1_name': teams.get('faction1', {}).get('name'),
        'team2_id': teams.get('faction2', {}).get('id'),
        'team2_name': teams.get('faction2', {}).get('name')
    }


def get_team_score(result, team_num):
    return result.get('factions', {}).get(f'faction{team_num}', {}).get('score', 0)


def get_result_players(result, team_num):
    players = result.get('factions', {}).get(f'faction{team_num}', {}).get('players', [])
    return [player.get('id') for player in players]


def extract_match_result(result):
    out = {
        'team1_score': get_team_score(result, 1),
        'team2_score': get_team_score(result, 2),
    }
    team_1_players = get_result_players(result, 1)
    team_2_players = get_result_players(result, 2)
    for i, p in enumerate(team_1_players):
        out[f'team1_player{i}'] = p

    for i, p in enumerate(team_2_players):
        out[f'team2_player{i}'] = p

    return out


def extract_results(match, maps_played):
    results = match.get('results', [])
    maps_with_results = zip(maps_played, results)
    teams = extrat_teams(match)
    out = []
    for map_played, result in maps_with_results:
        out.append({
            **map_played,
            **teams,
            **(extract_match_result(result))
        })
    return out


def extract_match_maps(match):
    payload = match.get('payload', {})
    match_id = payload.get('id')
    event = parse_event(payload)
    map_dict = extract_map_list(payload)

    maps_played = extract_maps_played(payload, map_dict)
    maps_played = [{**map_played, **event, 'match_id': match_id} for map_played in maps_played]
    results = extract_results(payload, maps_played)
    return results


def pull_and_extract_match_data(match_id):
    match_data = pull_match_data(match_id)
    if match_data is None:
        return None
    return extract_match_maps(match_data)
