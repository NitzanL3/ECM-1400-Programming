import random
import json

def initialise_board(size=10) -> list[list]:
    '''
    Create the board

    Parameter: 
    size: represents length and width of board

    Returns:
    list of lists: each item in the list is a coordinate on the board 
    '''
    grid = [[None]*size for i in range(size)]
    return grid

def create_battleships(filename = "battleships.txt") -> dict:
    '''
    Create the battleships

    Paramater: 
    Filename: a text file with battleship names and their corresponding sizes

    Return:
    dictionary: battleship names as keys and corresponding battleship sizes as values 
    '''
    try:
        battleships = {}
        with open(filename, "r") as f:
            for line in f:
                (names, sizes) = line.strip().split(":")
                battleships[names] = int(sizes)
        return battleships
    except FileNotFoundError:
        print("Unable to create battleships, text file with ship names and sizes is required.")
        with open("log.txt", "a") as f:
                f.write("[ERROR] Unable to create battleships, text file with Ship names and sizes is required.\n")

def place_battleships(board, ships, algorithm = "simple") -> list[list]:
    '''
    Place the battleships on the board

    Parameters:
    board: list of lists full of None values 
    ships: dictionary with ship names as keys and ship sizes as values 
    algorithm: identifier for type of placement  

    Return:
    board: list of lists with ship names as items and None values 
    '''
    if algorithm == "simple":
        # Horizontal placement with each ship in a different row
        index = 0
        for ship_names, ship_sizes in ships.items():
            for i in range(ship_sizes):
                board[index][i] = ship_names
            index += 1
        return board
    elif algorithm == "random":
        with open("log.txt", "a") as f:
                f.write("[INFO] Battleships have been placed randomly.\n")
        return place_battleships_random(board, ships)
    elif algorithm == "custom":
        with open("log.txt", "a") as f:
                f.write("[Info] Battleships have been placed according to a placment.config file.\n")
        return place_battleships_custom(board, ships)

def place_battleships_random(board, ships) -> list[list]:
    '''
    Place battleships randomly 
    '''
    for ship_names, ship_sizes in ships.items():
        placed = False

        while not placed:
            # Random choice between horizontal and vertical orientation
            orientation = random.choice(["Horizontal", "Vertical"])

            # Pick random coordinate according to the orientation and ship size
            if orientation == "Horizontal":
                x = random.randint(0, 9 - ship_sizes)
                y = random.randint(0, 9)
                if all(board[y][x+i] is None for i in range (ship_sizes)):
                    for j in range(ship_sizes):
                        board[y][x + j] = ship_names
                    placed = True
            elif orientation == "Vertical":
                x = random.randint(0, 9)
                y = random.randint(0, 9 - ship_sizes)
                if all(board[y+i][x] is None for i in range (ship_sizes)):
                    for j in range(ship_sizes):
                        board[y+j][x] = ship_names
                    placed = True
    return board


def place_battleships_custom(board, ships) -> list[list]:
    '''
    Place battleships according to a placement configuration file, placement.json
    '''
    try:
        # Open the json file
        with open("placement.json", "r") as f:
            # Convert file into a dictionary
            custom_placement = json.load(f)
    except FileNotFoundError:
        print("Custom placement unavailable. We have placed the battleships for you!")
        with open("log.txt", "a") as f:
                f.write("[ERROR] Custom placement unavailable.\n")
        # If no file present carry on game with random placement
        return place_battleships(board, ships, algorithm="random")
    # Place battleships according to dictionary
    for ship_names, ship_sizes in ships.items():
        x, y, orientation = custom_placement[ship_names]
        y = int(y)
        x = int(x)
        if orientation == "h":
            for i in range(ship_sizes):
                board[y][x + i] = ship_names
        elif orientation == "v":
            for i in range(ship_sizes):
                board[y + i][x] = ship_names
    return board

