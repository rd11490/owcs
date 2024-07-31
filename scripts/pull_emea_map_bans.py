from configs.EMEA_Config import emea_config_stage_1, emea_config_stage_2
from helpers.file_path import get_file_path
from processors.pull_map_bans import pull_map_bans
import pandas as pd

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)


path = get_file_path(__file__)

# pull_map_bans(emea_config_stage_1['swiss'])
# pull_map_bans(emea_config_stage_1['group_a'])
# pull_map_bans(emea_config_stage_1['group_b'])
# pull_map_bans(emea_config_stage_1['group_c'])
# pull_map_bans(emea_config_stage_1['group_d'])
# pull_map_bans(emea_config_stage_1['main_event'])
pull_map_bans(emea_config_stage_2['swiss'])
