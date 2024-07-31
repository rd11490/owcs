from configs.EMEA_Config import emea_config_stage_2, emea_config_stage_1, emea_config_faceit_stage_1
from configs.NA_config import na_config_stage_1, na_config_stage_2, na_config_faceit_stage_1
from helpers.file_names import matches_dir, build_source_dir, match_results_dir, player_stats_dir, team_stats_dir, \
    map_bans_dir
from processors.merge_directory import merge_directory


def merge_all(config, base_key):
    ## Match
    match_dir = matches_dir(config[base_key])
    match_file = f'{build_source_dir(config[base_key])}/matches.csv'
    merge_directory(match_dir, match_file)

    ## Match Results
    match_dir = match_results_dir(config[base_key])
    match_file = f'{build_source_dir(config[base_key])}/match_results.csv'
    merge_directory(match_dir, match_file)

    ## Team Stats
    match_dir = team_stats_dir(config[base_key])
    match_file = f'{build_source_dir(config[base_key])}/team_stats.csv'
    merge_directory(match_dir, match_file)

    ## Player Stats
    match_dir = player_stats_dir(config[base_key])
    match_file = f'{build_source_dir(config[base_key])}/player_stats.csv'
    merge_directory(match_dir, match_file)

    # ## map bans
    # match_dir = map_bans_dir(config[base_key])
    # match_file = f'{build_source_dir(config[base_key])}/map_bans.csv'
    # merge_directory(match_dir, match_file)


# merge_all(na_config_stage_1, 'swiss')
# merge_all(na_config_stage_2, 'swiss')
# merge_all(emea_config_stage_1, 'swiss')
# merge_all(emea_config_stage_2, 'swiss')


merge_all(na_config_faceit_stage_1, 'round_robin')
merge_all(emea_config_faceit_stage_1, 'round_robin')