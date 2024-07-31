import pandas as pd

from helpers.file_names import build_source_dir, placements_file, players_file, points_file, teams_file

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)


def filter_players_eligible(row):
    rank = row['rank']
    maps = row['maps']
    points = row['points']
    if rank <= 2:
        if maps >= 6:
            return points
    elif rank <= 4:
        if maps >= 5:
            return points
    elif rank <= 6:
        if maps >= 4:
            return points
    elif rank <= 8:
        if maps >= 3:
            return points
    elif rank <= 12:
        if maps >= 2:
            return points
    elif rank <= 16:
        if maps >= 1:
            return points
    return 0

def calculatae_circuit_points(config):
    match_file = f'{build_source_dir(config["swiss"])}/player_stats.csv'

    rounds_that_count = [config['group_a']['id'],
                         config['group_b']['id'],
                         config['group_c']['id'],
                         config['group_d']['id'],
                         config['main_event']['id']
                         ]

    player_stats = pd.read_csv(match_file)
    player_stats = player_stats[player_stats['competition_id'].isin(rounds_that_count)]
    maps_played = player_stats[['player_id', 'player_nickname', 'team_id', 'map_id']].groupby(
        ['team_id', 'player_id', 'player_nickname']).count().reset_index()



    placements_csv = placements_file(config['swiss'])
    placements_df = pd.read_csv(placements_csv)

    players_csv = players_file(config['swiss'])
    players_df = pd.read_csv(players_csv)

    maps_and_points = maps_played.merge(placements_df, left_on='team_id', right_on='team_id')
    print(maps_and_points)
    maps_and_points = maps_and_points.rename(columns={'map_id': 'maps'})
    maps_and_points['points'] = maps_and_points.apply(lambda row: filter_players_eligible(row), axis=1)
    maps_and_points = maps_and_points.sort_values(by='points', ascending=False)
    players_df = players_df[['player_id', 'ign']]
    maps_and_points = maps_and_points.merge(players_df, on='player_id')

    print(maps_and_points)

    teams_csv = f'{build_source_dir(config["swiss"])}/team_stats.csv'
    teams_df = pd.read_csv(teams_csv)
    teams_df = teams_df[teams_df['competition_id'].isin(rounds_that_count)]
    teams_df = teams_df[['team_id', 'team_name']]
    print(teams_df)
    teams_df = teams_df.groupby('team_id').first().reset_index()

    print(teams_df)

    maps_and_points = maps_and_points.merge(teams_df, left_on='team_id', right_on='team_id')
    print(maps_and_points)

    maps_and_points = maps_and_points[['team_id', 'team_name', 'player_id', 'ign', 'points']]

    roles = player_stats[['player_id', 'player_role']].groupby('player_id')['player_role'].agg(lambda x: list(set(x))).reset_index()

    maps_and_points = maps_and_points.merge(roles, on='player_id')

    maps_and_points = maps_and_points.rename(columns={
        'team_id': 'teamId',
        'player_id': 'playerId',
        'team_name': 'teamName',
        'player_role': 'role'
    })

    points_file_name = points_file(config['swiss'])
    maps_and_points.to_csv(points_file_name, index=False)
