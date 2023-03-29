# DEFINE YOUR LEAGUE ID
league_ID = "INSERT LEAGUE ID"
path_to_private_json = "INSERT PATH TO 'private.json' FILE"





# Importing packages and files
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
from pathlib import Path
from yfpy.query import YahooFantasySportsQuery
from yfpy.models import Roster
import matplotlib.pyplot as plt


# Declaring Variable:
weekly_roster = []
weekly_rosters = []
x_axis = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
y_Cover2 = []
y_StackedBox = []
y_Cover3 = []
y_DimeNDisguise = []


# Initializing Authentication
sc = OAuth2(None, None, from_file='private.json')
game = yfa.Game(sc, 'nfl')
league = yfa.League(sc, league_ID)
query = YahooFantasySportsQuery(Path(path_to_private_json), league_id={league_ID})



# Defining Functions

    # Determine desired team number
def Get_team_num():
    print()
    print('Which number would you like to see stats for?')
    print()
    team_num = input(">>")
    # Checks if team_num is an integer between 0 and 12
    if team_num.isdigit() and 1 <= int(team_num) <= len(teams):
        return team_num
    else:
        print('not acceptable team number')
        return Get_team_num()

    # Retrieve player_keys of the starting players each week up to current week
def retrieveStats(team_num):
    week_number = 1
    team_number = team_num
    while week_number <= league.current_week():
        get_roster = query.query(
            f"https://fantasysports.yahooapis.com/fantasy/v2/team/{league_ID}.t.{team_number}/roster;week={week_number}",
            ["team", "roster"],
            Roster
        )
        for player in get_roster.players:
            if player["player"].selected_position.position != "BN" and player["player"].selected_position.position != "IR":
                weekly_roster.append(player["player"].player_key)
        weekly_rosters.append(weekly_roster.copy())
        weekly_roster.clear()
        week_number += 1
    return weekly_rosters


# Print Team Names
teams = query.query(
    f"https://fantasysports.yahooapis.com/fantasy/v2/league/{league_ID}/teams",
    ["league", "teams"]
)
x = 1
print(); print();
for team in teams:
    print(f'{x}' + ": " + team['team'].managers['manager'].nickname)
    x += 1


# Choosing Team and Retrieving Stats
team_num = Get_team_num()
nick_name = str(teams[int(team_num) - 1]['team'].managers['manager'].nickname)
Player_Keys = retrieveStats(team_num)


