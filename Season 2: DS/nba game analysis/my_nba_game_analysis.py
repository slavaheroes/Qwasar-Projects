from os import name
import re
import csv


def find_all_players(play_by_play):
    name_pattern = re.compile(r'\w\. \w+', re.I)
    all_players = []
    for event in play_by_play:
        name = name_pattern.search(event[-1])
        if name:
            all_players.append(name.group(0))
    
    return list(set(all_players))


def all_player_stats(play_by_play, all_players):
    p2_pattern = re.compile(r'(\w\. \w+) makes 2-pt', re.I)
    p2a_pattern = re.compile(r'(\w\. \w+) misses 2-pt', re.I)
    p3_pattern = re.compile(r'(\w\. \w+) makes 3-pt', re.I)
    p3a_pattern = re.compile(r'(\w\. \w+) misses 3-pt', re.I)
    orb_pattern = re.compile(r'Offensive rebound by (\w\. \w+)', re.I)
    ft_pattern = re.compile(r'(\w\. \w+) makes free throw (\d) of (\d)', re.I)
    fta_pattern = re.compile(r'(\w\. \w+) misses free throw (\d) of (\d)', re.I)

    ft1_pattern = re.compile(r'(\w\. \w+) makes clear path free throw (\d) of (\d)', re.I)
    fta1_pattern = re.compile(r'(\w\. \w+) misses clear path free throw (\d) of (\d)', re.I)

    
    pf_pattern = re.compile(r'foul by (\w\. \w+)', re.I)

    drb_pattern = re.compile(r'Defensive rebound by (\w\. \w+)', re.I)

    ast_pattern = re.compile(r'assist by (\w\. \w+)', re.I)
    stl_pattern = re.compile(r'steal by (\w\. \w+)', re.I)
    blk_pattern = re.compile(r'block by (\w\. \w+)', re.I)
    tov_pattern = re.compile(r'Turnover by (\w\. \w+)', re.I)
    

    players_data = []
    for player in all_players:
        player_stats = {"player_name": player, "FG": 0, "FGA": 0, "FG%": 0, "3P": 0, "3PA": 0, 
        "3P%": 0, "FT": 0, "FTA": 0, "FT%": 0, "ORB": 0, "DRB": 0, "TRB": 0, 
        "AST": 0, "STL": 0, "BLK": 0, "TOV": 0, "PF": 0, "PTS": 0}

        for event in play_by_play:
            # 2-pt throws
            p3 = p2_pattern.search(event[-1])
            if p3 and p3.group(1) == player:
                player_stats["FG"] += 1
                player_stats["FGA"] += 1
                player_stats["PTS"] += 2
            p3 = p2a_pattern.search(event[-1])
            if p3 and p3.group(1) == player:
                player_stats["FGA"] += 1
            
            # 3-pt throws
            p3 = p3_pattern.search(event[-1])
            if p3 and p3.group(1) == player:
                player_stats["3P"] += 1
                player_stats["3PA"] += 1
                player_stats["FG"] += 1
                player_stats["FGA"] += 1
                player_stats["PTS"] += 3

            p3 = p3a_pattern.search(event[-1])
            if p3 and p3.group(1) == player:
                player_stats["3PA"] += 1
                player_stats["FGA"] += 1

            #free throws
            p3 = ft_pattern.search(event[-1])
            if p3 and p3.group(1) == player:
                #player_stats["FT"] += int(p3.group(2))
                #player_stats["FTA"] += int(p3.group(3))
                #player_stats["PTS"] += int(p3.group(2))
                player_stats["FT"] += 1
                player_stats["FTA"] += 1
                player_stats["PTS"] += 1
            
            p3 = fta_pattern.search(event[-1])
            if p3 and p3.group(1) == player:
                #player_stats["FT"] += int(p3.group(3)) - int(p3.group(2))
                #player_stats["PTS"] += int(p3.group(3)) - int(p3.group(2))
                player_stats["FTA"] += 1

            #free throws
            p3 = ft1_pattern.search(event[-1])
            if p3 and p3.group(1) == player:
                #player_stats["FT"] += int(p3.group(2))
                #player_stats["FTA"] += int(p3.group(3))
                #player_stats["PTS"] += int(p3.group(2))
                player_stats["FT"] += 1
                player_stats["FTA"] += 1
                player_stats["PTS"] += 1
            
            p3 = fta1_pattern.search(event[-1])
            if p3 and p3.group(1) == player:
#                 player_stats["FT"] += int(p3.group(3)) - int(p3.group(2))
                #player_stats["FTA"] += int(p3.group(3)) - int(p3.group(2))
