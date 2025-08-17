import json
from flask import Flask, jsonify, request, render_template
import components
import mp_game_engine
import game_engine

app = Flask(__name__)

# Initialise components
board_size = 10
board = components.initialise_board(board_size)
ships = components.create_battleships(filename = "battleships.txt")

# Player components
Player_board = components.initialise_board(board_size)
player_ships = components.create_battleships(filename = "battleships.txt")
initialised_player_board = []

# AI components
AI_board = components.initialise_board(board_size)
AI_ships = components.create_battleships(filename = "battleships.txt")
initialised_AI_board = []

@app.route('/placement', methods=['GET', 'POST'])
def placement_interface():
    '''
    Render player battleship custom placement and send AI board to front end 
    '''
    global initialised_player_board
    global initialised_AI_board


    if request.method == 'GET':
        return render_template('placement.html', ships=ships, board_size=board_size)

    if request.method == 'POST':
        # Place AI battleships on AI board
        initialised_AI_board = components.place_battleships(AI_board , AI_ships, algorithm="random")

        # Update placement.json
        custom_placement = request.get_json()
        with open("placement.json", "w") as f:
            json.dump(custom_placement, f)

        # Place player battleships on player board
        initialised_player_board = components.place_battleships(Player_board, player_ships, algorithm="custom")
        return jsonify({'message': 'Received'}), 200

@app.route('/', methods=['GET'])
def root():
    '''
    Send player board to main.html
    '''
    global initialised_AI_board
    return render_template('main.html', player_board=initialised_player_board)

@app.route('/attack', methods=['GET'])
def attack():
    '''
    Accepts get request containing two parameters x and y
    Registers player and AI attacks until game finishes
    '''
    global initialised_player_board, initialised_AI_board

    # Get player coordinates 
    if request.args:
        x = int(request.args.get("x"))
        y = int(request.args.get("y"))
        player_coordinates = (x,y)

        # Check if player hit or miss as True or False assigned to hit identifier
        hit = game_engine.attack(player_coordinates, initialised_AI_board, AI_ships)
        
        # Generate AI coordinates
        AI_Turn = mp_game_engine.generate_attack()

        # Check if AI hit or miss returning True or False accordingly
        game_engine.attack(AI_Turn, initialised_player_board, player_ships)

        # initialise board_state function to check the player and AI board
        player_board_empty = game_engine.board_state(initialised_player_board)
        AI_board_empty = game_engine.board_state(initialised_AI_board)

        # If game is over return an appropriate message 
    if player_board_empty is True:
        return jsonify({"hit": hit, "AI_Turn": AI_Turn, "finished": "Unlucky, all your battleships have been sunk!"})
    elif AI_board_empty is True:
        return jsonify({"hit": hit, "AI_Turn": AI_Turn, "finished": "Congratulations, you won!"})
        # If game is not over then proceed with the loop
    else:
        return jsonify({"hit": hit, "AI_Turn": AI_Turn})
        
if __name__ == "__main__":
    app.run()