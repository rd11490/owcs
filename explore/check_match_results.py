import pandas as pd
from configs.EMEA_Config import emea_config_stage_2, emea_config_stage_1
from configs.NA_config import na_config_stage_1, na_config_stage_2
from helpers.extract_team_data import scrape_all_teams
from helpers.file_names import build_source_dir, match_results_dir
import numpy as np

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)

match_dir = match_results_dir(na_config_stage_2['swiss'])
match_file = f'{build_source_dir(na_config_stage_2["swiss"])}/match_results.csv'

match_results_1 = pd.read_csv(match_file)

match_dir = match_results_dir(na_config_stage_1['swiss'])
match_file = f'{build_source_dir(na_config_stage_1["swiss"])}/match_results.csv'

match_results_2 = pd.read_csv(match_file)

match_results = pd.concat([match_results_1, match_results_2])
print(match_results.columns)

# team_name = 'FMCL'
# player = '826c2bd4-cb43-4b6c-90a9-21ee53b87bf9' # SEEKER
player = 'f306cf00-683c-4861-9b91-f74fbb379d27' #azruf

match_results = match_results[
    ['map_name', 'team1_name', 'team1_score', 'team2_name', 'team2_score', 'team1_player0', 'team1_player1',
     'team1_player2', 'team1_player3', 'team1_player4', 'team2_player0', 'team2_player1', 'team2_player2',
     'team2_player3', 'team2_player4']]
match_results['team1_win'] = 1 * (match_results['team1_score'] > match_results['team2_score'])
match_results['team2_win'] = -1 * (match_results['team2_score'] > match_results['team1_score'])
match_results['Y_score'] = match_results['team1_win'] + match_results['team2_win']

player_matches = match_results[(match_results['team1_player0'] == player) |
                               (match_results['team1_player1'] == player) |
                               (match_results['team1_player2'] == player) |
                               (match_results['team1_player3'] == player) |
                               (match_results['team1_player4'] == player) |
                               (match_results['team2_player0'] == player) |
                               (match_results['team2_player1'] == player) |
                               (match_results['team2_player2'] == player) |
                               (match_results['team2_player3'] == player) |
                               (match_results['team2_player4'] == player)]





teams_1 = list(player_matches['team1_name'].unique())
teams_2 = list(player_matches['team2_name'].unique())
teams = sorted(list(set(teams_1 + teams_2)))

na_players_stage1 = pd.read_csv('../data/NA/owcs/stage_1/players.csv')
na_players_stage2 = pd.read_csv('../data/NA/owcs/stage_2/players.csv')
emea_players_stage1 = pd.read_csv('../data/EMEA/owcs/stage_1/players.csv')
emea_players_stage2 = pd.read_csv('../data/EMEA/owcs/stage_2/players.csv')

players = pd.concat([na_players_stage1, na_players_stage2])
players = players[players['team_name'].isin(teams)]
players = players[['player_id', 'ign']].drop_duplicates()
players_ids = players['player_id'].unique().tolist()
# Generate a list of players
players_ids = sorted(players_ids)


def should_track(id, players):
    if id in players:
        return True
    return False


def set_row_value(id, players, row_out, value):
    if should_track(id, players):
        row_out[players.index(id)] = value


def build_row(row_in, players):
    id_t1_0 = row_in[0]
    id_t1_1 = row_in[1]
    id_t1_2 = row_in[2]
    id_t1_3 = row_in[3]
    id_t1_4 = row_in[4]

    id_t2_0 = row_in[5]
    id_t2_1 = row_in[6]
    id_t2_2 = row_in[7]
    id_t2_3 = row_in[8]
    id_t2_4 = row_in[9]

    row_out = np.zeros(len(players))

    set_row_value(id_t1_0, players, row_out, 1)
    set_row_value(id_t1_1, players, row_out, 1)
    set_row_value(id_t1_2, players, row_out, 1)
    set_row_value(id_t1_3, players, row_out, 1)
    set_row_value(id_t1_4, players, row_out, 1)

    set_row_value(id_t2_0, players, row_out, -1)
    set_row_value(id_t2_1, players, row_out, -1)
    set_row_value(id_t2_2, players, row_out, -1)
    set_row_value(id_t2_3, players, row_out, -1)
    set_row_value(id_t2_4, players, row_out, -1)
    return row_out


def extract_X_Y(frame, player_ids):
    working_frame = frame[
        ['team1_player0', 'team1_player1', 'team1_player2', 'team1_player3', 'team1_player4', 'team2_player0',
         'team2_player1', 'team2_player2', 'team2_player3', 'team2_player4', 'team1_score', 'team2_score']]
    working_frame = working_frame.dropna()
    maps_x_base = working_frame[
        ['team1_player0', 'team1_player1', 'team1_player2', 'team1_player3', 'team1_player4', 'team2_player0',
         'team2_player1', 'team2_player2', 'team2_player3', 'team2_player4']]
    maps_x_rows = np.apply_along_axis(build_row, 1, maps_x_base, player_ids)

    working_frame['team1_win'] = 1 * (working_frame['team1_score'] > working_frame['team2_score'])
    working_frame['team2_win'] = -1 * (working_frame['team2_score'] > working_frame['team1_score'])
    working_frame['Y_score'] = working_frame['team1_win'] + working_frame['team2_win']
    maps_y_rows = working_frame['Y_score'].values

    return maps_x_rows, maps_y_rows
print(player_matches[[ 'map_name','team1_name', 'team2_name', 'team1_score', 'team2_score', 'team1_win', 'team2_win', 'Y_score']])
X,Y = extract_X_Y(player_matches, players_ids)
print(players_ids.index(player))
print(X)
player_X = X[:, players_ids.index(player)]
player_Y = Y
positive = 0
negative = 0
for x,y in zip(player_X, player_Y):
    print(f'Team Score: {y}, Player Score: {x}')
    if int(x) == int(y):
        positive += 1
    else:
        negative += 1
print(f'Player {positive} wins and {negative} losses')
