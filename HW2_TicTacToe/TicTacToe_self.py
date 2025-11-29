# Constants: character stands for each player
PLAYER_NAME = ['Nobody', 'X', 'O']

# return player name
def player_name(player_id):
    return PLAYER_NAME[player_id]

# display board for tic tac toe
def display_board(board):
    board_to_show = ''
    for i in range(len(board)):
        if board[i] == 0:                           # base case
            board_to_show += str(i + 1)
        else:
            board_to_show += player_name(board[i])
        if (i + 1) % 3 == 0:
            board_to_show += '\n'
        else:
            board_to_show += ' | '
    print()
    print(board_to_show)

# function for moving from the dice number to the O or X in tic tac toe
def make_move(player, board):
    while True:
        try:
            move = int(input(player_name(player) + "'s" + 'move: '))
            if 1 <= move <= 9 and player == 1 and board[move-1] == 0:
                board[move-1] = 1
                display_board(board)
                break
            elif 1 <= move <= 9 and player == 2 and board[move-1] == 0:
                board[move-1] = 2
                display_board(board)
                break
            else:
                if (board[move-1] == 1 and player == 2) or (board[move-1] == 2 and player == 1):
                    print('Your opponent already chose that position!')
                if (board[move-1] == 1 and player == 1) or (board[move-1] == 2 and player == 2):
                    print('You already chose that position!')
                print(f'Enter number other than {move}')
        except ValueError:
            print('Enter a number between 1 and 9')
# function to check who wins the game
def check_win(board):
    # check horizontally first
    if board[0] == board[1] == board[2] == 1:
        return 1
    if board[0] == board[1] == board[2] == 2:
        return 2
    if board[3] == board[4] == board[5] == 1:
        return 1
    if board[3] == board[4] == board[5] == 2:
        return 2
    if board[6] == board[7] == board[8] == 1:
        return 1
    if board[6] == board[7] == board[8] == 2:
        return 2
    # check vertically
    if board[0] == board[3] == board[6] == 1:
        return 1
    if board[0] == board[3] == board[6] == 2:
        return 2
    if board[1] == board[4] == board[7] == 1:
        return 1
    if board[1] == board[4] == board[7] == 2:
        return 2
    if board[2] == board[5] == board[8] == 1:
        return 1
    if board[2] == board[5] == board[8] == 2:
        return 2
    # check diagonally
    if board[0] == board[4] == board[8] == 1:
        return 1
    if board[0] == board[4] == board[8] == 2:
        return 2
    if board[2] == board[4] == board[6] == 1:
        return 1
    if board[2] == board[4] == board[6] == 2:
        return 2
    return 0

def next_player(current_player):
    if current_player == 1:
        return 2
    else:
        return 1

# main function
def main():
    board = [0, 0, 0,               # top row
             0, 0, 0,               # middle row
             0, 0, 0]               # bottom row
    player = 1                      # 'X' goes first
    moves_left = 9                  # maximum moves are 9 moves
    winner = 0                      # default is nobody wins
    while(moves_left > 0 and winner == 0):
        display_board(board)        # takes the blank board as argument
        make_move(player, board)    # X moves first. Input the value
        winner = check_win(board)   # check whos winner
        player = next_player(player)
        moves_left -= 1
    if winner == 0:
        print('Game over! Nobody wins!')
    else:
        print(f'Game over! {player_name(winner)} wins!')

# if the py file is executed directly, call main function
if __name__ == '__main__':
    main()