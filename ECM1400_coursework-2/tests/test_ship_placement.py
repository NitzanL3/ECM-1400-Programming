import components

def test_placement():
    '''
    Test to see if place_battleships fucntion places battleships for the simple algorithm 
    '''
    # Components for attack fucntion to use
    ships = { "destroyer": 2, "cruiser": 3, "ship": 1}
    board = [[None, None, None],[None, None, None],[None,None,None]]
    # Run the function
    placement = components.place_battleships(board, ships, algorithm = "simple")
    # Check to see if placement is in the desired pattern
    assert placement == [["destroyer", "destroyer", None],["cruiser", "cruiser", "cruiser"],["ship",None,None]]

def test_algorithm():
    '''
    Test to see if place_battleships changes the placement algorithm
    '''
    # Components for attack fucntion to use
    board = components.initialise_board()
    ships = components.create_battleships()
    # Run the function with random algorithm
    random_placement = components.place_battleships(board, ships, algorithm = "random")
    # Check if random function is used
    assert random_placement == components.place_battleships_random(board, ships)
    # Run the function with the custom algorithm
    custom_placement = components.place_battleships(board, ships, algorithm = "custom")
    # Check if custom function is used
    assert custom_placement == components.place_battleships_custom(board, ships)