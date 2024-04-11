from flask import Flask, request, jsonify
import random
import copy
import math

app = Flask(__name__)

@app.route('/process_data', methods=['POST'])

def process_data():
    data = request.json
    return jsonify(data)
# assigning board
board = [["-","-","-"],["-","-","-"],["-","-","-"]]

def reset_board(): # reset board after a game is played
    global board # global variable so can be used globally
    board = [["-","-","-"],["-","-","-"],["-","-","-"]]

def test_win_move(board_copy, any_tag, row, col):    
    boardCopy = copy.deepcopy(board)
    boardCopy[row][col] = any_tag
    return isWin(boardCopy)
    
def valid(user_input):
    # validating user input
    if user_input.isnumeric():
        user_input = int(user_input)
        if user_input < 3 and user_input >=0:
            return True
    else:
        return False


def each_turn(tag): # for logic of making a move
    print("Type your coordinates for your move.")
    while True:
        user_row = input("Input your row")
        user_col = input("Input your col")

        if valid(user_row) and valid(user_col):
            user_row = int(user_row)
            user_col = int(user_col)
            if board[user_row][user_col] != "-": # checks if there is not a empty node instead of checking if there is an occupied one so it handles both X and O
                print("Occupied")
            else:
                board[user_row][user_col] = tag # place nought / cross
                break
        else:
            print("illegal move")

def ai_player_easy(op_tag): # gets a random empty square and places tag
    possible_moves = []
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == "-":
                this_move = [row,col]
                possible_moves.append(this_move)
    random_choice = random.choice(possible_moves)
    board[random_choice[0]][random_choice[1]] = op_tag
    return random_choice

def ai_player_hard(board, op_tag, tag): # blocks wins and finds wins
    if not isWin(board):
        good_moves = []
        best_moves = []
        # check computer win moves   
        for row in range(len(board)):
            for col in range(len(board)):
                if board[row][col] == "-" and test_win_move(board, op_tag, row, col):
                    best_moves.append((row,col))
                    
                     
        # check player win moves
        for row in range(len(board)):
            for col in range(len(board)):
                if board[row][col] == "-" and test_win_move(board, tag, row, col):
                    good_moves.append((row,col))                

    possible_moves = []

    # choose a move to play

    if not isWin(board) and not isDraw(board):
        if best_moves:
            for x in best_moves:
                possible_moves.append(x)
        if good_moves and not best_moves:
            for x in good_moves:
                possible_moves.append(x)
        if good_moves and best_moves:
            for x in best_moves:
                possible_moves.append(x)
        # play a random move if no good or best moves
        if not good_moves or best_moves:
            ai_player_easy(op_tag)

        # choose a random move out of possible move lists if multiple choices are present
        if possible_moves:
            random_move = random.choice(possible_moves)
            board[random_move[0]][random_move[1]] = op_tag
    

def utility(board, max_player, min_player): # uses heura thingy to return a score
    huristic = 0
    if isWin(board) == max_player:
        if min_player == max_player:
            huristic = 1
        else:
            hursitic = -1
            
        return {'move': None, 'score': huristic}
    if isDraw(board):
        return {'move': None, 'score': 0}

def terminal(board): # returns either true or false if game is in win or draw state
    
    if isWin(board) == "X" or isWin(board) == "O":
        return True
    elif isDraw(board):
        return True
    else:
        return False
    
    
                        
    
def game():
    # title
    print("NOUGHTS AND CROSSES")
    print("-------------------")
    main() # for initial start
    running = True
    # while loop to ask user if they want to exit the game
    while running: 
        keep_playing = input("Would you like to keep playing? (YES)(NO)")
        keep_playing = keep_playing.upper()
        if keep_playing == "YES":
            reset_board() # resets board
            main() # calls main to run game
        elif keep_playing == "NO":
            running = False
        else:
            print("invalid input")
            
        
    
def main():
    # asks which tag they would like to use and assigns them the tag
    if choice():
        tag = "O"
        op_tag = "X" # opponent tag / player 2 tag
    else:
        tag = "X"
        op_tag = "O"

    if tag == "X": # determines whos first turn it is
        playerOne = True
    else:
        playerOne = False

    if ai_or_player(): # asks which opponent they would like to face.
        ai = False
    else:
        ai = True
        difficulty_mode = difficulty()
    while isWin(board) == False and isDraw(board) == False:
        if playerOne: # determines whos turn it is
            DisplayBoard()
            each_turn(tag)
            playerOne=False
            print("")     
        if not playerOne and not isWin(board) and not isDraw(board): # checks every turn whether the game is in a win state so there isn't an extra turn
            if ai:
                if difficulty_mode == "EASY":
                    ai_player_easy(op_tag)
                if difficulty_mode == "HARD":
                    ai_player_hard(board,op_tag, tag)
                if difficulty_mode == "IMPOSSIBLE":
                    row,col = get_best_move(board,op_tag)
                    board[row][col] = op_tag
                    
            if not ai:
                DisplayBoard()
                each_turn(op_tag)
                
                
            playerOne=True

            
    result = isWin(board)
    # checks winning player
    if result:
        if result == tag:
            print("Player One Wins!")
        elif result == op_tag:
            print("Player Two Wins!")
        DisplayBoard()

    if isDraw(board) and not result:
        DisplayBoard()
        print("Draw")
        print("")
        

              
        
def isWin(board):
    if board[0][0] != "-" and board[0][0] == board[1][1] == board[2][2]: # diagonal check
        return board[0][0]
    if board[2][0] != "-" and board[2][0] == board[1][1] == board[0][2]: # diagonal check
        return board[2][0]
    for x in range(3):
        if board[x][0] != "-" and board[x][0] == board[x][1] ==board[x][2]: # row checks
            return board[x][0]
        if board[0][x] != "-" and board[0][x] == board[1][x] ==board[2][x]:
            return board[0][x]
    else:
        return False
    

def isDraw(board):
    if not any("-" in x for x in board):
        return True
    else:
        return False
##game()
    
if __name__ == 'main':
    app.run(debug=True)