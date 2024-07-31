import pandas as pd

from configs.EMEA_Config import emea_config_stage_2
from configs.NA_config import na_config_stage_2

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)

na_circuit_points = pd.read_csv('../data/NA/na_circuit_points.csv')
na_circuit_points = na_circuit_points[['playerId', 'points', 'teamId']]
na_circuit_points['region'] = 'NA'
na_circuit_points.columns = ['playerId', 'points', 'prevTeamId', 'region']

emea_circuit_points = pd.read_csv('../data/EMEA/emea_circuit_points.csv')
emea_circuit_points = emea_circuit_points[['playerId', 'points', 'teamId']]
emea_circuit_points['region'] = 'EMEA'
emea_circuit_points.columns = ['playerId', 'points', 'prevTeamId', 'region']

circuit_points = pd.concat([emea_circuit_points, na_circuit_points])
circuit_points['region'] = circuit_points['region'].astype(str)

stage_2_groups = pd.read_csv('data/stage_2_groups.csv')


def determine_region(str_val):
    if 'EMEA Stage 2' in str_val:
        return 'EMEA'
    else:
        return 'NA'


stage_2_groups['region'] = stage_2_groups['event_name'].apply(determine_region)
stage_2_groups['region'] = stage_2_groups['region'].astype(str)

stage_2_groups_with_points = stage_2_groups.merge(circuit_points, left_on=['player_id', 'region'], right_on=['playerId', 'region'], how='left')
stage_2_groups_with_points = stage_2_groups_with_points.fillna(0)

na_player_stats_file = f'../data/NA/owcs/stage_2/player_stats.csv'
emea_player_stats_file = f'../data/EMEA/owcs/stage_2/player_stats.csv'

na_player_stats = pd.read_csv(na_player_stats_file)
emea_player_states = pd.read_csv(emea_player_stats_file)

# filter sonne who shows up in both
na_player_stats = na_player_stats[na_player_stats['player_id'] != '955b333d-0104-487b-818e-79951d603905']

swiss_ids = [emea_config_stage_2['swiss']['id'], na_config_stage_2['swiss']['id']]

player_stats = pd.concat([na_player_stats, emea_player_states])

maps_played = player_stats[~player_stats['competition_id'].isin(swiss_ids)][['player_id', 'map_id']].groupby(
    ['player_id']).count().reset_index()[['player_id', 'map_id']]
stage_2_groups_with_points = stage_2_groups_with_points.merge(maps_played, on='player_id', how='left').fillna(0).rename(
    columns={'map_id': 'maps_played'})

stage_2_groups_with_points = stage_2_groups_with_points.sort_values(by=['region', 'team_id', 'points', 'maps_played'],
                                                                    ascending=False)


def determine_roles(roles):
    out = []
    modes = roles.mode()
    most_frequent_value = modes[0] if not modes.empty else None
    if most_frequent_value is not None:
        out.append(most_frequent_value)
    counts = roles.value_counts()
    items_more_than_3 = counts[counts > 5].index.tolist()
    return list(set(out + items_more_than_3))


roles = player_stats[['player_id', 'player_role']].groupby('player_id')['player_role'].agg(
    lambda x: determine_roles(x)).reset_index()
stage_2_groups_with_points = stage_2_groups_with_points.merge(roles, on='player_id', how='left')
stage_2_groups_with_points['player_role'] = stage_2_groups_with_points['player_role'].fillna(
    pd.Series([['Tank', 'Damage', 'Support']] * len(stage_2_groups_with_points)))

# handle placements
emea_placements = pd.read_csv('../data/EMEA/owcs/stage_2/placements.csv')
na_placements = pd.read_csv('../data/NA/owcs/stage_2/placements.csv')
placements = pd.concat([emea_placements, na_placements])[['team_id', 'place']]

stage_2_groups_with_points = stage_2_groups_with_points.merge(placements, how='left', on='team_id').fillna('TBD')


def filter_placed_players(group):
    if group['place'].values[0] != 'TBD':
        sorted_group = group.sort_values(by='maps_played', ascending=False)
        return sorted_group.head(5)
    return group


stage_2_groups_with_points = stage_2_groups_with_points.groupby('team_id').apply(filter_placed_players)

stage_2_groups_with_points = stage_2_groups_with_points.rename(
    columns={'player_id': 'playerId', 'team_id': 'teamId', 'team_name': 'teamName', 'maps_played': 'mapsPlayed',
             'player_role': 'role'})
stage_2_groups_with_points[
    ['region', 'playerId', 'ign', 'teamId', 'teamName', 'prevTeamId', 'points', 'mapsPlayed',
     'role', 'place']].to_csv(
    'data/team_circuit_points.csv', index=False)

print(stage_2_groups_with_points[
          ['region', 'playerId', 'ign', 'teamId', 'teamName', 'prevTeamId', 'points', 'mapsPlayed', 'role', 'place']])
