import pandas as pd
import numpy as np
from sklearn.linear_model import RidgeCV
from sklearn import metrics

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)

na_players_stage1 = pd.read_csv('../data/NA/owcs/stage_1/players.csv')
na_players_stage2 = pd.read_csv('../data/NA/owcs/stage_2/players.csv')
emea_players_stage1 = pd.read_csv('../data/EMEA/owcs/stage_1/players.csv')
emea_players_stage2 = pd.read_csv('../data/EMEA/owcs/stage_2/players.csv')
emea_faceit_players_stage1 = pd.read_csv('../data/EMEA/faceit/stage_1/players.csv')
na_faceit_players_stage1 = pd.read_csv('../data/NA/faceit/stage_1/players.csv')

players = pd.concat([na_players_stage1, na_players_stage2, na_faceit_players_stage1, emea_players_stage1, emea_players_stage2, emea_faceit_players_stage1])
players = players[['player_id', 'ign']].drop_duplicates()

players_ids = players['player_id'].unique().tolist()

# Generate a list of players
players_ids = sorted(players_ids)

na_match_results_stage1 = pd.read_csv('../data/NA/owcs/stage_1/match_results.csv')
na_match_results_stage2 = pd.read_csv('../data/NA/owcs/stage_2/match_results.csv')
na_match_results_faceit_stage1 = pd.read_csv('../data/NA/faceit/stage_1/match_results.csv')
emea_match_results_stage1 = pd.read_csv('../data/EMEA/owcs/stage_1/match_results.csv')
emea_match_results_stage2 = pd.read_csv('../data/EMEA/owcs/stage_2/match_results.csv')
emea_match_results_faceit_stage1 = pd.read_csv('../data/EMEA/faceit/stage_1/match_results.csv')

# na_match_results_stage1['weight'] = 1
# emea_match_results_stage1['weight'] = 1
# na_match_results_stage2['weight'] = 2
# emea_match_results_stage2['weight'] = 2

match_results = pd.concat([na_match_results_stage1, na_match_results_stage2, na_match_results_faceit_stage1, emea_match_results_stage1, emea_match_results_stage2, emea_match_results_faceit_stage1])


def determine_sample_weight(event_name):
    sample_weight = 1
    # if 'Stage 2' in event_name:
    #     sample_weight = sample_weight * 2
    #     if 'Group' in event_name:
    #         sample_weight = sample_weight * 8
    #     if 'Main Event' in event_name:
    #         sample_weight = sample_weight * 16
    # if 'Stage 1' in event_name:
    #     if 'Group' in event_name:
    #         sample_weight = sample_weight * 2
    #     if 'Main Event' in event_name:
    #         sample_weight = sample_weight * 2

    return sample_weight


match_results['weight'] = match_results['event_name'].apply(determine_sample_weight)

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
         'team2_player1', 'team2_player2', 'team2_player3', 'team2_player4', 'team1_score', 'team2_score', 'weight']]
    working_frame = working_frame.dropna()
    maps_x_base = working_frame[
        ['team1_player0', 'team1_player1', 'team1_player2', 'team1_player3', 'team1_player4', 'team2_player0',
         'team2_player1', 'team2_player2', 'team2_player3', 'team2_player4']]
    maps_x_rows = np.apply_along_axis(build_row, 1, maps_x_base, player_ids)

    working_frame['team1_win'] = 1 * (working_frame['team1_score'] > working_frame['team2_score'])
    working_frame['team2_win'] = -1 * (working_frame['team2_score'] > working_frame['team1_score'])
    working_frame['Y_score'] = working_frame['team1_win'] + working_frame['team2_win']
    maps_y_rows = working_frame['Y_score'].values
    weights = working_frame['weight']

    return maps_x_rows, maps_y_rows, weights

# Convert lambda value to alpha needed for ridge CV
def lambda_to_alpha(lambda_value, samples):
    return (lambda_value * samples) / 2.0


# Convert RidgeCV alpha back into a lambda value
def alpha_to_lambda(alpha_value, samples):
    return (alpha_value * 2.0) / samples


# Calculate Regularized Map Type Score
def calculate_rmts(stint_X_rows, stint_Y_rows, players, sample_weights):
    print('Running MWA')
    # We will perform cross validation across a number of different lambdas
    lambdas = [.001, .01, 0.025, .05, 0.075, .1, .125, .15, .175, .2, .225, .25]

    # convert the lambdas into alpha values
    alphas = [lambda_to_alpha(l, stint_X_rows.shape[0]) for l in lambdas]

    # Create our ridge CV model
    clf = RidgeCV(alphas=alphas, cv=5, fit_intercept=True)

    # Fit our player_data
    model = clf.fit(stint_X_rows, stint_Y_rows, sample_weight=sample_weights)

    # extract our teams, and coefficients and combine them into a single matrix (20 x 3)
    players_arr = np.transpose(np.array(players).reshape(1, len(players)))
    coef_array = np.transpose(model.coef_.reshape(1, len(players)))
    print(players_arr)
    print(coef_array)

    player_coefs = np.concatenate([players_arr, coef_array], axis=1)

    # build a dataframe from our matrix
    rmts = pd.DataFrame(player_coefs)
    intercept = model.intercept_


    rmts.columns = ['player_id', 'mwa']
    rmts['mwa'] = rmts['mwa'].astype(float)

    # Calculate a total mwa
    rmts['intercept'] = intercept

    # Generate a couple of error statistics
    lambda_picked = alpha_to_lambda(model.alpha_, stint_X_rows.shape[0])
    print('r^2: ', model.score(stint_X_rows, stint_Y_rows))
    print('lambda: ', lambda_picked)
    print('intercept: ', intercept)

    pred = model.predict(stint_X_rows)
    print('MAE: ', metrics.mean_absolute_error(stint_Y_rows, pred))
    print('MSE: ', metrics.mean_squared_error(stint_Y_rows, pred))
    rmts = rmts.sort_values(by='mwa', ascending=False)

    sigma_sq = np.var(stint_Y_rows - pred)
    coef_variance = sigma_sq * np.linalg.inv(stint_X_rows.T @ stint_X_rows + model.alpha_ * np.identity(stint_X_rows.shape[1])) @ stint_X_rows.T @ stint_X_rows @ np.linalg.inv(stint_X_rows.T @ stint_X_rows + model.alpha_ * np.identity(stint_X_rows.shape[1])).T


    print(f'Variance: {coef_variance}')


    var_map = {}
    for ind, player in enumerate(players_arr):
        var = abs(coef_variance[ind][ind])
        var_map[player[0]] = {'player_id': player[0], 'var': var }
    variance = pd.DataFrame(var_map.values())

    rmts = rmts.merge(variance, on='player_id')
    rmts['mwa stdev'] = np.sqrt(rmts['var'])
    rmts = rmts[['player_id', 'mwa', 'mwa stdev']]
    rmts['normalized mwa'] = 100 * ((2 * (rmts['mwa'] - rmts['mwa'].min())/(rmts['mwa'].max()-rmts['mwa'].min())) - 1)
    print(rmts)
    return rmts


X, Y, weight = extract_X_Y(match_results, players_ids)
print(X)
print(Y)
mwa = calculate_rmts(X, Y, players_ids, weight)
mwa = mwa.merge(players, on='player_id')
mwa = mwa[['player_id', 'ign', 'mwa', 'mwa stdev', 'normalized mwa']]
mwa.to_csv('data/mwa.csv', index=False)
print(mwa)