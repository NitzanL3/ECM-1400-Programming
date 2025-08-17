import components

def attack(coordinates, board, battleships) -> bool:
    '''
    Register attack on the board 

    Parameters:
    coordinates: tuple containing two inetegers 
    board: list of lists containing ship names and None values 
    battleships: dictionary containing ship names as keys and ship sizes as values 

    Return:
    True or False determined by hit or a miss
    '''
    # Convert the tuple into a list so it is iterable
    loc = []
    loc.append(coordinates)

    for (x, y) in loc:
        # If battleship is present
        if board[y][x] is not None:
            name = board[y][x]
            # Decrement size value in dictionary
            battleships[name] -= 1
            # Change loaction in board to None
            board[y][x] = None
            # Notify user that they hit the battleship
            print("Hit!")
            # Check if battleship has been sunk
            if battleships[name] == 0:
                # Notify user that thier battleship has been sunk
                print("The {} has been sunk!".format(name))
            with open("log.txt", "a") as f:
                f.write("[INFO] Attack has been registered: HIT\n")
            return True
        else:
            print("Miss!")
            with open("log.txt", "a") as f:
                f.write("[INFO] Attack has been registered: MISS\n")
            return False

def cli_coordinates_input() -> (int,int):
    '''
    Ask the user to input coordinates 

    Return:
    tuple: containing two integers representing x and y values 
    '''
    coordinates = ()
    while True:
        try:
            # Assign inetger to x
            x = int(input("enter x coordinate: "))
            # Assign integer to y
            y = int(input("enter y coordinate: "))
            if x > 10 or y > 10:
                # Account for out of range coordinate
                raise ValueError
            # Reduce x and y values by 1 to account for indexing in lists
            coordinates = (x - 1, y - 1)
            with open("log.txt", "a") as f:
                f.write("[INFO] User has input coordinates.\n")
            return coordinates
        # Account for incorrect input
        except ValueError:
            print("Invalid input! Enter a number between 1 and 10.")
            # Add error to log file
            with open("log.txt", "a") as f:
                f.write("[ERROR] Invalid input! Enter a number between 1 and 10.\n")

def simple_game_loop ():
    '''
    function for intermediate manual testing
    '''
    # Components of game
    board = components.initialise_board(size=10)
    ships = components.create_battleships()

    # Place battelship on board
    components.place_battleships(board, ships)

    print("Welcome to Battleships!")

    # Check board continously until no battleships remain
    while board_state(board) is False:
        coordinates = cli_coordinates_input()
        attack(coordinates, board, ships)
    print("Game Over!")

def board_state(board) -> bool:
    '''
    Check if game is finsihed 

    Parameter:
    board: list of lists full of ship names and None values 

    Return:
    True: if game is finished
    False: if game is active
    '''
    # Iterate through list of lists
    for y in range(0,9):
        for x in range(0,9):
            # Check if ship names are present
            if board[y][x] is not None:
                return False
    with open("log.txt", "a") as f:
        f.write("[INFO] Game over.\n")      
    return True

if __name__ == "__main__":
    simple_game_loop()