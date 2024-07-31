import random

import numpy as np

def get_mwa_from_dict(team_id, dict):
    return dict[team_id]['mwa'], dict[team_id]['mwa stdev'], dict[team_id]['team_name']

def predict_match(team_one, team_two, mwa_dict, maps_to_win=3):
    # initialize each team to have 0 projected wins
    team_one_projected_wins = 0
    team_two_projected_wins = 0

    projected_winner = None
    loser = None
    winner_name = None
    loser_name = None

    team_one_mwa, team_one_mwa_stdev, team_one_name = get_mwa_from_dict(team_one, mwa_dict)
    team_two_mwa, team_two_mwa_stdev, team_two_name = get_mwa_from_dict(team_two, mwa_dict)

    while team_one_projected_wins < maps_to_win and team_two_projected_wins < maps_to_win:
        team_one_mwa_expected = np.random.normal(team_one_mwa, team_one_mwa_stdev)
        team_two_mwa_expected = np.random.normal(team_two_mwa, team_two_mwa_stdev)

        # use estimated map score to determine the map winner
        if team_one_mwa_expected > team_two_mwa_expected:
            team_one_projected_wins += 1
        elif team_one_mwa_expected < team_two_mwa_expected:
            team_two_projected_wins += 1

    # break once a team reaches 3 map wins
    if team_one_projected_wins >= maps_to_win:
        projected_winner = team_one
        winner_name = team_one_name
        loser = team_two
        loser_name = team_two_name

    if team_two_projected_wins >= maps_to_win:
        projected_winner = team_two
        winner_name = team_two_name
        loser = team_one
        loser_name = team_one_name

    return {
        'team_one': team_one,
        'team_one_name': team_one_name,
        'team_one_map_wins': team_one_projected_wins,
        'team_two': team_two,
        'team_two_name': team_two_name,
        'team_two_map_wins': team_two_projected_wins,
        'winner': projected_winner,
        'winner_name': winner_name,
        'loser': loser,
        'loser_name': loser_name
    }

def predict_match_coin_flip(team_one, team_two, mwa_dict, maps_to_win=3):
    # initialize each team to have 0 projected wins
    team_one_projected_wins = 0
    team_two_projected_wins = 0

    projected_winner = None
    loser = None
    winner_name = None
    loser_name = None

    team_one_mwa, team_one_mwa_stdev, team_one_name = get_mwa_from_dict(team_one, mwa_dict)
    team_two_mwa, team_two_mwa_stdev, team_two_name = get_mwa_from_dict(team_two, mwa_dict)


    while team_one_projected_wins < maps_to_win and team_two_projected_wins < maps_to_win:
        team_one_mwa_expected = random.random()
        team_two_mwa_expected = random.random()

        # use estimated map score to determine the map winner
        if team_one_mwa_expected > team_two_mwa_expected:
            team_one_projected_wins += 1
        elif team_one_mwa_expected < team_two_mwa_expected:
            team_two_projected_wins += 1

    # break once a team reaches 3 map wins
    if team_one_projected_wins >= maps_to_win:
        projected_winner = team_one
        winner_name = team_one_name
        loser = team_two
        loser_name = team_two_name

    if team_two_projected_wins >= maps_to_win:
        projected_winner = team_two
        winner_name = team_two_name
        loser = team_one
        loser_name = team_one_name

    return {
        'team_one': team_one,
        'team_one_name': team_one_name,
        'team_one_map_wins': team_one_projected_wins,
        'team_two': team_two,
        'team_two_name': team_two_name,
        'team_two_map_wins': team_two_projected_wins,
        'winner': projected_winner,
        'winner_name': winner_name,
        'loser': loser,
        'loser_name': loser_name
    }