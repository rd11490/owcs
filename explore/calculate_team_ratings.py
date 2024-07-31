import pandas as pd
from configs.EMEA_Config import emea_config_stage_2, emea_config_stage_1
from configs.NA_config import na_config_stage_1, na_config_stage_2
from explore.teams import ENCE, SPACESTATION, TORONTO_DEFIANT, M80, TWISTED_MINDS, SOG
from helpers.extract_team_data import scrape_all_teams
from helpers.file_names import build_source_dir
import math
import numpy as np

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)

groups = pd.read_csv('data/stage_2_groups.csv')
grouped_teams = groups['team_id'].unique()

match_file_emea = f'{build_source_dir(emea_config_stage_2["swiss"])}/player_stats.csv'
match_file_na = f'{build_source_dir(na_config_stage_2["swiss"])}/player_stats.csv'

teams_at_dallas = [ENCE, SPACESTATION, TORONTO_DEFIANT, M80, SOG]

player_stats_emea = pd.read_csv(match_file_emea)
player_stats_na = pd.read_csv(match_file_na)

player_stats = pd.concat([player_stats_emea, player_stats_na])

player_stats = player_stats[player_stats['team_id'].isin(grouped_teams)]

swiss_ids = [emea_config_stage_2['swiss']['id'], na_config_stage_2['swiss']['id']]

maps_played = player_stats[~player_stats['competition_id'].isin(swiss_ids)][
    ['player_id', 'player_nickname', 'team_id', 'map_id']].groupby(
    ['team_id', 'player_id', 'player_nickname']).count().reset_index()

groups = groups.merge(maps_played, on=['player_id', 'team_id'])
groups = groups[['player_id', 'team_id', 'team_name', 'ign', 'map_id']]

mwa = pd.read_csv('data/mwa.csv')
mwa = mwa[['player_id', 'mwa', 'mwa stdev']]
groups_with_score = groups.merge(mwa, on=['player_id'])


def stdev_agg(series):
    squared_sum = (series ** 2).sum()  # Square all values and sum them
    result = np.sqrt(squared_sum)  # Take the square root of the total
    return result


groups_with_score = groups_with_score.groupby('team_id').apply(lambda x: x.nlargest(5, 'map_id')).reset_index(drop=True)
print(groups_with_score)

groups_with_score = groups_with_score.groupby(['team_id', 'team_name'])[['mwa', 'mwa stdev']].agg(
    {'mwa': 'sum', 'mwa stdev': 'sum'}).reset_index()
groups_with_score = groups_with_score.sort_values(by='mwa', ascending=False)
groups_with_score = groups_with_score[groups_with_score['team_id'].isin(teams_at_dallas)]
manual_teams = [
    {
        'team_id': '1',
        'team_name': 'Falcons',
        'mwa': 1.3,
        'mwa stdev': .3
    }, {
        'team_id': '2',
        'team_name': 'Crazy Racoons',
        'mwa': 1.3,
        'mwa stdev': .3
    },
    {
        'team_id': TWISTED_MINDS,
        'team_name': 'Twisted Minds',
        'mwa': 0.375493875959065,
        'mwa stdev': .13
    }
]
manual_teams_df = pd.DataFrame(manual_teams)
groups_with_score = pd.concat([groups_with_score, manual_teams_df])
groups_with_score = groups_with_score.sort_values(by='mwa', ascending=False)

print(groups_with_score)

groups_with_score.to_csv('data/team_mwa.csv', index=False)
