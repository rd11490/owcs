import pandas as pd
from explore.predict_match import predict_match
from explore.teams import *

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)

num_sims = 10000

team_mwa = pd.read_csv('data/team_mwa.csv')

team_mwa_dict = team_mwa.set_index('team_id').to_dict(orient='index')


def predict_group(seed1, seed2, seed3, seed4, team_mwa_dict, match_results={}):
    if match_results.get('round1_match1') is None:
        round1_match1 = predict_match(seed1, seed4, team_mwa_dict)
    else:
        round1_match1 = match_results['round1_match1']

    if match_results.get('round1_match2') is None:
        round1_match2 = predict_match(seed2, seed3, team_mwa_dict)
    else:
        round1_match2 = match_results['round1_match2']

    if match_results.get('winners_final') is None:
        winners_final = predict_match(round1_match1['winner'], round1_match2['winner'], team_mwa_dict)
    else:
        winners_final = match_results['winners_final']

    if match_results.get('elimination') is None:
        elimination = predict_match(round1_match1['loser'], round1_match2['loser'], team_mwa_dict)
    else:
        elimination = match_results['elimination']

    if match_results.get('decider') is None:
        decider = predict_match(winners_final['loser'], elimination['winner'], team_mwa_dict)
    else:
        decider = match_results['decider']

    return {
        '1': winners_final['winner'],
        '2': decider['winner'],
        '3': decider['loser'],
        '4': elimination['loser']
    }


def get_or_zero(value_counts, team):
    if team in value_counts.keys():
        return value_counts[team]
    return 0


def sim_group(seed1, seed2, seed3, seed4, team_mwa_dict, num_sims, match_results={}):
    results = []
    for i in range(num_sims):
        result = predict_group(seed1, seed2, seed3, seed4, team_mwa_dict, match_results)
        result['sim'] = i
        results.append(result)

    results_df = pd.DataFrame(results)

    first = results_df['1'].value_counts()
    second = results_df['2'].value_counts()
    third = results_df['3'].value_counts()
    fourth = results_df['4'].value_counts()

    odds = []
    for team in [seed1, seed2, seed3, seed4]:
        odds.append({
            'team': team_mwa_dict[team]['team_name'],
            '1': 100 * get_or_zero(first, team) / num_sims,
            '2': 100 * get_or_zero(second, team) / num_sims,
            '3': 100 * get_or_zero(third, team) / num_sims,
            '4': 100 * get_or_zero(fourth, team) / num_sims
        })

    odds_df = pd.DataFrame(odds)
    odds_df = odds_df.round()
    odds_df = odds_df.sort_values(by=['1', '2', '3', '4'], ascending=False)
    print(odds_df)


def build_match_result(winner, loser):
    return {
        'winner': winner,
        'loser': loser
    }


# EMEA Group A
# winners final
print('EMEA Group A')
seed1 = SPACESTATION
seed2 = EX_OBLIVIONE
seed3 = SUPERSHYOW
seed4 = SCHMUNGUS

match_results = {
    'round1_match1': build_match_result(seed1, seed4),
    'round1_match2': build_match_result(seed2, seed3),
    'winners_final': build_match_result(seed1, seed2),
    'elimination': build_match_result(seed3, seed4)
}

sim_group(seed1, seed2, seed3, seed4, team_mwa_dict, num_sims, match_results)



# EMEA Group B
print('EMEA Group B')
seed1 = ENCE
seed2 = TEAM_PEPS
seed3 = A_ONE_MAN_ARMY
seed4 = SHEER_COLD

match_results = {
    'round1_match1': build_match_result(seed1, seed4),
    'round1_match2': build_match_result(seed2, seed3),
    'winners_final': build_match_result(seed1, seed2),
    'elimination': build_match_result(seed3, seed4)
}

sim_group(seed1, seed2, seed3, seed4, team_mwa_dict, num_sims, match_results)

# EMEA Group C
print('EMEA Group C')
seed1 = TWISTED_MINDS
seed2 = DEIMPERO
seed3 = EF_FLEXODIAX
seed4 = ROCSTARS

match_results = {
    'round1_match1': build_match_result(seed1, seed4),
    'round1_match2': build_match_result(seed2, seed3),
    'winners_final': build_match_result(seed1, seed2)
}

sim_group(seed1, seed2, seed3, seed4, team_mwa_dict, num_sims, match_results)

# EMEA Group D
print('EMEA Group D')
seed1 = PEACE
seed2 = ATARAXIA
seed3 = METABOIZ
seed4 = AWW_YEAH

match_results = {
    'round1_match1': build_match_result(seed1, seed4),
    'round1_match2': build_match_result(seed2, seed3),
    'winners_final': build_match_result(seed1, seed2)
}

sim_group(seed1, seed2, seed3, seed4, team_mwa_dict, num_sims, match_results)

# NA Group A
print('NA Group A')
seed1 = TORONTO_DEFIANT
seed2 = DHILLDUCKS
seed3 = VISORED
seed4 = WHO_IS_GOLDFISH

match_results = {
    'round1_match1': build_match_result(seed1, seed4),
    'round1_match2': build_match_result(seed2, seed3),
    'winners_final': build_match_result(seed1, seed2),
    'elimination': build_match_result(seed4, seed3)
}

sim_group(seed1, seed2, seed3, seed4, team_mwa_dict, num_sims, match_results)

# NA Group B
print('NA Group B')
seed1 = TIMELESS
seed2 = LUMINOSITY
seed3 = CITRUS_NATION
seed4 = DAYBREAK

match_results = {
    'round1_match1': build_match_result(seed1, seed4),
    'round1_match2': build_match_result(seed2, seed3),
    'winners_final': build_match_result(seed2, seed1),
    'elimination': build_match_result(seed3, seed4)
}

sim_group(seed1, seed2, seed3, seed4, team_mwa_dict, num_sims, match_results)

# NA Group C
print('NA Group C')
seed1 = M80
seed2 = PIP
seed3 = SHIKIGAMI
seed4 = UNC_INC

match_results = {
    'round1_match1': build_match_result(seed1, seed4),
    'round1_match2': build_match_result(seed2, seed3),
    'winners_final': build_match_result(seed1, seed2)
}

sim_group(seed1, seed2, seed3, seed4, team_mwa_dict, num_sims, match_results)

# NA Group D
print('NA Group D')
seed1 = VICE
seed2 = FMCL
seed3 = TML_NIGHTMARE
seed4 = SOG

match_results = {
    'round1_match1': build_match_result(seed4, seed1),
    'round1_match2': build_match_result(seed2, seed3),
    'winners_final': build_match_result(seed4, seed2)
}

sim_group(seed1, seed2, seed3, seed4, team_mwa_dict, num_sims, match_results)
