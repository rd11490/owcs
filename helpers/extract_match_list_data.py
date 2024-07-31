from helpers.general_utils import parse_event
from services.facit_api import pull_matches_swiss
import pandas as pd
import time

def parse_teams(teams):
    return {
        'team1_id': teams.get('faction1', {}).get('id'),
        'team1_name': teams.get('faction1', {}).get('name'),
        'team2_id': teams.get('faction2', {}).get('id'),
        'team2_name': teams.get('faction2', {}).get('name'),
    }



def parse_match(match_jsn):
    match_id = match_jsn.get('id')
    teams = parse_teams(match_jsn.get('teams'))
    event = parse_event(match_jsn)
    return {
        'match_id': match_id,
        **teams,
        **event
    }


def scrape_all_matches(stage_id):
    match_list = []
    keep_going = True
    offset = 0
    limit = 20
    while keep_going:
        jsn = pull_matches_swiss(stage_id, offset, limit)

        matches = jsn.get('payload', [])
        if len(matches) > 0:
            for match in matches:
                match_data = parse_match(match)
                match_list.append(match_data)
            offset = offset + limit
        else:
            keep_going = False

        print(f'Offset: {offset}')
        print(f'Matches Pulled: {len(match_list)}')
        time.sleep(.5)

    match_df = pd.DataFrame(match_list)

    return match_df