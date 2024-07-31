import pandas as pd

from helpers.extract_match_data import pull_and_extract_match_data
from helpers.extract_unique_match_ids import extract_unique_match_ids
from helpers.file_names import matches_file, match_results_file, match_results_failed_ids_file
import time

from helpers.pandas_extended import read_csv_if_exists, delete_if_exists

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)


def pull_match_results(config):
    match_df = read_csv_if_exists(matches_file(config))
    match_ids = list(match_df['match_id'].unique())
    print(f'Total Matches: {len(match_ids)}')

    completed_ids, completed_maps = extract_unique_match_ids(match_results_file(config))
    failed_ids_from_past, _ = extract_unique_match_ids(match_results_failed_ids_file(config))

    print(f'Completed Matches: {len(completed_ids)}')
    print(f'Failed Matches: {len(failed_ids_from_past)}')

    match_ids = list(set([m_id for m_id in match_ids if m_id not in completed_ids] + failed_ids_from_past))
    print(f'Matches to pull: {len(match_ids)}')
    match_results = []
    failed_ids = []
    match_id = None
    try:
        for i, match_id in enumerate(match_ids):
            print(f'Match: {i} - {match_id}')
            match_maps = pull_and_extract_match_data(match_id)
            if match_maps is None:
                failed_ids.append({'match_id': match_id})
            else:
                match_results = match_results + match_maps
            print(f'failed_ids: {len(failed_ids)}')
            print(f'Matches pulled: {len(match_results)}')
            time.sleep(1)
    except:
        if match_id is not None:
            failed_ids.append({'match_id': match_id})

    match_results_df = pd.DataFrame(match_results)
    if completed_maps is not None:
        match_results_df = pd.concat([match_results_df, completed_maps])
    match_results_df.drop_duplicates()
    if not match_results_df.empty:
        match_results_df.to_csv(match_results_file(config), index=False)

    if len(failed_ids) > 0:
        failed_ids_df = pd.DataFrame(failed_ids)
        failed_ids_df.drop_duplicates()
        if not failed_ids_df.empty:
            failed_ids_df.to_csv(match_results_failed_ids_file(config), index=False)
    else:
        delete_if_exists(match_results_failed_ids_file(config))
    print(match_results_df)
