import pandas as pd

from configs.NA_config import na_config_stage_1, na_config_stage_2, na_config_faceit_stage_1
from helpers.file_path import get_file_path
from processors.pull_teams import pull_team_data

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)

path = get_file_path(__file__)
#
# pull_team_data(na_config_stage_1['swiss'])
# pull_team_data(na_config_stage_1['swiss'])
pull_team_data(na_config_faceit_stage_1['round_robin'])