chosen_week = 1
for week in Player_Keys:
    for player in week:
        player_key = player
        player_stats = query.query(
            f"https://fantasysports.yahooapis.com/fantasy/v2/league/{league_ID}/players;"
            f"player_keys={player_key}/stats;type=week;week={chosen_week}",
            ["league", "players", "0", "player"],
            
        )
        
        # Cover 2
        tempx = 0
        if player_stats['display_position'] == 'WR':
            for statx in player_stats['player_stats'].stats:
                if statx['stat'].stat_id == "12":
                    if len(y_Cover2) > chosen_week-1:
                        tempx = y_Cover2[chosen_week-1]
                        y_Cover2.pop(chosen_week-1)
                    y_Cover2.append(tempx + int(statx['stat'].value) * 0.1 * 0.4)
                    break         
        if player_stats['display_position'] == 'RB' or player_stats['display_position'] == 'TE':
            for statx in player_stats['player_stats'].stats:
                if statx['stat'].stat_id == "12":
                    if len(y_Cover2) > chosen_week-1:
                        tempx = y_Cover2[chosen_week-1]
                        y_Cover2.pop(chosen_week-1)
                    y_Cover2.append(tempx - int(statx['stat'].value) * 0.1 * 0.3)
                    break
        
        # Stacked Box
        tempx = 0
        if player_stats['display_position'] != 'QB':
            for statx in player_stats['player_stats'].stats:
                if statx['stat'].stat_id == "9":
                    if len(y_StackedBox) > chosen_week-1:
                        tempx = y_StackedBox[chosen_week-1]
                        y_StackedBox.pop(chosen_week-1)
                    y_StackedBox.append(tempx + int(statx['stat'].value) * 0.1 * 0.5)
                    break         
        if player_stats['display_position'] == 'WR':
            for statx in player_stats['player_stats'].stats:
                if statx['stat'].stat_id == "12":
                    if len(y_StackedBox) > chosen_week-1:
                        tempx = y_StackedBox[chosen_week-1]
                        y_StackedBox.pop(chosen_week-1)
                    y_StackedBox.append(tempx - int(statx['stat'].value) * 0.1 * 0.2)
                    break  
        
        # Cover 3
        tempx = 0
        for statx in player_stats['player_stats'].stats:
            if statx['stat'].stat_id == "12":
                if len(y_Cover3) > chosen_week-1:
                    tempx = y_Cover3[chosen_week-1]
                    y_Cover3.pop(chosen_week-1)
                y_Cover3.append(tempx + int(statx['stat'].value) * 0.1 * 0.25)
                break         
        if player_stats['display_position'] != 'QB':
            for statx in player_stats['player_stats'].stats:
                if statx['stat'].stat_id == "9":
                    if len(y_Cover3) > chosen_week-1:
                        tempx = y_Cover3[chosen_week-1]
                        y_Cover3.pop(chosen_week-1)
                    y_Cover3.append(tempx - int(statx['stat'].value) * 0.1 * 0.2)
                    break 
                
        # Dime 'N Disguise
        tempx = 0
        for statx in player_stats['player_stats'].stats:
            if statx['stat'].stat_id == "4":
                if len(y_DimeNDisguise) > chosen_week-1:
                    tempx = y_DimeNDisguise[chosen_week-1]
                    y_DimeNDisguise.pop(chosen_week-1)
                y_DimeNDisguise.append(tempx + int(statx['stat'].value) * 0.04 * 0.25)
                break
        for statx in player_stats['player_stats'].stats:
            if statx['stat'].stat_id == "5":
                if len(y_DimeNDisguise) > chosen_week-1:
                    tempx = y_DimeNDisguise[chosen_week-1]
                    y_DimeNDisguise.pop(chosen_week-1)
                y_DimeNDisguise.append(tempx + int(statx['stat'].value) * 6 / 3)
                break
        for statx in player_stats['player_stats'].stats:
            if statx['stat'].stat_id == "6":
                if len(y_DimeNDisguise) > chosen_week-1:
                    tempx = y_DimeNDisguise[chosen_week-1]
                    y_DimeNDisguise.pop(chosen_week-1)
                y_DimeNDisguise.append(tempx + int(statx['stat'].value) * 2 * 1)
                break
        for statx in player_stats['player_stats'].stats:
            if statx['stat'].stat_id == "9":
                if len(y_DimeNDisguise) > chosen_week-1:
                    tempx = y_DimeNDisguise[chosen_week-1]
                    y_DimeNDisguise.pop(chosen_week-1)
                y_DimeNDisguise.append(tempx - int(statx['stat'].value) * 0.1 * 0.25)
                break 
                
    # End of Scheme Corrections for this week
    chosen_week += 1
 
#Creating and Showing the Chart               
plt.style.use('bmh')
plt.plot(x_axis, y_Cover2, label = "Cover 2", linewidth=4, color='black')
plt.plot(x_axis, y_StackedBox, label = "Stacked Box", linewidth=4, color='darkblue')
plt.plot(x_axis, y_Cover3, label = "Cover 3", linewidth=4, color='blue')
plt.plot(x_axis, y_DimeNDisguise, label = "Dime 'N Disguise", linewidth=4, color='lightblue')
plt.title("Defensive Scheme Influence on " + nick_name + "'s Team")
plt.xlabel('Week')
plt.ylabel('Fantasy Points Deducted By Scheme')
plt.legend()
plt.show()
                
