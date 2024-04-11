from flask import  Flask, current_app, flash, jsonify, make_response, redirect, request, url_for, render_template
import random, copy
app = Flask(__name__)
return_data = {}
@app.route("/")
def home():
    return render_template("index.html", static_url_path='/static')

@app.route('/process_data', methods=['POST', 'GET'])
def process_data():
    if request.method == "POST":
        print("POST")
        data = request.json
        terminal(data)
        return data
    else:
        print("GET!")
        print(return_data)
        return jsonify(return_data)

def terminal(data):
    global return_data
    converted_data = convert_data(data)
    print(converted_data)
    return_move = main(converted_data)
    print(return_move)
    return_data = convert_data_back(return_move)
    print(board)
    return converted_data
def convert_data(data):
    print(data)
    # convert string to a usable data type for python script to handle
    row_col = data.get("data")
    row_col = row_col.replace("cell", "")
    row = str(row_col[0])
    col = str(row_col[1])
    symbol = data.get("symbol")
    aiEnabled = data.get("ai")
    return aiEnabled, symbol, (row,col)

def convert_data_back(data):
    # convert data back so that it can be sent through json
    send_back = {'symbol':'','data':''}
    symbol = data[0]
    print(symbol)
    first_num = data[1][0]
    second_num = data[1][1]
    origin_data = 'cell' + str(first_num) + str(second_num)

    # insert values into dict format
    send_back['symbol'] = symbol
    send_back['data'] = origin_data
    print(send_back)
    return send_back

#----------BACKEND TIC TAC TOE LOGIC-----------#
board = [["-","-","-"],["-","-","-"],["-","-","-"]]
def main(data):
    ai = data[0]
    symbol = data[1]
    move = data[2]
    #--game cycle--#
    return_move = turn(ai, symbol, move)
    print("main")
    return return_move

    

def turn(ai, symbol, move):
    #-- inputs player's move --#
    if board[int(move[0])][int(move[1])] == "-":
        board[int(move[0])][int(move[1])] = symbol
    #-- ai / player 2 move --#
    if ai:
        cpu_symbol = ""
        print("Symbol: ",symbol)
        if symbol == "O":
            cpu_symbol = "X"
        else:
            cpu_symbol = "O"
        print("CPU Symbol: ",cpu_symbol)
        ai_turn = cpu_move(symbol,cpu_symbol)
        print("Move to make: ",ai_turn[0], ai_turn[1])
        board[int(ai_turn[0])][int(ai_turn[1])] = cpu_symbol
        return cpu_symbol, ai_turn
 
def cpu_move(symbol, cpu_symbol): # blocks wins and finds wins
    good_moves = []
    best_moves = []
    # check computer win moves   
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == "-" and test_win_move(board, cpu_symbol, row, col):
                best_moves.append((row,col))
                
                    
    # check player win moves
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == "-" and test_win_move(board, symbol, row, col):
                good_moves.append((row,col))  

    possible_moves = []
    # choose a move to play
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
        move = random_move()
        return move
    print("Moves", good_moves,best_moves)
    if possible_moves:
        move = random.choice(possible_moves)
        return move
           
def random_move(): # gets a random empty square and places tag
    global board
    possible_moves = []
    print(board)
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == "-":
                this_move = [row,col]
                possible_moves.append(this_move)
    print("possible: ",possible_moves)
    random_choice = random.choice(possible_moves)
    return random_choice

def test_win_move(board_copy, symbol, row, col):    
    boardCopy = copy.deepcopy(board)
    boardCopy[row][col] = symbol
    return isWin(boardCopy)
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
if __name__ == '__main__':
    app.run(debug=True)