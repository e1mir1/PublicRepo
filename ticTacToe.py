#! python3
# ticTacToe.py - A simple Tic Tac Toe game I built while learning Python with Automate the Boring Stuff.

# Winning Rules:
# to win you need at least board_width amount of moves
# if all your board_width moves share the same x or y coords  //catches vertical/horizontal moves 
# if all your board_width moves have there x == y or x + y == board_width + 1  // catches diagonal moves 

import random, time
import pyinputplus as pyip


#### build theBoard in different sizes depending on board_width
def build_board():
   global theBoard, board_width, mapOfCoords
   board_width = 3
   theBoard = {}

   span = board_width * board_width
   for i in range(span):
       theBoard.setdefault(i+1, str(i+1))  #+1 cuz range start at 0 and exclude span

   #compute it once and make it sharable for other function
   mapOfCoords = map_coords()


#### it maps the coords for each position in the board
def map_coords(): 
    coord_map = {}   

    x, y = 1, 1    #the start coord which is the same as key -> 1: (1, 1) 
    for key in theBoard:
        coord_map.setdefault(key, (x, y))
        x += 1
        if key % board_width == 0:
            x = 1   #back to start in next column (y)
            y += 1

    return coord_map
    

#### find the link between moves_list if there is and return the missing move 
def link_moves(moves_list):
    #find the link between moves_list
    #use that link (x|y) to find the next move that share same link
    link_x = {}
    link_y = {}
    diagonal_link = {'\\': [], '/': []}

    for move in moves_list:
        link_x.setdefault(mapOfCoords[move][0], [])
        link_x[mapOfCoords[move][0]].append(move)
        link_y.setdefault(mapOfCoords[move][1], [])
        link_y[mapOfCoords[move][1]].append(move)

        if mapOfCoords[move][0] == mapOfCoords[move][1]:
            diagonal_link['\\'].append(move)
        if mapOfCoords[move][0] + mapOfCoords[move][1] == board_width + 1:
            diagonal_link['/'].append(move)

    next_link = []
    for k, v in mapOfCoords.items():
        if v[0] in link_x and len(link_x[v[0]]) == board_width - 1 and k not in link_x[v[0]]:
            next_link.append(k)
        if v[1] in link_y and len(link_y[v[1]]) == board_width - 1 and k not in link_y[v[1]]:
            next_link.append(k)

        if v[0] == v[1] and len(diagonal_link['\\']) == board_width - 1 and k not in diagonal_link['\\']:
            next_link.append(k)
        if v[0] + v[1] == board_width + 1 and len(diagonal_link['/']) == board_width - 1 and k not in diagonal_link['/']:
            next_link.append(k)


    random.shuffle(next_link)  #if multiple choose a random one, after shuffle in place
    for move in next_link:
        if theBoard[move] == ' ':
            return move
        
    return 0


#### validate the player move only through inputCustom
def valid_move(move):
    move = int(move)

    available_moves = []
    for k in theBoard:
        if theBoard[k] == ' ':
            available_moves.append(k)
    
    if move not in range(1, (board_width * board_width) + 1) or theBoard[move] != ' ':  #is it in theboard? is it empty?
        raise Exception(f'(Invalid move!) -available moves: {available_moves}')
    
    return move


#### record moves of both players in moves_dict
def record_moves(moves_book, character, move):
    moves_book.setdefault(character, [])
    moves_book[character].append(move)


#### decide who is the 'Winner' based on game rules    
def game_logic(moves_list):
    if len(moves_list) < board_width:   
        return False

    Xcoords = {}
    Ycoords = {}

    right_diagonal = 0
    left_diagonal = 0
    for move in moves_list:
        if mapOfCoords[move][0] == mapOfCoords[move][1]:
            right_diagonal += 1
        if mapOfCoords[move][0] + mapOfCoords[move][1] == board_width + 1:
            left_diagonal += 1

        Xcoords.setdefault(mapOfCoords[move][0], 0)
        Xcoords[mapOfCoords[move][0]] += 1
        Ycoords.setdefault(mapOfCoords[move][1], 0)
        Ycoords[mapOfCoords[move][1]] += 1

    if board_width in Xcoords.values() or board_width in Ycoords.values():  #catching moves with same x or y 
        return True
    
    if right_diagonal == board_width or left_diagonal == board_width:   #catching diagonal moves
        return True
    
    return False


