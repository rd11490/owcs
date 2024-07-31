import pandas as pd

from helpers.build_mapping_keys import build_mapping_keys
from helpers.extract_match_stats import pull_and_extract_match_stats
from helpers.extract_unique_match_ids import extract_unique_match_ids
from helpers.file_names import matches_file, team_stats_file, player_stats_file, stats_failed_ids_file
import time

from helpers.pandas_extended import read_csv_if_exists, delete_if_exists

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)


def pull_match_stats(config):
    match_df = read_csv_if_exists(matches_file(config))
    match_ids = list(match_df['match_id'].unique())
    print(f'Total Matches: {len(match_ids)}')

    completed_team_match_ids, completed_team_stats = extract_unique_match_ids(team_stats_file(config))
    completed_player_match_ids, completed_player_stats = extract_unique_match_ids(player_stats_file(config))
    completed_ids = list(set(completed_team_match_ids + completed_player_match_ids))
    print(f'Completed Matches: {len(completed_ids)}')

    failed_ids_from_past, _ = extract_unique_match_ids(stats_failed_ids_file(config))

    print(f'Failed Matches: {len(failed_ids_from_past)}')

    match_ids = list(set([m_id for m_id in match_ids if m_id not in completed_ids] + failed_ids_from_past))
    print(f'Matches to pull: {len(match_ids)}')

    mapping_keys, map_info = build_mapping_keys()

    all_player_stats = []
    all_team_stats = []

    failed_ids = []
    match_id = None
    try:
        for i, match_id in enumerate(match_ids):
            print(f'Match: {i} - {match_id}')
            result = pull_and_extract_match_stats(match_id, map_info)
            if result is None:
                failed_ids.append({'match_id': match_id})
            else:
                player_stats, team_stats = result
                all_player_stats = all_player_stats + player_stats
                all_team_stats = all_team_stats + team_stats

            print(f'failed_ids: {len(failed_ids)}')
            print(f'maps pulled: {len(all_team_stats)}')
            time.sleep(1)
    except:
        if match_id is not None:
            failed_ids.append({'match_id': match_id})

    team_stats_df = pd.DataFrame(all_team_stats)
    if completed_team_stats is not None:
        team_stats_df = pd.concat([team_stats_df, completed_team_stats])
    team_stats_df.drop_duplicates()
    team_stats_df.to_csv(team_stats_file(config), index=False)

    player_stats_df = pd.DataFrame(all_player_stats)
    if completed_player_stats is not None:
        player_stats_df = pd.concat([player_stats_df, completed_player_stats])
    player_stats_df.drop_duplicates()
    if not player_stats_df.empty:
        player_stats_df.to_csv(player_stats_file(config), index=False)

    if len(failed_ids) > 0:
        failed_ids_df = pd.DataFrame(failed_ids)
        failed_ids_df.drop_duplicates()
        if not failed_ids_df.empty:
            failed_ids_df.to_csv(stats_failed_ids_file(config), index=False)
    else:
        delete_if_exists(stats_failed_ids_file(config))

    print(team_stats_df)
    print(player_stats_df)
