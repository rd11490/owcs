from helpers.extract_match_list_data import scrape_all_matches
from helpers.file_names import matches_file
from helpers.file_path import get_file_path, create_dir_if_not_exists, prep_dir
import pandas as pd

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)


def pull_matches(config):
    comp_id = config['id']
    matches = scrape_all_matches(comp_id)

    prep_dir(config)
    if not matches.empty:
        matches.to_csv(matches_file(config), index=False)
