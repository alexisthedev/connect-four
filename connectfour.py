"""
Connect-4: A Game in Python

Alex Papadopoulos [github.com/alexisthedev]

Dimitris Fotogiannopoulos [github.com/dfotogiannopoulos]

Dimitris Toumazatos [github.com/dimitristoumazatos]

"""

import csv
from time import sleep

def start():
    """
    Initializes new game objects if the users
    choose to start a new game

    """


    global positions
    global player1
    global player2
    global n

    n = give_dimensions()
    positions = [] # nXn list for player moves
    for i in range(n): # initialized as empty
        positions.append([' ']*n)

    player1 = make_player(input('Player 1, what\'s your name?\n'), 1)
    player2 = make_player(input('Player 2, what\'s your name?\n'), 2)

def make_board():
    """
    Creates an empty nXn game board (visualization)
    """

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
    """
    Prints the game board (visualzied) at the state of the game
    depending on the values of the positions two-dimensional array ('O', 'X', ' ')
    """

    print(''.join(board[0])) # Column numbers as joined string
    print(board[1]) # --- line
    for i in range(2, n+2):
        print(''.join(board[i])) # Game board rows as joined strings
    print(board[-1] + '\n') # --- line

def copy_board():
    """
    Creates a copy of the positions array (non-visualized board)

    """

    temp = []
    for i in range(n):
        temp.append([])
        for j in range(n):
            temp[i].append(positions[i][j])
    return temp

def give_dimensions():
    """
    Gets the board dimensions from the players

    """

    n = input("Give the game board dimensions (5-10): ").strip()

    while not n.isdigit() or int(n)<5 or int(n)>10: # Checks if input is a 5-10 integer
        n = input("Please give a valid input (5-10): ").strip()
    
    return int(n)

def make_player(name, player, score=0):
    """
    Creates player dictionary that holds values of player name, 
    whether the player is player 1 or 2, and individual score

    >>> make_player('alex', 1)
    {'name': 'alex', 'number': 1, 'score': 0}
    
    >>> make_player('dimitris', 2, 50)
    {'name': 'dimitris', 'number': 2, 'score': 50}

    """

    return {'name': name, 'number': player, 'score': score}

