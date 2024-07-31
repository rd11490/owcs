from helpers.build_mapping_keys import build_mapping_keys
from helpers.extract_unique_match_ids import extract_unique_match_ids
from helpers.file_names import matches_file, match_map_bans_file, match_map_bans_failed_ids_file
from helpers.pandas_extended import read_csv_if_exists, delete_if_exists
from services.facit_api import pull_map_voting
import pandas as pd
import time

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)

def pull_map_bans(config):
    mapping_keys, map_info = build_mapping_keys()

    match_df = read_csv_if_exists(matches_file(config))
    match_ids = list(match_df['match_id'].unique())
    print(f'Total Matches: {len(match_ids)}')

    completed_ids, completed_map_bans = extract_unique_match_ids(match_map_bans_file(config))
    failed_ids_from_past, _ = extract_unique_match_ids(match_map_bans_failed_ids_file(config))

    match_df['idx'] = match_df['match_id']
    match_info_dict = match_df.set_index('idx').to_dict(orient='index')

    print(f'Completed Matches: {len(completed_ids)}')
    print(f'Failed Matches: {len(failed_ids_from_past)}')

    match_ids = list(set([m_id for m_id in match_ids if m_id not in completed_ids] + failed_ids_from_past))
    print(f'Matches to pull: {len(match_ids)}')
    map_bans_results = []
    failed_ids = []
    match_id = None


    def extract_map_bans(competition_id, match_id, map_ban_data):
        tickets = map_ban_data['payload']['tickets']
        map_votes = []
        for ticket in tickets:
            if ticket['entity_type'] == 'map':
                votes = ticket['entities']
                for vote in votes:
                    map_id = vote['guid']
                    action = vote['status']
                    action_round = vote['round']
                    match_info = match_info_dict[match_id]
                    team1_id = match_info['team1_id']
                    team2_id = match_info['team2_id']
                    team1_name = match_info['team1_name']
                    team2_name = match_info['team2_name']
                    competition_name = match_info['event_name']

                    team_name = team1_name if vote['selected_by'] == 'faction1' else team2_name
                    team_id = team1_id if vote['selected_by'] == 'faction1' else team2_id

                    oppo_name = team1_name if vote['selected_by'] == 'faction2' else team2_name
                    oppo_id = team1_id if vote['selected_by'] == 'faction2' else team2_id
                    map_name = map_info[map_id]
                    map_votes.append({
                            "match_id": match_id,
                            "competition_id": competition_id,
                            "competition_name": competition_name,
                            "team_id": team_id,
                            "team_name": team_name,
                            "opponent_id": oppo_id,
                            "opponent_name": oppo_name,
                            "map_id": map_id,
                            "map_name": map_name,
                            "action": action,
                            "action_round": action_round
                    })
        return map_votes
    def pull_and_extract_map_bans(competition_id, match_id):
        map_ban_data = pull_map_voting(match_id)
        if map_ban_data is None:
            return None
        return extract_map_bans(competition_id, match_id, map_ban_data)

    competition_id = config['id']
    try:
        for i, match_id in enumerate(match_ids):
            print(f'Match: {i} - {match_id}')
            map_bans = pull_and_extract_map_bans(competition_id, match_id)
            if map_bans is None:
                failed_ids.append({'match_id': match_id})
            else:
                map_bans_results = map_bans_results + map_bans
            print(f'failed_ids: {len(failed_ids)}')
            print(f'Matches pulled: {len(map_bans_results)}')
            time.sleep(1)
    except:
        if match_id is not None:
            failed_ids.append({'match_id': match_id})


    map_bans_df = pd.DataFrame(map_bans_results)
    print(map_bans_df)

    if completed_map_bans is not None:
        map_bans_df = pd.concat([map_bans_df, completed_map_bans])
    map_bans_df.drop_duplicates()
    map_bans_df.to_csv(match_map_bans_file(config), index=False)

    if len(failed_ids) > 0:
        failed_ids_df = pd.DataFrame(failed_ids)
        failed_ids_df.drop_duplicates()
        failed_ids_df.to_csv(match_map_bans_failed_ids_file(config), index=False)
    else:
        delete_if_exists(match_map_bans_failed_ids_file(config))

    print(map_bans_df)
