def make_board(): # Creates an empty nXn game board
    board = [[] for x in range(n)]

    for i in range(n):
        letter = chr(65+i) # Letter at the start of the row (chr(65) is A, chr(66) is B, ..)
        board[i].append(f'{letter}|')
        for j in range(n): # Adds the cells to each row
            board[i].append(f'   {positions[i][j]}|')

    board.insert(0, '-'*n*5) # First row of ---
    board.append('-'*n*5) # Last row of ---
    board.insert(0, [f'    {x}' for x in range(1, n+1)]) # Row of column numbers

    return board

def print_board():
    print(''.join(board[0])) # Column numbers as joined string
    print(board[1]) # --- line
    for i in range(2, n+2):
        print(''.join(board[i])) # Game board rows as joined strings
    print(board[-1] + '\n') # --- line

def give_dimensions():
    n = input("Give the game board dimensions (5-10): ").strip()

    while not n.isdigit() or int(n)<5 or int(n)>10: # Checks if input is a 5-10 integer
        n = input("Please give a valid input (5-10): ").strip()
    
    return int(n)

def player_move():
    def place_in_col(col): # Drops disk in column
        row = n-1
        while positions[row][col-1] != ' ': # Starts checking if column cell is empty from bottom to top
            row -= 1 # Goes on cell up until the first empty cell is found
        positions[row][col-1] = 'O' # Drops disk in the empty cell
        change_board(row, col-1)

    def change_board(i, j): # Updates the state of the game board
        board[i+2][j+1] = f'   {positions[i][j]}|'


    col = input("Player 1: Choose a column for your disk: ").strip()

    while not col.isdigit() or int(col)<1 or int(col)>n or positions[0][int(col)-1]!=' ': # Checks that input is 1-N integer and column is empty
        col = input("Player 1: Choose a valid column for your disk: ").strip()
    
    place_in_col(int(col))

n = give_dimensions()
positions = [] # nXn list for player moves
for i in range(n): # initialized as empty
    positions.append([' ']*n)

board = make_board()
print_board()
player_move()
print_board()
player_move()
print_board()