import pandas as pd


pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)

points = pd.read_csv('data/team_circuit_points.csv', keep_default_na=False, na_values=[])

response = {
    'naTeams': {
        'placed': {

        },
        'competing': {

        }
    },
    'emeaTeams': {
        'placed': {

        },
        'competing': {

        }
    }
}
def build_row_from_group(group):
    region = group['region'].values[0]
    team = group['teamName'].values[0]
    competing = group['place'].values[0]
    data = group.sort_values(by='mapsPlayed', ascending=False).to_dict('records')
    if region == 'NA':
        if competing == 'TBD':
            response['naTeams']['competing'][team] = data
        else:
            response['naTeams']['placed'][team] = data

    else:
        if competing == 'TBD':
            response['emeaTeams']['competing'][team] = data
        else:
            response['emeaTeams']['placed'][team] = data


regions_and_teams = points.groupby(by=['region', 'teamId']).apply(build_row_from_group)

print(response)