#### npc decision making  
def NPC_move(npc_moves = [], player_moves = []):
    #random move generator
    while True:     
        npc_move = random.randint(1, board_width * board_width)
        if theBoard[npc_move] == ' ':
            break
    
    #NPC move prioritize winning over blocking. 
    if npc_moves or player_moves: 
        win_move = link_moves(npc_moves)
        block_move = link_moves(player_moves)    
        if win_move:
            return win_move
        elif block_move:
            return block_move      
    
    center_board = ((board_width * board_width) + 1) // 2     #if board_width is odd go to center otherwise not
    if center_board % 2 == 1 and theBoard[center_board] == ' ':
        return center_board
     
    return npc_move


#### display theBoard with each update     
def print_board(board, i = 21):
    separator = '+-'
    indent = ' ' * i
    print()
    print(indent, end='')
    for k in board:
        if k % board_width != 0:   #if u reach the edge(board width) go to a newline
            print(board[k] + '|', end='')
        else:
            print(board[k])
            if k != board_width * board_width:
                print(indent + '-' + (separator * (board_width - 1))) #compatible seperator
                print(indent, end='')
    print()
            

#### clean the board for next replay
def clear_board(board):
    for k in board:
        board[k] = ' '


#### orgnize and Display function
def main():
    print('\n', '(*______Tic_Tac_Toe______*)'.center(45))    # A welcome message
    build_board()
    print_board(theBoard)   # Display the board

    while True:
        clear_board(theBoard)
        input_msg = '-> To Play Enter "X" or "O" /(to quit enter blank.): '
        player = pyip.inputChoice(choices = ['X','O'], prompt=input_msg, blank=True,  #choices are case insensitive
                                    timeout=30, default='')       #if time run out default to blank then quit
            
        if not player:
            return    #returns None but it serves as sys.exit()

        if player == 'X':
            NPC = 'O'   # Non playable character is the enemy
        else:
            NPC = 'X'

        turn = random.choice(['X', 'O'])  # Select a random turn to start (coin flip to start the game)
        moves_dict = {}      #Track the moves of both players

        # Main Game loop:
        for move in range(board_width * board_width): 
            print(f'\n=> {turn}\'s turn:') 

            if turn == player:
                try:
                    player_move = pyip.inputCustom(valid_move, prompt=f'Enter a position (1-{board_width * board_width}): ',
                                                    limit = 3) # 3 chances to get a correct move
                    theBoard[player_move] = player
                    record_moves(moves_dict, player, player_move)  
                except pyip.RetryLimitException: #instead of the exception default msg print this
                    print('Out Of Tries!')
                    break     
            else:
                #only send moves_dict when there is board_width - 1 in one of the lists     
                npcMove = NPC_move() if move < board_width else NPC_move(moves_dict[NPC], moves_dict[player])
                theBoard[npcMove] = NPC
                record_moves(moves_dict, NPC, npcMove)
                print(f'position: {npcMove}')

            print('\n| move', move + 1)
            print_board(theBoard)

            if game_logic(moves_dict[turn]):            #announcing the winner
                print(f'The winner is: {turn}\n')
                print(f'win history:{moves_dict[turn]}\n')
                break

            if move == (board_width * board_width) - 1:       #last round draw
                print('- It\'s a Tie!\n')
                print(f'moves history:\n{player}: {moves_dict[player]}, {NPC}: {moves_dict[NPC]}\n')
                break    
            
            if turn == player:              #switching turns
                turn = NPC
            else:
                turn = player

            time.sleep(0.5)  #for UX and readability

main()           

