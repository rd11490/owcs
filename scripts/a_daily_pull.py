from configs.EMEA_Config import emea_config_stage_2, emea_config_stage_1
from configs.NA_config import na_config_stage_1, na_config_stage_2
from helpers.file_path import get_file_path
from processors.pull_match_results import pull_match_results
from processors.pull_match_stats import pull_match_stats
from processors.pull_matches import pull_matches
import pandas as pd

from scripts.merge_all import merge_all

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)


path = get_file_path(__file__)


# pull_matches(na_config_stage_2['group_a'])
# pull_matches(na_config_stage_2['group_b'])
# pull_matches(na_config_stage_2['group_c'])
# pull_matches(na_config_stage_2['group_d'])
pull_matches(na_config_stage_2['main_event'])

# pull_match_results(na_config_stage_2['group_a'])
# pull_match_results(na_config_stage_2['group_b'])
# pull_match_results(na_config_stage_2['group_c'])
# pull_match_results(na_config_stage_2['group_d'])
pull_match_results(na_config_stage_2['main_event'])


# pull_match_stats(na_config_stage_2['group_a'])
# pull_match_stats(na_config_stage_2['group_b'])
# pull_match_stats(na_config_stage_2['group_c'])
# pull_match_stats(na_config_stage_2['group_d'])
pull_match_stats(na_config_stage_2['main_event'])


# pull_matches(emea_config_stage_2['group_a'])
# pull_matches(emea_config_stage_2['group_b'])
# pull_matches(emea_config_stage_2['group_c'])
# pull_matches(emea_config_stage_2['group_d'])
pull_matches(emea_config_stage_2['main_event'])


# pull_match_results(emea_config_stage_2['group_a'])
# pull_match_results(emea_config_stage_2['group_b'])
# pull_match_results(emea_config_stage_2['group_c'])
# pull_match_results(emea_config_stage_2['group_d'])
pull_match_results(emea_config_stage_2['main_event'])


# pull_match_stats(emea_config_stage_2['group_a'])
# pull_match_stats(emea_config_stage_2['group_b'])
# pull_match_stats(emea_config_stage_2['group_c'])
# pull_match_stats(emea_config_stage_2['group_d'])
pull_match_stats(emea_config_stage_2['main_event'])



merge_all(na_config_stage_1)
merge_all(na_config_stage_2)
merge_all(emea_config_stage_1)
merge_all(emea_config_stage_2)