import random
import components
import game_engine

# Players dictionary in global namespace
players = {}

def initialise_players(username, board, battleships):
    '''
    Store the player info in a dictionary in the global namespace 

    Parameters:
    username: string with player username
    board: list of lists with ship names and None values 
    battleships: dictionary with ship names as keys and ship sizes as values
    '''
    global players
    board = components.initialise_board(size=10)
    battleships = components.create_battleships()
    players[username] = { "board" : board, "battleships" : battleships }

def generate_attack()-> (int,int):
    '''
    Generate AI coordinates 
    '''
    # Random number generator for x and y values
    x = random.randint(0,9)
    y = random.randint(0,9)
    coordinates = (x,y)
    with open("log.txt", "a") as f:
        f.write("[INFO] AI has input coordinates.\n")
    return coordinates

# Store used AI coordinates in global namespace so AI can keep track
used_coordinates = []
# initialise AI attack so AI can idenify whether it hit or miss
AI_attack = False

def generate_attack_hard(AI_attack) -> (int,int):
    '''
    Imporved AI:
    AI doesn't repeat coordinates
    AI targets localised area when registering a hit
    '''
    global used_coordinates
    try:
        # Identify last coordinates used
        previous_coordinates = (used_coordinates[-1])
        # If last coordinates hit 
        if AI_attack is True:
            # Convert tupple into list so it is iterable 
            hit = []
            hit.append(previous_coordinates)
            for x, y in hit:
                attack = False
                while attack is False:
                    # AI decides to attack ship vertically or horizontally
                    orientation = random.choice(["Horizontal", "Vertical"])
                    if orientation == "Horizontal":
                        # Attack nearby x coorddinate on same row
                        # Account for out of range coordinates
                        if x == 0:
                            new_x = 1
                        elif x == 9:
                            new_x = 8
                        else:
                            new_x = random.randint(x-1,x+1)       
                        coordinates = (new_x,y)
                        # Ensure AI doesn't repeat coordinates
                        if coordinates not in used_coordinates:
                            # Keep track of used coordinates by adding new coordinates to list
                            used_coordinates.append(coordinates)
                            attack = True
                            with open("log.txt", "a") as f:
                                f.write("[INFO] AI has input coordinates.\n")
                                return coordinates 
                    elif orientation == "Vertical":
                        # Attack nearby y coordinate in same column
                        # Account for out of range coordinates
                        if y == 9:
                            new_y = 8
                        elif y == 0:
                            new_y = 1  
                        else:
                            new_y = random.randint(y-1, y+1)
                        coordinates = (x,new_y)
                        # Ensure AI doesn't repeat coordinates
                        if coordinates not in used_coordinates:
                            # Keep track of used coordinates by adding new coordinates to list
                            used_coordinates.append(coordinates)
                            attack = True
                            with open("log.txt", "a") as f:
                                f.write("[INFO] AI has input coordinates.\n")
                            return coordinates
                    # Allow an escape for the while loop if all nearby coordinates have been used
                    elif ((x-1,y) in used_coordinates or x-1<0) and ((x+1,y) in used_coordinates or x+1>9) and ((x,y-1) in used_coordinates or y-1<0) and ((x,y+1) in used_coordinates or y+1>9):
                        while True:
                            x = random.randint(0,9)
                            y = random.randint(0,9)
                            coordinates = (x,y)
                            # Ensure AI doesn't repeat coordinates
                            if coordinates not in used_coordinates:
                                # Keep track of used coordinates by adding new coordinates to list
                                used_coordinates.append(coordinates)
                                attack = True
                                with open("log.txt", "a") as f:
                                    f.write("[INFO] AI has input coordinates.\n")
                                return coordinates              
        # If last coordinates missed genrate new radndom coordinates
        else:
            while True:
                x = random.randint(0,9)
                y = random.randint(0,9)
                coordinates = (x,y)
                # Ensure AI doesn't repeat coordinates
                if coordinates not in used_coordinates:
                    # Keep track of used coordinates by adding new coordinates to list
                    used_coordinates.append(coordinates)
                    with open("log.txt", "a") as f:
                        f.write("[INFO] AI has input coordinates.\n")
                    return coordinates
    
    # Account for initial error as list of used coordinates contains no items
    except IndexError:
        with open("log.txt", "a") as f:
                f.write("[ERROR] Cannot index used coordinate list if none are present.\n")
        while True:
                x = random.randint(0,9)
                y = random.randint(0,9)
                coordinates = (x,y)
                if coordinates not in used_coordinates:
                    used_coordinates.append(coordinates)
                    with open("log.txt", "a") as f:
                        f.write("[INFO] AI has input coordinates.\n")
                    return coordinates

def ai_opponent_game_loop():
    '''
    Player vs AI game in terminal 
    '''
    print("Welcome to Battleships!")
    # Initialise player components
    player_board = components.initialise_board()
    player_ships = components.create_battleships()

    # Place player battleships on player board
    components.place_battleships(player_board,player_ships, algorithm="custom")

    # Initialise AI components
    AI_board = components.initialise_board()
    AI_ships = components.create_battleships()

    # Place AI battleships on AI board
    components.place_battleships(AI_board, AI_ships, algorithm="random")

    # Initialise players
    initialise_players("Player_1", player_board, player_ships)
    initialise_players("AI", AI_board, AI_ships)

    # Check player and AI board to see if any battleships remain
    player_active = game_engine.board_state(player_board)
    AI_active = game_engine.board_state(AI_board)
    
    while player_active is False and AI_active is False:
        player_coordinates = game_engine.cli_coordinates_input()
        game_engine.attack(player_coordinates, AI_board, AI_ships)
        AI_coordinates = generate_attack()
        game_engine.attack(AI_coordinates, player_board, player_ships)
        print(player_board)

    # Display message depending if player won or lost
    if player_active is True:
        print("You won!")
    else:
        print("You lost!")

if __name__ == "__main__":
    ai_opponent_game_loop()
