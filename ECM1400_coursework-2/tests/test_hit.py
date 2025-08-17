import game_engine

def test_hit():
    '''
    Test to see if attack function returns True when hit and False when miss 
    '''
    # Components for attack fucntion to use
    battleship = { "destroyer": 2 }
    board = [["destroyer", "destroyer", None],[None, None, None],[None,None,None]]
    # Coordinates gaurantee a hit
    coordinate_hit = (0,0)
    # Coordinates gaurantee a miss
    coordinate_miss = (1,2)
    # Run the function
    attack_hit = game_engine.attack(coordinate_hit, board, battleship)
    attack_miss = game_engine.attack(coordinate_miss, board, battleship)
    # Check if True is returned
    assert attack_hit is True
    # Check if False is returned
    assert attack_miss is False

