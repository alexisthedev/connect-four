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

n = give_dimensions()
positions = [[' ']*n]*n # nXn list for player moves
board = make_board()
print_board()