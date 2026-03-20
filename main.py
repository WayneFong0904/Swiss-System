import random

class player:
    def __init__(self, num):
        self.name = 'Player ' + str(num + 1)
        self.point = 0
        self.bye = False
        self.was_bye = False
    
    def get_point(self):
        return self.point
    
    def add_point(self, num):
        self.point += num
        self.point = float(self.point)
    
    def is_bye(self):
        return self.bye
    
    def set_bye(self):
        self.bye = not self.bye

    def get_was_bye(self):
        return self.was_bye

    def set_was_bye(self):
        self.was_bye = True

#Sort player based on point
def sort_players(players):
    
    iteration = len(players)
    temp_players = players

    for i in range(iteration):
        for j in range(iteration):
            if i == j:
                continue
            if temp_players[i].get_point() > temp_players[j].get_point():
                temp = temp_players[j]
                temp_players[j] = temp_players[i]
                temp_players[i] = temp

    return temp_players

def display_match_info(left_players, right_players, g_turn):
    
    #This is needed for the first match (left & right do not have the same number of player)
    #This section of code can be improved with some proper modification in first_game() function
    num_of_mathces = min(len(left_players), len(right_players))
    
    print("\n" + "#"*10 + " Match " + str(g_turn) + " " + "#"*10)

    for i in range(num_of_mathces):
        print(left_players[i].name, "VS", right_players[i].name)

    print("#"*10 + " Match " + str(g_turn) + " " + "#"*10)

def print_result(players, g_turn):
    result = sort_players(players)
    print("\n" + "#"*10 + " Result of Game " + str(g_turn) + " " + "#"*10)

    for i in result:
        if i.is_bye():
            print(i.name + " has " + str(i.point) + " (bye player)")
            #Reset current bye player into a normal player
            i.set_bye()
        else:
            print(i.name + " has " + str(i.point))

    print("#"*10 + " Result of Game " + str(g_turn) + " " + "#"*10)

    return result

#Initialize players
def initialize_players(num_of_players):
    if num_of_players == 0:
        return None
    
    participants = []

    for i in range(num_of_players):
        p = player(i)
        participants.append(p)
    
    return participants

#Swiss System simulation (For the first match)
def first_game(players):
    #Check if number of player is odd number
    if len(players) % 2 != 0:
        left_players = []
        right_players = []

        counter = 0

        #Sort player into left and right
        for i in players:
            if counter % 2 == 0:
                left_players.append(i)
            else:
                right_players.append(i)
            counter += 1
        
        #Set a player as bye.
        #The last player in list will always be bye player
        #The last player will always be located in right_players list
        #The code below is just for a safety measurement
        if len(left_players) > len(right_players):
            bye_player = len(left_players) - 1
            left_players[bye_player].add_point(1)
            left_players[bye_player].set_bye()
            left_players[bye_player].set_was_bye()
        else:
            bye_player = len(right_players) - 1
            right_players[bye_player].add_point(1)
            right_players[bye_player].set_bye()
            right_players[bye_player].set_was_bye()

        iteration = min(len(left_players), len(right_players))

        #Simulates a game of win/lose/tie
        for i in range(iteration):
            probability_of_game = random.randint(0, 99)
            if probability_of_game <= 33:
                left_players[i].add_point(1)
            elif probability_of_game >= 66:
                right_players[i].add_point(1)
            else:
                left_players[i].add_point(0.5)
                right_players[i].add_point(0.5)
        
        #Display the opponents in all the matches
        display_match_info(left_players, right_players, 1)

        result = []
        result.extend(left_players)
        result.extend(right_players)

        #Show result here, put a function here print_result(player list)
        updated_result = print_result(result, 1)
        
        return updated_result
    else:
        print("The number of players is not odd! Program is terminated!")
        exit()

#Swiss System simulation (For after the first match)
def n_game(players, num_of_game):
    
    #number of game cannot be greater than number of players
    #because this will cause infinite loop
    if num_of_game > len(players):
        num_of_game = len(players)

    #Go for the first game
    player_list = first_game(players)

    #Go for the n + 1 game
    player_list_size = len(player_list)
    game_turn = num_of_game - 1

    #Set current game's bye player
    for i in range(game_turn):
        n_player = random.randint(0, player_list_size - 1)
        left_players = []
        right_players = []
        counter = 0
        current_bye_player = None

        #To eliminate the possibility of n_player becomes "< 0" or "> list size"

        while player_list[n_player].get_was_bye():
            n_player = random.randint(0, player_list_size - 1)
        else:
            player_list[n_player].set_bye()
            player_list[n_player].add_point(1)
            player_list[n_player].set_was_bye()
            current_bye_player = player_list[n_player]

        #Remove the bye player (temporarily)
        for p in range(player_list_size):
            if player_list[p].is_bye():
                player_list.pop(p)
                break

        #Sort players into left and right
        for p in player_list:
            if counter % 2 == 0:
                left_players.append(p)
            elif counter % 2 != 0:
                right_players.append(p)
            counter += 1

        #left and right should have the same number of people
        iteration = len(left_players)

        #Simulates a game of win/lose/tie
        for ite in range(iteration):
            probability_of_game = random.randint(0, 99)
            if probability_of_game <= 33:
                left_players[ite].add_point(1)
            elif probability_of_game >= 66:
                right_players[ite].add_point(1)
            else:
                left_players[ite].add_point(0.5)
                right_players[ite].add_point(0.5)

        #Display the opponents in all the matches
        display_match_info(left_players, right_players, i + 2)

        #Regroup every player
        temp_player_list = []
        temp_player_list.append(current_bye_player)
        temp_player_list.extend(left_players)
        temp_player_list.extend(right_players)

        #Display game results and update player's information
        player_list = print_result(temp_player_list, i + 2)

    return None



player_list = initialize_players(19)
n_game(player_list, 5)  #-> This will show everything
print()  #-> Just to make the output cleaner