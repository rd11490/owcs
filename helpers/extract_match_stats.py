from services.facit_api import pull_player_stats


def opponent_id(team_id, team1, team2):
    if team_id == team1:
        return team2
    else:
        return team1


def extract_match_stats(resp, map_info):
    player_stats = []
    team_stats = []
    for map_stats in resp:
        comp_id = map_stats.get('competitionId')
        map_num = map_stats.get('matchRound')
        map_date = map_stats.get('date')
        match_id = map_stats.get('matchId')
        map_id = map_stats.get('i1')  # map_id
        winning_team = map_stats.get('i2')
        map_type = map_stats.get('i18')
        teams = map_stats.get('teams', [])
        team1_id = map_stats.get('teams', [])[0].get('teamId')
        team2_id = map_stats.get('teams', [])[1].get('teamId')
        for team in teams:
            players = team.get('players', [])
            team_id = team.get('teamId')
            team_name = team.get('i4')
            team_win = float(team.get('i5'))
            team_score = float(team.get('i6'))
            team_elims = float(team.get('c3'))
            team_deaths = float(team.get('c4'))
            team_stats.append({
                'competition_id': comp_id,
                'map_number': map_num,
                'map_date': map_date,
                'match_id': match_id,
                'map_id': map_id,
                'map_name': map_info[map_id],
                'winning_team': winning_team,
                'map_type': map_type,
                'team_id': team_id,
                'team_name': team_name,
                'team_win': team_win,
                'opponent_team_id': opponent_id(team_id, team1_id, team2_id),
                'team_score': team_score,
                'team_elims': team_elims,
                'team_deaths': team_deaths
            })

            for player in players:
                player_deaths = float(player.get('i9'))
                player_nickname = player.get('nickname')
                player_assists = float(player.get('i10'))
                player_damage = float(player.get('i13'))
                player_healing = float(player.get('i14'))
                player_damage_mit = float(player.get('i17'))
                player_elims = float(player.get('i8'))
                player_role = player.get('i16')
                player_id = player.get('playerId')
                player_stats.append({
                    'competition_id': comp_id,
                    'map_number': map_num,
                    'map_date': map_date,
                    'match_id': match_id,
                    'map_id': map_id,
                    'map_name': map_info[map_id],
                    'winning_team': winning_team,
                    'map_type': map_type,
                    'team_id': team_id,
                    'team_name': team_name,
                    'team_win': team_win,
                    'opponent_team_id': opponent_id(team_id, team1_id, team2_id),
                    'team_score': team_score,
                    'player_id': player_id,
                    'player_nickname': player_nickname,
                    'player_role': player_role,
                    'elims': player_elims,
                    'deaths': player_deaths,
                    'assists': player_assists,
                    'damage': player_damage,
                    'healing': player_healing,
                    'mitigation': player_damage_mit
                })
    return player_stats, team_stats


def pull_and_extract_match_stats(match_id, map_info):
    resp = pull_player_stats(match_id)
    if resp is None:
        return None
    return extract_match_stats(resp, map_info)
