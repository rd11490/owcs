from helpers.file_path import data_home_dir, create_dir_if_not_exists


def build_file_with_prefix(config, postfix):
    data_dir = config['dir']
    file_prefix = config['file_prefix']
    directory = f'{data_home_dir()}/{data_dir}'
    create_dir_if_not_exists(directory)
    return f'{directory}/{file_prefix}_{postfix}.csv'


def build_file_with_prefix_and_sub_dir(config, subdir, postfix):
    data_dir = config['dir']
    file_prefix = config['file_prefix']
    directory = f'{data_home_dir()}/{data_dir}/{subdir}'
    create_dir_if_not_exists(directory)
    return f'{directory}/{file_prefix}_{postfix}.csv'


def build_file_no_prefix(config, postfix):
    data_dir = config['dir']
    directory = f'{data_home_dir()}/{data_dir}'
    create_dir_if_not_exists(directory)
    return f'{directory}/{postfix}.csv'


def build_subdir(config, subdir):
    data_dir = config['dir']
    return f'{data_home_dir()}/{data_dir}/{subdir}'


def build_source_dir(config):
    data_dir = config['dir']
    return f'{data_home_dir()}/{data_dir}'


def matches_dir(config):
    return build_subdir(config, 'matches')


def match_results_dir(config):
    return build_subdir(config, 'matches_results')


def player_stats_dir(config):
    return build_subdir(config, 'player_stats')


def team_stats_dir(config):
    return build_subdir(config, 'team_stats')


def map_bans_dir(config):
    return build_subdir(config, 'match_map_bans')


def matches_file(config):
    return build_file_with_prefix_and_sub_dir(config, 'matches', 'matches')


def match_results_file(config):
    return build_file_with_prefix_and_sub_dir(config, 'matches_results', 'matches_results')


def match_results_failed_ids_file(config):
    return build_file_with_prefix_and_sub_dir(config, 'failed_ids', 'match_failed_ids')


def match_map_bans_file(config):
    return build_file_with_prefix_and_sub_dir(config, 'match_map_bans', 'match_map_bans')


def match_map_bans_failed_ids_file(config):
    return build_file_with_prefix_and_sub_dir(config, 'failed_ids', 'match_map_bans_failed_ids')


def team_stats_file(config):
    return build_file_with_prefix_and_sub_dir(config, 'team_stats', 'team_stats')


def player_stats_file(config):
    return build_file_with_prefix_and_sub_dir(config, 'player_stats', 'player_stats')


def stats_failed_ids_file(config):
    return build_file_with_prefix_and_sub_dir(config, 'failed_ids', 'stats_failed_ids')


def teams_file(config):
    return build_file_no_prefix(config, 'teams')


def players_file(config):
    return build_file_no_prefix(config, 'players')


def coaches_file(config):
    return build_file_no_prefix(config, 'coaches')


def placements_file(config):
    return build_file_no_prefix(config, 'placements')


def points_file(config):
    return build_file_no_prefix(config, 'circuit_points')
