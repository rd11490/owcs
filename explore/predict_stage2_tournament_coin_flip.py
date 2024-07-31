import pandas as pd
from explore.predict_match import predict_match_coin_flip
from explore.teams import *

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)

num_sims = 100000

team_mwa = pd.read_csv('data/team_mwa.csv')

team_mwa_dict = team_mwa.set_index('team_id').to_dict(orient='index')


def predict_tournament(seed1, seed2, seed3, seed4, seed5, seed6, seed7, seed8, team_mwa_dict, match_results={}):
    if match_results.get('round1_match1') is None:
        round1_match1 = predict_match_coin_flip(seed1, seed8, team_mwa_dict)
    else:
        round1_match1 = match_results['round1_match1']

    if match_results.get('round1_match2') is None:
        round1_match2 = predict_match_coin_flip(seed4, seed5, team_mwa_dict)
    else:
        round1_match2 = match_results['round1_match2']

    if match_results.get('round1_match3') is None:
        round1_match3 = predict_match_coin_flip(seed2, seed7, team_mwa_dict)
    else:
        round1_match3 = match_results['round1_match3']

    if match_results.get('round1_match4') is None:
        round1_match4 = predict_match_coin_flip(seed3, seed6, team_mwa_dict)
    else:
        round1_match4 = match_results['round1_match4']

    if match_results.get('winners_semifinal1') is None:
        winners_semifinal1 = predict_match_coin_flip(round1_match1['winner'], round1_match2['winner'], team_mwa_dict)
    else:
        winners_semifinal1 = match_results['winners_semifinal1']

    if match_results.get('winners_semifinal2') is None:
        winners_semifinal2 = predict_match_coin_flip(round1_match3['winner'], round1_match4['winner'], team_mwa_dict)
    else:
        winners_semifinal2 = match_results['winners_semifinal2']

    if match_results.get('winners_final') is None:
        winners_final = predict_match_coin_flip(winners_semifinal1['winner'], winners_semifinal2['winner'], team_mwa_dict)
    else:
        winners_final = match_results['winners_final']

    if match_results.get('losers_round1_match1') is None:
        losers_round1_match1 = predict_match_coin_flip(round1_match1['loser'], round1_match2['loser'], team_mwa_dict)
    else:
        losers_round1_match1 = match_results['losers_round1_match1']

    if match_results.get('losers_round1_match2') is None:
        losers_round1_match2 = predict_match_coin_flip(round1_match3['loser'], round1_match4['loser'], team_mwa_dict)
    else:
        losers_round1_match2 = match_results['losers_round1_match2']

    if match_results.get('losers_round2_match1') is None:
        losers_round2_match1 = predict_match_coin_flip(losers_round1_match1['winner'], winners_semifinal2['loser'], team_mwa_dict)
    else:
        losers_round2_match1 = match_results['losers_round2_match1']

    if match_results.get('losers_round2_match2') is None:
        losers_round2_match2 = predict_match_coin_flip(losers_round1_match2['winner'], winners_semifinal1['loser'], team_mwa_dict)
    else:
        losers_round2_match2 = match_results['losers_round2_match2']

    if match_results.get('losers_semifinal') is None:
        losers_semifinal = predict_match_coin_flip(losers_round2_match1['winner'], losers_round2_match2['winner'], team_mwa_dict)
    else:
        losers_semifinal = match_results['losers_semifinal']

    if match_results.get('losers_final') is None:
        losers_final = predict_match_coin_flip(losers_semifinal['winner'], winners_final['loser'], team_mwa_dict)
    else:
        losers_final = match_results['losers_final']

    if match_results.get('grand_final') is None:
        grand_final = predict_match_coin_flip(losers_final['winner'], winners_final['winner'], team_mwa_dict, maps_to_win=4)
    else:
        grand_final = match_results['grand_final']

    return {
        '1': grand_final['winner'],
        '2': grand_final['loser'],
        '3': losers_final['loser'],
        '4': losers_semifinal['loser'],
        '5': losers_round2_match1['loser'],
        '6': losers_round2_match2['loser'],
        '7': losers_round1_match1['loser'],
        '8': losers_round1_match2['loser']
    }


