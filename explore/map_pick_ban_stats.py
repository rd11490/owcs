import pandas as pd

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)


na_stage_1 = pd.read_csv('../data/NA/owcs/stage_1/map_bans.csv')

# emea_stage_1 = pd.read_csv('../data/NA/stage_1/map_bans.csv')


def overall_stats(map_ban_df):
    df = map_ban_df[['map_name', 'action', 'action_round', 'match_id']]
    counted = df.groupby(['map_name', 'action', 'action_round']).count().reset_index()
    counted.columns = ['map_name', 'action', 'action_round', 'count']
    print(counted)


overall_stats(na_stage_1)