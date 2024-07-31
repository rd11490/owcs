from configs.EMEA_Config import emea_config_stage_1, emea_config_stage_2, emea_config_faceit_stage_1
from helpers.file_path import get_file_path
from processors.pull_matches import pull_matches
import pandas as pd

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)


# pull_matches(emea_config_stage_1['swiss'])
# pull_matches(emea_config_stage_1['group_a'])
# pull_matches(emea_config_stage_1['group_b'])
# pull_matches(emea_config_stage_1['group_c'])
# pull_matches(emea_config_stage_1['group_d'])
# pull_matches(emea_config_stage_1['main_event'])
# pull_matches(emea_config_stage_2['swiss'])
# pull_matches(emea_config_stage_2['group_a'])
# pull_matches(emea_config_stage_2['group_b'])
# pull_matches(emea_config_stage_2['group_c'])
# pull_matches(emea_config_stage_2['group_d'])
# pull_matches(emea_config_stage_2['main_event'])
pull_matches(emea_config_faceit_stage_1['round_robin'])





