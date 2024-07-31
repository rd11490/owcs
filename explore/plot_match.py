import pandas as pd
from explore.predict_match import predict_match
from explore.teams import *
import matplotlib.pyplot as plt


pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)

num_sims = 10000
maps_to_win = 3
stage = 'stage2/major'

team_mwa = pd.read_csv('data/team_mwa.csv')

team_mwa_dict = team_mwa.set_index('team_id').to_dict(orient='index')

TEAM_1 = SPACESTATION
TEAM_2 = TORONTO_DEFIANT

def build_map_diff_dict(maps_to_win):
    possible_loser_scores = list(range(0, maps_to_win))
    combos = []
    dict = {}
    for score in possible_loser_scores:
        combos.append(score - maps_to_win)
        combos.append(maps_to_win - score)
    combos.sort()
    for c in combos:
        dict[c] = 0
    return dict

def convert_average_diff_to_score(diff):
    diff = round(diff, 1)
    if diff < 0:
        return maps_to_win, round(maps_to_win + diff,1)
    else:
        return round(maps_to_win - diff, 1), maps_to_win

def ticks_to_labels(ticks, maps_to_win):
    labels = []
    for t in ticks:
        if t < 0:
            labels.append('{}-{}'.format(maps_to_win, maps_to_win + t))
        else:
            labels.append('{}-{}'.format(maps_to_win - t, maps_to_win))
    return labels

def bar_colors(ticks):
    color = []
    for t in ticks:
        if t < 0:
            color.append('blue')
        else:
            color.append('red')
    return color
def plot_histogram(results_arr, maps_to_win):
    map_diff = build_map_diff_dict(maps_to_win)
    team_one = results_arr[0]['team_one_name']
    team_two = results_arr[0]['team_two_name']

    differential_arr = []
    team_one_wins_cnt = 0
    for r in results_arr:
        differential = r['team_one_map_wins'] - r['team_two_map_wins']
        differential_arr.append(differential)
        if differential > 0:
            team_one_wins_cnt += 1
        map_diff[differential] += 1

    team_one_wins = round(100*team_one_wins_cnt/len(differential_arr))
    team_two_wins = 100 - team_one_wins

    frequency = [v / num_sims for v in map_diff.values()]
    xvalues = list(map_diff.keys())
    xvalues.reverse()

    color = bar_colors(xvalues)

    plt.figure(figsize=(8, 5))
    rects = plt.bar(xvalues, frequency, color=color)
    labels = ticks_to_labels(xvalues, maps_to_win)

    plt.xticks(ticks=xvalues, labels=labels)
    plt.title('{} ({}%) {} ({}%) ({} Simulations)'.format(team_one, team_one_wins, team_two, team_two_wins, num_sims))
    plt.xlabel('{} - {}'.format(team_one, team_two))
    plt.ylabel('Frequency')
    plt.ylim((0, 1))

    for rect in rects:
        height = rect.get_height()
        y = round(height * num_sims)
        if y > 0:
            plt.text(rect.get_x() + rect.get_width() / 2, height * 1.01, y, fontweight='bold', ha='center')
    filename = '-'.join(f'{team_one}-{team_two}-match-result-first_to_{maps_to_win}'.split(' '))
    plt.savefig(f'plots/{stage}/{filename}')


results = []

for i in range(num_sims):
    result = predict_match(TEAM_1, TEAM_2, team_mwa_dict, maps_to_win)
    result['sim'] = i
    results.append(result)

plot_histogram(results, maps_to_win)