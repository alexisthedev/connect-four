from typing import Counter


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

def player_move(player):
    def place_in_col(col): # Drops disk in column
        row = n-1
        while positions[row][col-1] != ' ': # Starts checking if column cell is empty from bottom to top
            row -= 1 # Goes on cell up until the first empty cell is found
        positions[row][col-1] = disk # Drops disk in the empty cell

        change_board(row, col-1)

        return (row, col-1) # col-1 because in the visualization the letter cell A| is at index 0

    def change_board(i, j): # Updates the state of the game board
        board[i+2][j+1] = f'   {positions[i][j]}|'
    
    def wincond(p): # Checks if player wins after latest move (p is tuple of (i, j))
        def horizontal(score): # Checks for 4 disks in row
            count = 0
            win = False
            index = -1
            row = p[0] # Only checks the row where latest disk was placed

            for j in range(n):
                if count == 0 and positions[row][j]==disk: # Disk is first in sequence
                    index = j # Position of first disk
                    count += 1
                elif count > 0 and count < 3 and positions[row][j] == disk: # Disk is in sequence
                    count += 1
                elif count < 4 and positions[row][j] != disk: # Disk breaks previous sequence
                    count = 0
                elif count == 3 and positions[row][j] == disk: # Disk creates winning sequence
                    win = True
                    count += 1
                elif count >= 4 and positions[row][j] == disk: # Disk increases score of winning sequence
                    count += 1
                else: # Disk breaks the winning sequence
                    break

            if win:
                score += count # Increases the score of the player if they won
                for i in range(index, index+count): # Makes the winning disks stars(*)
                    positions[row][i] = '*'
                    change_board(row, i)
            return win
        
        def vertical(score): # Checks for 4 disks in column
            count = 0
            win = False
            col = p[1]

            for i in range(n-1, -1, -1): # Searches column bottom-up for winning sequence
                if positions[i][col] == ' ':
                    break
                elif count == 0 and positions[i][col]==disk: # Disk is first in sequence
                    count += 1
                elif count > 0 and count < 3 and positions[i][col] == disk: # Disk is in sequence
                    count += 1
                elif count < 4 and positions[i][col] != disk: # Disk breaks previous sequence
                    count = 0
                elif count == 3 and positions[i][col] == disk: # Disk creates winning sequence
                    win = True
                    break

            if win:
                score += 4 # Maximum 4 consecutive disks in a column

                for i in range(p[0], p[0]+4): # Turns vertical sequence to stars (*)
                    positions[i][col] = '*'
                    change_board(i, col)
            return win
        
        def diagonal1(score): # Checks for 4 disks in y=x diagonal
            count = 0
            win = False
            i, j = p[0], p[1]
            while i != n-1 and j != 0: # Finds leftmost cell of y=x diagonal
                i += 1
                j -= 1

            if j==0: # Calculates length of y=x diagonal
                dlength = i+1
            else:
                dlength = i+1-j

            for k in range(dlength):
                if count == 0 and positions[i-k][j+k]==disk: # Disk is first in sequence
                    pos = (i-k, j+k) # Coordinates of first disk
                    count += 1
                elif count > 0 and count < 3 and positions[i-k][j+k] == disk: # Disk is in sequence
                    count += 1
                elif count < 4 and positions[i-k][j+k] != disk: # Disk breaks previous sequence
                    count = 0
                elif count == 3 and positions[i-k][j+k] == disk: # Disk creates winning sequence
                    win = True
                    count += 1
                elif count >= 4 and positions[i-k][j+k] == disk: # Disk increases score of winning sequence
                    count += 1
                else: # Disk breaks the winning sequence
                    break


            if win:
                score += count

                i = pos[0]
                j = pos[1]
                for k in range(count):
                    positions[i-k][j+k] = '*'
                    change_board(i-k, j+k)
            return win
        
        def diagonal2(score): # Checks for 4 disks in y=-x diagonal
            count = 0
            win = False
            i, j = p[0], p[1]
            while i != n-1 and j != n-1: # Finds rightmost cell of y=-x diagonal
                i += 1
                j += 1

            if j==n-1: # Calculates length of y=-x diagonal
                dlength = i+1
            else:
                dlength = j+1

            for k in range(dlength):
                if count == 0 and positions[i-k][j-k]==disk: # Disk is first in sequence
                    pos = (i-k, j-k) # Coordinates of first disk
                    count += 1
                elif count > 0 and count < 3 and positions[i-k][j-k] == disk: # Disk is in sequence
                    count += 1
                elif count < 4 and positions[i-k][j-k] != disk: # Disk breaks previous sequence
                    count = 0
                elif count == 3 and positions[i-k][j-k] == disk: # Disk creates winning sequence
                    win = True
                    count += 1
                elif count >= 4 and positions[i-k][j-k] == disk: # Disk increases score of winning sequence
                    count += 1
                else: # Disk breaks the winning sequence
                    break


            if win:
                score += count

                i = pos[0]
                j = pos[1]
                for k in range(count):
                    positions[i-k][j-k] = '*'
                    change_board(i-k, j-k)
            return win

        score = 0
        h = horizontal(score)
        v = vertical(score)
        d1 = diagonal1(score)
        d2 = diagonal2(score)

        if h or v or d1 or d2:
            return True

    if player == 1:
        disk = 'O'
    else:
        disk = 'X'
    
    col = input(f'Player {player}: Choose a column for your disk: ').strip()

    while not col.isdigit() or int(col)<1 or int(col)>n or positions[0][int(col)-1]!=' ': # Checks that input is 1-N integer and column is empty
        col = input(f'Player {player}: Choose a valid column for your disk: ').strip()
    
    cords = place_in_col(int(col))

    print_board()

    if wincond(cords):
        print(f'Player {player} won!')
        print_board()
        return True
    return False


print('Welcome to Connect-4!')
n = give_dimensions()
positions = [] # nXn list for player moves
for i in range(n): # initialized as empty
    positions.append([' ']*n)

board = make_board()
player = 1
print_board()
while not player_move(player): # Game runs until someone wins
    if player == 1:
        player = 2
    else:
        player = 1