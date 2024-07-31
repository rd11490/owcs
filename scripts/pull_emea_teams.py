import pandas as pd

from configs.EMEA_Config import emea_config_stage_1, emea_config_stage_2, emea_config_faceit_stage_1
from processors.pull_teams import pull_team_data

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)


# pull_team_data(emea_config_stage_1['swiss'])
# pull_team_data(emea_config_stage_2['swiss'])
pull_team_data(emea_config_faceit_stage_1['round_robin'])


