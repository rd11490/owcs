from services.facit_api import pull_teams
import pandas as pd


def get_teams(jsn):
    return jsn.get('payload', {}).get('items', [])


def is_team_stable(team):
    return team.get('team', {}).get('status') == 'STABLE'


def get_members(team):
    return team.get('team', {}).get('members', [])


def get_member_name(member):
    return member.get('nickname')


def get_member_id(member):
    return member.get('id')


def get_member_ign(member):
    games = member.get('games', [])
    for g in games:
        if g.get('game') == 'ow2':
            return g.get('userGameName')
    return None


def get_member_info(member):
    return {
        'name': get_member_name(member),
        'ign': get_member_ign(member),
        'player_id': get_member_id(member)
    }


def get_event(team):
    event = team.get('championship', {})
    return {
        'event_id': event.get('id'),
        'event_name': event.get('name')
    }


def merge_player_with_team_and_event(member, event, team_id, team_name):
    return {
        **member,
        **event,
        'team_id': team_id,
        'team_name': team_name
    }


def extract_team_info(team):
    members = get_members(team)
    event = get_event(team)
    coach_ids = team.get('coaches', [])
    starters = team.get('roster', [])
    subs = team.get('substitutes', [])
    player_ids = starters + subs
    team_id = team.get('team', {}).get('id')
    team_name = team.get('team', {}).get('name')
    players = [get_member_info(member) for member in members if member.get('id') in player_ids]
    coaches = [get_member_info(member) for member in members if member.get('id') in coach_ids]

    team = {
        'team_id': team_id,
        'team_name': team_name,
        'teamSize': len(members),
        'players': players,
        'coaches': coaches,
        **event
    }

    players_arr = [merge_player_with_team_and_event(member, event, team_id, team_name) for member in players]
    coaches_arr = [merge_player_with_team_and_event(member, event, team_id, team_name) for member in coaches]
    return team, players_arr, coaches_arr


def scrape_all_teams(stage_id):
    team_info = []
    player_info = []
    coach_info = []
    keep_going = True
    offset = 0
    limit = 20
    while keep_going:
        jsn = pull_teams(stage_id, offset, limit)

        teams = get_teams(jsn)
        if len(teams) > 0:
            for t in teams:
                team_data, players, coaches = extract_team_info(t)
                team_info.append(team_data)
                player_info = player_info + players
                coach_info = coach_info + coaches
            offset = offset + limit
        else:
            keep_going = False

        print(f'Offset: {offset}')
        print(f'Teams Pulled: {len(team_info)}')

    team_df = pd.DataFrame(team_info)
    player_df = pd.DataFrame(player_info)
    coach_df = pd.DataFrame(coach_info)
    return team_df, player_df, coach_df
