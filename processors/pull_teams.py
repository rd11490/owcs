import pandas as pd

from helpers.extract_team_data import scrape_all_teams
from helpers.file_names import teams_file, players_file, coaches_file
from helpers.file_path import get_file_path, prep_dir

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)


def pull_team_data(config):
    comp_id = config['id']

    teams, players, coaches = scrape_all_teams(comp_id)
    prep_dir(config)

    teams.to_csv(teams_file(config), index=False)
    players.to_csv(players_file(config), index=False)
    coaches.to_csv(coaches_file(config), index=False)

