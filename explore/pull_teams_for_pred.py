import pandas as pd
from configs.EMEA_Config import emea_config_stage_2, emea_config_stage_1
from configs.NA_config import na_config_stage_1, na_config_stage_2
from helpers.extract_team_data import scrape_all_teams
from helpers.file_names import build_source_dir

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)


def pull_teams(config):
    comp_id = config['id']

    teams, players, coaches = scrape_all_teams(comp_id)
    return players


emea_group_a = pull_teams(emea_config_stage_2['group_a'])
emea_group_b = pull_teams(emea_config_stage_2['group_b'])
emea_group_c = pull_teams(emea_config_stage_2['group_c'])
emea_group_d = pull_teams(emea_config_stage_2['group_d'])


na_group_a = pull_teams(na_config_stage_2['group_a'])
na_group_b = pull_teams(na_config_stage_2['group_b'])
na_group_c = pull_teams(na_config_stage_2['group_c'])
na_group_d = pull_teams(na_config_stage_2['group_d'])

groups = pd.concat([emea_group_a, emea_group_b, emea_group_c, emea_group_d, na_group_a, na_group_b, na_group_c, na_group_d])

groups.to_csv('data/stage_2_groups.csv', index=False)