import pandas as pd
from explore.predict_match import predict_match
from explore.teams import *

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)

team_mwa = pd.read_csv('data/team_mwa.csv')

team_mwa_dict = team_mwa.set_index('team_id').to_dict(orient='index')

emea_results = pd.read_csv('./data/emea_sim_results.csv')
emea_current_points = {
    TWISTED_MINDS: 210,
    ENCE: 190,
    SPACESTATION: 125,
    TEAM_PEPS: 65,
    AWW_YEAH: 30,
    PEACE_AND_LOVE: 20,
    SUPERSHYOW: 0,
    DEIMPERO: 0
}


def points_per_place(place):
    if place == 1:
        return 500
    if place == 2:
        return 400
    if place == 3:
        return 300
    if place == 4:
        return 250
    if place == 5 or place == 6:
        return 200
    return 150


def calculate_point_totals(row, curr_point_totals):
    first = row['1']
    second = row['2']
    third = row['3']
    fourth = row['4']
    fifth = row['5']
    sixth = row['6']
    seventh = row['7']
    eight = row['8']

    sim = row['sim']

    qualified = [(first, curr_point_totals[first] + points_per_place(1))]

    teams_and_points = [
        (second, curr_point_totals[second] + points_per_place(2)),
        (third, curr_point_totals[third] + points_per_place(3)),
        (fourth, curr_point_totals[fourth] + points_per_place(4)),
        (fifth, curr_point_totals[fifth] + points_per_place(5)),
        (sixth, curr_point_totals[sixth] + points_per_place(6)),
        (seventh, curr_point_totals[seventh] + points_per_place(7)),
        (eight, curr_point_totals[eight] + points_per_place(8)),
    ]

    teams_and_points = sorted(teams_and_points, key=lambda x: x[1])
    teams_and_points.reverse()
    teams_and_points = qualified + teams_and_points
    out = {
        'sim': sim
    }
    for i, team in enumerate(teams_and_points):
        out[str(i + 1)] = team[0]

    return pd.Series(out)


def get_or_zero(value_counts, team):
    if team in value_counts.keys():
        return value_counts[team]
    return 0


def convert_point_results_to_odds(results_df, current_points):
    first = results_df['1'].value_counts()
    second = results_df['2'].value_counts()
    third = results_df['3'].value_counts()
    fourth = results_df['4'].value_counts()
    fifth_sixth1 = results_df['5'].value_counts()
    fifth_sixth2 = results_df['6'].value_counts()
    seven_eight1 = results_df['7'].value_counts()
    seven_eight2 = results_df['8'].value_counts()

    num_sims = results_df['sim'].max()

    odds = []
    for team in current_points.keys():
        odds.append({
            'team': team_mwa_dict[team]['team_name'],
            '1': 100 * get_or_zero(first, team) / num_sims,
            '2': 100 * get_or_zero(second, team) / num_sims,
            '3': 100 * get_or_zero(third, team) / num_sims,
            '4': 100 * get_or_zero(fourth, team) / num_sims,
            '5/6': 100 * (get_or_zero(fifth_sixth1, team) + get_or_zero(fifth_sixth2, team)) / num_sims,
            '7/8': 100 * (get_or_zero(seven_eight1, team) + get_or_zero(seven_eight2, team)) / num_sims,
            'Qualified': 100 * (
                        get_or_zero(first, team) + get_or_zero(second, team) + get_or_zero(third, team)) / num_sims
        })

    odds_df = pd.DataFrame(odds)
    odds_df = odds_df.round()
    odds_df = odds_df.sort_values(by=['Qualified', '1', '2', '3', '4', '5/6', '7/8'], ascending=False)
    print(odds_df)


print('     EMEA Dallas Qualification')
emea_points_results = emea_results.apply(lambda row: calculate_point_totals(row, emea_current_points), axis=1)
convert_point_results_to_odds(emea_points_results, emea_current_points)


na_results = pd.read_csv('./data/na_sim_results.csv')
na_circuit_points = {
    TORONTO_DEFIANT: 250,
    LUMINOSITY: 125,
    M80: 105,
    SOG: 100,
    PIP: 90,
    FMCL: 65,
    CITRUS_NATION: 45,
    WHO_IS_GOLDFISH: 0
}

print('\n\n')
print('     NA Dallas Qualification')
na_points_results = na_results.apply(lambda row: calculate_point_totals(row, na_circuit_points), axis=1)
convert_point_results_to_odds(na_points_results, na_circuit_points)