#                 player_stats["PTS"] += int(p3.group(3)) - int(p3.group(2))
                player_stats["FTA"] += 1


            #orb
            p3 = orb_pattern.search(event[-1])
            if p3 and p3.group(1) == player:
                player_stats["ORB"] += 1
                player_stats["TRB"] += 1
            
            #drb
            p3 = drb_pattern.search(event[-1])
            if p3 and p3.group(1) == player:
                player_stats["DRB"] += 1
                player_stats["TRB"] += 1

            #ast
            p3 = ast_pattern.search(event[-1])
            if p3 and p3.group(1) == player:
                player_stats["AST"] += 1

            #stl !
            p3 = stl_pattern.search(event[-1])
            if p3 and p3.group(1) == player:
                player_stats["STL"] += 1

            #blk
            p3 = blk_pattern.search(event[-1])
            if p3 and p3.group(1) == player:
                player_stats["BLK"] += 1

            #tov !
            p3 = tov_pattern.search(event[-1])
            if p3 and p3.group(1) == player:
                player_stats["TOV"] += 1

            #pf
            p3 = pf_pattern.search(event[-1])
            if p3 and p3.group(1) == player:
                player_stats["PF"] += 1 
        
        
        #calculate percentages
        if player_stats["FGA"]!=0:
            player_stats["FG%"] = player_stats["FG"]/player_stats["FGA"]
            player_stats["FG%"] = round( player_stats["FG%"], 3)
        
        if player_stats["3PA"]!=0:
            player_stats["3P%"] = player_stats["3P"]/player_stats["3PA"]
            player_stats["3P%"] = round(player_stats["3P%"], 3)

        if player_stats["FTA"]!=0:
            player_stats["FT%"] = player_stats["FT"]/player_stats["FTA"]
            player_stats["FT%"] = round(player_stats["FT%"], 3)
        
        players_data.append(player_stats)
        
    return players_data


def match_to_team(play_by_play, stats_of_players, all_players):
    ret_dict = {"home_team": {"name": play_by_play[0][4], "players_data": []}, 
    "away_team": {"name": play_by_play[0][3], "players_data": []}}

    player_team_hash = {}

    name_pattern = re.compile(r'(\w\. \w+) misses', re.I)
    pf_pattern = re.compile(r'Defensive rebound by (\w\. \w+)', re.I)

    for event in play_by_play:
        p = name_pattern.search(event[-1])
        if p:
            player_team_hash[p.group(1)] = event[2]

        p = pf_pattern.search(event[-1])
        if p:
            player_team_hash[p.group(1)] = event[2]
    
    for stat in stats_of_players:
        if player_team_hash[stat["player_name"]] == play_by_play[0][4]:
            # home player
            ret_dict["home_team"]["players_data"].append(stat)
        else:
            # away player
            ret_dict["away_team"]["players_data"].append(stat)


    return ret_dict


def analyse_nba_game(play_by_play_moves):
    with open(play_by_play_moves) as csv_text:
        text_line = csv.reader(csv_text, delimiter='|')
        play_by_play = [each for each in text_line]

    all_players = find_all_players(play_by_play)
    players_data = all_player_stats(play_by_play, all_players)
    results = match_to_team(play_by_play, players_data, all_players)
    return results

    
def print_nba_game_stats(team_dict):
    print("Players	FG	FGA	FG%	3P	3PA	3P%	FT	FTA	FT%	ORB	DRB	TRB	AST	STL	BLK	TOV	PF	PTS")
    team_total = {"player_name": "Team Totals", "FG": 0, "FGA": 0, "FG%": 0, "3P": 0, "3PA": 0, 
        "3P%": 0, "FT": 0, "FTA": 0, "FT%": 0, "ORB": 0, "DRB": 0, "TRB": 0, 
        "AST": 0, "STL": 0, "BLK": 0, "TOV": 0, "PF": 0, "PTS": 0}

    
    for i in team_dict['players_data']:
        print(i['player_name'],i['FG'],i['FGA'],i['FG%'],i['3P'],i['3PA'],i['3P%'],
              i['FT'],i['FTA'],i['FT%'],i['ORB'],i['DRB'],i['TRB'],i['AST'],
              i['STL'],i['BLK'],i['TOV'],i['PF'],i['PTS'], sep='\t')
        
        team_total["FG"] += i['FG']
        team_total["FGA"] += i['FGA']
        team_total["DRB"] += i['DRB']
        team_total["3P"] += i['3P']
        team_total["3PA"] += i['3PA']
        team_total["FT"] += i['FT']
        team_total["FTA"] += i['FTA']
        team_total["ORB"] += i['ORB']
        team_total["TRB"] += i['TRB']
        team_total["AST"] += i['AST']
        team_total["STL"] += i['STL']
        team_total["BLK"] += i['BLK']
        team_total["TOV"] += i['TOV']
        team_total["PF"] += i['PF']
        team_total["PTS"] += i['PTS']
    
    player_stats = team_total
    if player_stats["FGA"]!=0:
            player_stats["FG%"] = player_stats["FG"]/player_stats["FGA"]
            player_stats["FG%"] = round( player_stats["FG%"], 3)
        
    if player_stats["3PA"]!=0:
            player_stats["3P%"] = player_stats["3P"]/player_stats["3PA"]
            player_stats["3P%"] = round(player_stats["3P%"], 3)

    if player_stats["FTA"]!=0:
            player_stats["FT%"] = player_stats["FT"]/player_stats["FTA"]
            player_stats["FT%"] = round(player_stats["FT%"], 3)

    i = player_stats
    
    print(i['player_name'],i['FG'],i['FGA'],i['FG%'],i['3P'],i['3PA'],i['3P%'],
              i['FT'],i['FTA'],i['FT%'],i['ORB'],i['DRB'],i['TRB'],i['AST'],
              i['STL'],i['BLK'],i['TOV'],i['PF'],i['PTS'], sep='\t')
    
        
        
print_nba_game_stats(analyse_nba_game('nba.txt')['home_team'])