def get_or_zero(value_counts, team):
    if team in value_counts.keys():
        return value_counts[team]
    return 0


def sim_tournament(seed1, seed2, seed3, seed4, seed5, seed6, seed7, seed8, team_mwa_dict, num_sims, match_results={}):
    results = []
    for i in range(num_sims):
        result = predict_tournament(seed1, seed2, seed3, seed4, seed5, seed6, seed7, seed8, team_mwa_dict, match_results)
        result['sim'] = i
        results.append(result)

    results_df = pd.DataFrame(results)

    first = results_df['1'].value_counts()
    second = results_df['2'].value_counts()
    third = results_df['3'].value_counts()
    fourth = results_df['4'].value_counts()
    fifth_sixth1 = results_df['5'].value_counts()
    fifth_sixth2 = results_df['6'].value_counts()
    seven_eight1 = results_df['7'].value_counts()
    seven_eight2 = results_df['8'].value_counts()

    odds = []
    for team in [seed1, seed2, seed3, seed4, seed5, seed6, seed7, seed8]:
        odds.append({
            'team': team_mwa_dict[team]['team_name'],
            '1': 100 * get_or_zero(first, team) / num_sims,
            '2': 100 * get_or_zero(second, team) / num_sims,
            '3': 100 * get_or_zero(third, team) / num_sims,
            '4': 100 * get_or_zero(fourth, team) / num_sims,
            '5/6': 100 * (get_or_zero(fifth_sixth1, team) + get_or_zero(fifth_sixth2, team)) / num_sims,
            '7/8': 100 * (get_or_zero(seven_eight1, team) + get_or_zero(seven_eight2, team)) / num_sims,
        })

    odds_df = pd.DataFrame(odds)
    odds_df = odds_df.round()
    odds_df = odds_df.sort_values(by=['1', '2', '3', '4', '5/6', '7/8'], ascending=False)
    print(odds_df)
    return results_df


def build_match_result(winner, loser):
    return {
        'winner': winner,
        'loser': loser
    }


#### EMEA Tournament
seed1 = SPACESTATION
seed2 = ENCE
seed3 = TWISTED_MINDS
seed4 = PEACE_AND_LOVE
seed5 = DEIMPERO
seed6 = AWW_YEAH
seed7 = SUPERSHYOW
seed8 = TEAM_PEPS

match_results = {
    'round1_match1': build_match_result(seed1, seed8),
    'round1_match2': build_match_result(seed4, seed5),
    'round1_match3': build_match_result(seed2, seed7),
    'round1_match4': build_match_result(seed3, seed6),

    'winners_semifinal1': build_match_result(seed1, seed4),
    'winners_semifinal2': build_match_result(seed2, seed3),

    'losers_round1_match1': build_match_result(seed8, seed5),
    'losers_round1_match2': build_match_result(seed7, seed6)
}

print('EMEA Stage 2')
emea_results = sim_tournament(seed1, seed2, seed3, seed4, seed5, seed6, seed7, seed8, team_mwa_dict, num_sims, match_results)
emea_results.to_csv('./data/emea_sim_results_flip.csv', index=False)

#
# #### NA Tournament
# seed1 = TORONTO_DEFIANT
# seed2 = LUMINOSITY
# seed3 = M80
# seed4 = SOG
# seed5 = PIP
# seed6 = FMCL
# seed7 = WHO_IS_GOLDFISH
# seed8 = CITRUS_NATION
#
# match_results = {
#     'round1_match1': build_match_result(seed1, seed8),
#     'round1_match2': build_match_result(seed2, seed7),
#     'round1_match3': build_match_result(seed3, seed6),
#     'round1_match4': build_match_result(seed4, seed5),
#
#     'losers_round1_match1': build_match_result(seed8, seed5),
#     'losers_round1_match2': build_match_result(seed6, seed7)
# }
# print('NA Stage 2')
# na_results = sim_tournament(seed1, seed2, seed3, seed4, seed5, seed6, seed7, seed8, team_mwa_dict, num_sims, match_results)
# na_results.to_csv('./data/na_sim_results_flip.csv', index=False)
