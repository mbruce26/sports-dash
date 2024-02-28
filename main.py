from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import boxscoretraditionalv3
from prettytable import PrettyTable

def format_box_score(box_score):
    table = PrettyTable()

    # Define columns
    table.field_names = ["Player", "Position", "Minutes", "FGM", "FGA", "FG%", "3PM", "3PA", "3P%", "FTM", "FTA", "FT%", "Reb", "Ast", "Stl", "Blk", "TO", "PF", "Pts", "+/-"]

    # Extract player statistics
    for player in box_score["homeTeam"]["players"]:
        stats = player["statistics"]
        table.add_row([
            f"{player['firstName']} {player['familyName']}",
            player["position"],
            stats["minutes"],
            stats["fieldGoalsMade"],
            stats["fieldGoalsAttempted"],
            stats["fieldGoalsPercentage"],
            stats["threePointersMade"],
            stats["threePointersAttempted"],
            stats["threePointersPercentage"],
            stats["freeThrowsMade"],
            stats["freeThrowsAttempted"],
            stats["freeThrowsPercentage"],
            stats["reboundsTotal"],
            stats["assists"],
            stats["steals"],
            stats["blocks"],
            stats["turnovers"],
            stats["foulsPersonal"],
            stats["points"],
            stats["plusMinusPoints"]
        ])

    # Print the formatted table
    print(table)
    
    table = PrettyTable()

    # Define columns
    table.field_names = ["Player", "Position", "Minutes", "FGM", "FGA", "FG%", "3PM", "3PA", "3P%", "FTM", "FTA", "FT%", "Reb", "Ast", "Stl", "Blk", "TO", "PF", "Pts", "+/-"]

    # Extract player statistics
    for player in box_score["awayTeam"]["players"]:
        stats = player["statistics"]
        table.add_row([
            f"{player['firstName']} {player['familyName']}",
            player["position"],
            stats["minutes"],
            stats["fieldGoalsMade"],
            stats["fieldGoalsAttempted"],
            stats["fieldGoalsPercentage"],
            stats["threePointersMade"],
            stats["threePointersAttempted"],
            stats["threePointersPercentage"],
            stats["freeThrowsMade"],
            stats["freeThrowsAttempted"],
            stats["freeThrowsPercentage"],
            stats["reboundsTotal"],
            stats["assists"],
            stats["steals"],
            stats["blocks"],
            stats["turnovers"],
            stats["foulsPersonal"],
            stats["points"],
            stats["plusMinusPoints"]
        ])

    # Print the formatted table
    print(table)
    

def format_game_data(game_data):
    # Create a PrettyTable instance
    table = PrettyTable(["Game Information", "Team", "1","2","3","4","Final Score"])
    
    home_name = game_data["homeTeam"]["teamTricode"]
    away_name = game_data["awayTeam"]["teamTricode"]

    home_1 = game_data["homeTeam"]["periods"][0]["score"]
    away_1 = game_data["awayTeam"]["periods"][0]["score"]

    home_2 = game_data["homeTeam"]["periods"][1]["score"]
    away_2 = game_data["awayTeam"]["periods"][1]["score"]

    home_3 = game_data["homeTeam"]["periods"][2]["score"]
    away_3 = game_data["awayTeam"]["periods"][2]["score"]

    home_4 = game_data["homeTeam"]["periods"][3]["score"]
    away_4 = game_data["awayTeam"]["periods"][3]["score"]

    home_final = game_data["homeTeam"]["score"]
    away_final = game_data["awayTeam"]["score"]

    # Add rows to the table
    table.add_row(["Home Team", home_name, home_1, home_2, home_3, home_4, home_final])
    table.add_row(["Away Team", away_name, away_1, away_2, away_3, away_4, away_final])
    
    # Set the alignment
    table.align["Game Information"] = "c"
    table.align["Team"] = "c"
    table.align["1"] = "c"
    table.align["2"] = "c"
    table.align["3"] = "c"
    table.align["4"] = "c"
    table.align["Final Score"] = "c"

    # Print the table
    print(table)

def get_team_tricode(team):
    nba_teams = {
        "hawks": "ATL",
        "celtics": "BOS",
        "nets": "BKN",
        "hornets": "CHA",
        "bulls": "CHI",
        "cavaliers": "CLE",
        "mavericks": "DAL",
        "nuggets": "DEN",
        "pistons": "DET",
        "warriors": "GSW",
        "rockets": "HOU",
        "pacers": "IND",
        "clippers": "LAC",
        "lakers": "LAL",
        "grizzlies": "MEM",
        "heat": "MIA",
        "bucks": "MIL",
        "timberwolves": "MIN",
        "pelicans": "NOP",
        "knicks": "NYK",
        "thunder": "OKC",
        "magic": "ORL",
        "sixers": "PHI",
        "suns": "PHX",
        "blazers": "POR",
        "kings": "SAC",
        "spurs": "SAS",
        "raptors": "TOR",
        "jazz": "UTA",
        "wizards": "WAS"
    }
    tricode = nba_teams.get(team)
    if tricode:
        return tricode
    else:
        raise KeyError("That's not a valid NBA team")

def main():
    games = scoreboard.ScoreBoard().get_dict()

    # print(json.dumps(games, indent=2))
    while True:
        try:
            team = input("Choose an NBA Team: ")
            if not team:
                team = "rockets"
                
            teamTricode = get_team_tricode(team)
        except KeyError:
            continue

    # current game
    rox_board = [game for game in games["scoreboard"]["games"] if game["homeTeam"]["teamTricode"] == "HOU" or game["awayTeam"]["teamTricode"] == "HOU"]
    
    if len(rox_board) > 0:

        game_data = rox_board[0]
        
        format_game_data(game_data)

        players = boxscoretraditionalv3.BoxScoreTraditionalV3(game_data["gameId"]).get_dict()

        format_box_score(players["boxScoreTraditional"])
    else:
        print(f"No {team} game today")

if __name__ == "__main__":
    main()