def save_game(board, pone, ptwo):
    """
    Saves current game state (boar, scores, player names)
    in a file named by the players
    """

    for i in range(n):
        for j in range(n):
            cell = board[i][j]
            if cell == ' ':
                board[i][j] = 0
            elif cell == 'O':
                board[i][j] = 1
            else:
                board[i][j] = 2
    
    board.append([pone['score'], ptwo['score']])
    board.append([pone['name'],ptwo['name']])

    filename = input('Give file name: ').strip()

    with open(f'{filename}', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(board)

def load_game():
    """
    Loads previously saved game from a file
    
    """

    global positions
    global player1
    global player2
    global n

    positions = []
    filename = input('Give file name: ').strip()
    with open(f'{filename}', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            positions.append(row)
    
    names = positions.pop(-1)
    scores = positions.pop(-1)

    player1 = make_player(names[0], 1, int(scores[0]))
    player2 = make_player(names[1], 2, int(scores[1]))

    n = len(positions)
    for i in range(n):
        for j in range(n):
            cell = int(positions[i][j])
            if cell == 0:
                positions[i][j] = ' '
            elif cell == 1:
                positions[i][j] = 'O'
            else:
                positions[i][j] = 'X'
    

def player_move(player):
    """
    General function that orchestrates each player move
    (disk placement, win check, board visualization update, asterisks, etc)

    """

    def place_in_col(col):
        """
        Drops player's disk (O or X) in chosen column (if not full)

        >>> n = 5
        >>> disk = 'O'
        >>> positions = [[' '*n], [' '*n], [' '*n], [' '*n], [' '*n]]
        >>> place_in_col(3)
        >>> positions[4][2] == 'O'
        True
        """

        row = n-1
        while positions[row][col-1] != ' ': # Starts checking if column cell is empty from bottom to top
            row -= 1 # Goes on cell up until the first empty cell is found
        positions[row][col-1] = disk # Drops disk in the empty cell

        change_board(row, col-1)

        return (row, col-1) # col-1 because in the visualization the letter cell A| is at index 0

    def change_board(i, j):
        """
        Updates the state of the visualized game board
        (called when changes are made to the positions array)

        """

        board[i+2][j+1] = f'   {positions[i][j]}|'

    def asterisks(hor, ver, diag1, diag2):
        """
        Replaces winning disk sequences  with asterisks (*)
        
        """

        for i in range(n):
            for j in range(n):
                if hor[i][j] == '*':
                    positions[i][j] = '*'
                    change_board(i, j)
                elif ver[i][j] == '*':
                    positions[i][j] = '*'
                    change_board(i, j)
                elif diag1[i][j] == '*':
                    positions[i][j] = '*'
                    change_board(i, j)
                elif diag2[i][j] == '*':
                    positions[i][j] = '*'
                    change_board(i, j)
    
    def remove_asterisks():
        """
        Removes asterisks and slides floating disks down
        
        """

        for j in range(n):
            col = []
            for i in range(n-1,-1,-1):
                col.append(positions[i][j])
            
            for i in range(n):
                while col[i] == '*':
                    col.pop(i)
                    col.append(' ')
            
            for i in range(n-1,-1,-1):
                positions[i][j] = col[n-i-1]
                change_board(i,j)
    
    def wincond(p):
        """
        Checks if player wins after latest move
        (p is tutple of (i,j) indexes/coordinates)

        """

        def horizontal(player):
            """
            Checks for 4 disks in horizontal row

            """

            count = 0
            win = False
            index = -1
            row = p[0] # Only checks the row where latest disk was placed
            temp = copy_board()

            for j in range(n):
                if count == 0 and temp[row][j]==disk: # Disk is first in sequence
                    index = j # Position of first disk
                    count += 1
                elif count > 0 and count < 3 and temp[row][j] == disk: # Disk is in sequence
                    count += 1
                elif count < 4 and temp[row][j] != disk: # Disk breaks previous sequence
                    count = 0
                elif count == 3 and temp[row][j] == disk: # Disk creates winning sequence
                    win = True
                    count += 1
                elif count >= 4 and temp[row][j] == disk: # Disk increases score of winning sequence
                    count += 1
                else: # Disk breaks the winning sequence
                    break

            if win:
                player['score'] += count # Increases the score of the player if they won
                for i in range(index, index+count): # Makes the winning disks stars(*)
                    temp[row][i] = '*'
            
            
            return (win, temp)
        
        def vertical(player):
            """
            Checks for 4 disks in vertical column
            
            """

            count = 0
            win = False
            col = p[1]
            temp = copy_board()

            for i in range(n-1, -1, -1): # Searches column bottom-up for winning sequence
                if temp[i][col] == ' ':
                    break
                elif count == 0 and temp[i][col]==disk: # Disk is first in sequence
                    count += 1
                elif count > 0 and count < 3 and temp[i][col] == disk: # Disk is in sequence
                    count += 1
                elif count < 4 and temp[i][col] != disk: # Disk breaks previous sequence
                    count = 0
                elif count == 3 and temp[i][col] == disk: # Disk creates winning sequence
                    win = True
                    break

            if win:
                player['score'] += 4 # Maximum 4 consecutive disks in a column

                for i in range(p[0], p[0]+4): # Turns vertical sequence to stars (*)
                    temp[i][col] = '*'
                
            return (win, temp)
        
        def diagonal1(player):
            """
            Checks for 4 disks in y=x diagonal
            
            """
            count = 0
            win = False
            i, j = p[0], p[1]
            temp = copy_board()

            while i != n-1 and j != 0: # Finds leftmost cell of y=x diagonal
                i += 1
                j -= 1

            if j==0: # Calculates length of y=x diagonal
                dlength = i+1
            else:
                dlength = i+1-j

            for k in range(dlength):
                if count == 0 and temp[i-k][j+k]==disk: # Disk is first in sequence
                    pos = (i-k, j+k) # Coordinates of first disk
                    count += 1
                elif count > 0 and count < 3 and temp[i-k][j+k] == disk: # Disk is in sequence
                    count += 1
                elif count < 4 and temp[i-k][j+k] != disk: # Disk breaks previous sequence
                    count = 0
                elif count == 3 and temp[i-k][j+k] == disk: # Disk creates winning sequence
                    win = True
                    count += 1
                elif count >= 4 and temp[i-k][j+k] == disk: # Disk increases score of winning sequence
                    count += 1
                else: # Disk breaks the winning sequence
                    break


            if win:
                player['score'] += count

                i = pos[0]
                j = pos[1]
                for k in range(count):
                    temp[i-k][j+k] = '*'
            return (win, temp)
        
        def diagonal2(player):
            """
            Checks for 4 disks in y=-x diagonal

            """

            count = 0
            win = False
            i, j = p[0], p[1]
            temp = copy_board()

            while i != n-1 and j != n-1: # Finds rightmost cell of y=-x diagonal
                i += 1
                j += 1

            if j==n-1: # Calculates length of y=-x diagonal
                dlength = i+1
            else:
                dlength = j+1

            for k in range(dlength):
                if count == 0 and temp[i-k][j-k]==disk: # Disk is first in sequence
                    pos = (i-k, j-k) # Coordinates of first disk
                    count += 1
                elif count > 0 and count < 3 and temp[i-k][j-k] == disk: # Disk is in sequence
                    count += 1
                elif count < 4 and temp[i-k][j-k] != disk: # Disk breaks previous sequence
                    count = 0
                elif count == 3 and temp[i-k][j-k] == disk: # Disk creates winning sequence
                    win = True
                    count += 1
                elif count >= 4 and temp[i-k][j-k] == disk: # Disk increases score of winning sequence
                    count += 1
                else: # Disk breaks the winning sequence
                    break


            if win:
                player['score'] += count

                i = pos[0]
                j = pos[1]
                for k in range(count):
                    temp[i-k][j-k] = '*'
            return (win, temp)
            
        h = horizontal(player) # Returns tuple, first element Boolean, second element the board with *
        v = vertical(player) # For columns
        d1 = diagonal1(player) # For diagonal y=x
        d2 = diagonal2(player) # For diagonal y=-x

        if h[0] or v[0] or d1[0] or d2[0]: # If at least one win in any direction returns tuple (Boolean, list of boards with *)
            return (True, [h[1], v[1], d1[1], d2[1]]) # Temporal boards are used to support multi-directional wins
        return (False, None)

    if player['number'] == 1:
        disk = 'O'
    else:
        disk = 'X'

    playername = player['name']
    
    col = input(f'{playername}: Choose a column for your disk: ').strip()

    while not col.isdigit() or int(col)<1 or int(col)>n or positions[0][int(col)-1]!=' ': # Checks that input is 1-N integer and column is empty
        col = input(f'{playername}: Choose a valid column for your disk: ').strip()
    
    cords = place_in_col(int(col))

    print('\n')
    print_board()
    print('\n\n')

    doeswin = wincond(cords) # Tuple of Boolean and a list of temporal boards that replaced winning disks with *
    if doeswin[0]:
        asterisks(doeswin[1][0], doeswin[1][1], doeswin[1][2], doeswin[1][3])
        print_board()
        print(f'{playername} connected 4!')
        sleep(1)
        remove_asterisks()
        print_board()

if __name__ == '__main__':
    print('Welcome to Connect-4!')

    gamestate = input('Would you like to start a new game (N) or load one from a file (S)? ').strip() # Checks for valid input on New or Load game
    while gamestate != 'S' and gamestate != 'N':
        gamestate = input('Please enter a valid input (N for new game, S to load game): ').strip()


    if gamestate == 'N':
        start()
    else:
        load_game()

    board = make_board()
    print_board()

    while True: # Game runs until board fills up or game state is saved
        player_move(player1)
        if not any(' ' in ls for ls in positions): # Stops if board filled up after player 1 moved
            break
        
        player_move(player2)
        if not any(' ' in ls for ls in positions): # Stops if board filled up after player 2 move
            break

        ans = input("\n\nChoose any key to continue playing.\nTo pause and save the game choose 's': ")
        if ans == 's':
            save_game(positions, player1, player2)
            break

    if any(' ' in ls for ls in positions): # Prints out score when game is finished (full board)
        if player1['score'] > player2['score']:
            print(f"Player 1 {player1['name']} won the game with a score of {player1['score']} against {player2['name']}'\s {player2['score']}")
        elif player1['score']==player2['score']:
            print('How did you guys manage to tie in a game of connect-4?')
        else:
            print(f"Player 2 {player2['name']} won the game with a score of {player2['score']} against {player1['name']}'\s {player1['score']}")