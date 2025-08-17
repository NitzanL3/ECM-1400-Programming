# Battleships Game 
## Author (candidate number): 133792

This project is a battleships game in which a player can play against an AI opponent. 
It consists of a 10x10 board and 5 battleships that vary in sizes.
The game ends when all battleships have been sunk.

#### To Play the Game:
- Run the main.py python file and follow the link http://127.0.0.1:5000
- Input '/placement' after the url to begin the game 
- Select the battleship location and hit send board 
- Register your attack by clicking a square on the empty board displayed 
- This point will turn red for a hit or blue for a miss
- The AI's turn can be seen in the game log and the player board on the right
- A message will be displayed when all battleships have been sunk

#### My Contribution: 
- Beyond the specification i created my own function called board_state used to check when the game has ended 
- This function can be found in game_engine.py
- I added three tests to my project that can be found in the tests folder
- I have also added log file called log.txt which displays ERROR messages and INFO messages
- I attempted to imporve my AI with the function generate_attack_hard found in mp_game_engine.py 
(this function contained some bugs so I excluded it from main.py) 
 

#### Installation 
- pytest 
- flask

#### Licensing:
Distributed under the MIT License. See License.txt for more information.

