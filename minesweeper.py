import random
import re
# Create the board.
# this is where we can just say "Create a new board" or a "dig here"
# or "render this game for this object"
class Board:

    def __init__(self, dim_size, num_bombs):
        # Let's keep track of these parameters
        # set the passed in params
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # create the board
        # helper function
        self.board = self.make_new_board() # plant the bombs
        self.assign_values_to_board()

        # init a set to keep track of where we've dug
        # save (row, col) as a tuple in this set
        self.dug = set() #if we dig at 0, 0 then self.dug = {(0,0)} 

    def make_new_board(self):   # plant the bombs
                
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        # construct new board based om dim_size and num_bombs
        # the board will be a list of lists
        # rows = self.dim_size, cols = self.dim_size makes the same number of rows and columns
        # looks something like this
        # [[None, None, ..., None],
        #  [None, None, ..., None],
        #  [...,                 ],
        #  [None, None, ..., None]]

        # Plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1) # returns a random int between 0
                                                          # and dim_size squared (-1 for 0 index)
            row = loc // self.dim_size                    # how many times does dim size into the rand int?
                                                          # this is the row (i.e 63 in a 9x9 would be row 7 of 9)
            col = loc % self.dim_size                     # which col? divide by dim_size. (i.e 63 / 9 = 7)
                                                          # for 63 this would be row 7, col 7, (i.e [7],[7])

            if board[row][col] == '*':
                # if true then there's already a bomb here so keep going without increasing bombs_planted
                continue

            board[row][col] = '*'
            bombs_planted += 1
        
        return board

    def assign_values_to_board(self):
        # bombs are now planted. Let's assign values to all indexes for how many bombs are around them

        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    # if there is already a bomb, it won't get a value
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
             # let's iterate through all neighboring squares and sum the number of bombs
             # top left = r-1, c - 1
             # top middle = r-1, c
             # top left = r-1, c + 1
             # left = r, c - 1
             # right = r, c + 1
             # bottom left = r + 1, c - 1
             # bottom middle = r + 1, c
             # bottom right = r + 1, c + 1         

             #make sure we don't go out of bounds
             num_neighboring_bombs = 0
             for r in range(max(0, row-1), min(self.dim_size-1, (row+1)+1)):
                for c in range(max(0, col-1), min(self.dim_size-1, (col+1)+1)):
                    if r == row and c == col:
                        #the starting position, don't check
                        continue
                    if self.board[r][c] =='*':
                        num_neighboring_bombs += 1

    def dig(self, row, col):
        # dig at the location
        # return True if successful dig, False if we dig a bomb

        # we hit a bomb -> Game Over
        # dig at a location with neighboring bombs -> finish dig
        # dig at a location with no neighboring bombs -> recursivly dig neighbors

        self.dug.add((row, col)) #keep track of where we've dug

        if self.board[row][col] == '*': # dug bomb
            return False
        elif self.board[row][col] != 0: 
            return True

    
        #if self.board[row][col] == 0: # dig with no neighboring bombs
            for r in range(max(0, row-1), min(self.dim_size-1, (row+1)+1)):
                    for c in range(max(0, col-1), min(self.dim_size-1, (col+1)+1)):
                        if (r, c) in self.dug: # we already dug here
                            continue
                        self.dig(r, c)  # keep digging
        return True

    def __str__(self):
        # this is a magic function
        # if you call print on this object it'll print out what it returns
        # return a string that shows the board to the player

        #first create an array with what the user should see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        # put all of this in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep


#play the game
def play(dim_size=10, num_bombs=10):
    #Step 1: Create the board and plant the bombs
    board  = Board(dim_size, num_bombs)

    #Step 2: Show the user the board and ask where they want to dig
    #Step 3a: If location is a bomb, show game over and reveal the board
    #Step 3b: If location is empty, dig recursively until each square is
    #         at least next to a bomb
    #Step 4: Repeat steps 2, 3a/b until there are no more places to dig -> Victory
    
    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row,col: "))
        row, col = int(user_input[0]), int(user_input[-1])
        #check for invalid input
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid location, try again.")
            continue
        
        #if it's valid, we dig
        safe = board.dig(row, col)
        if not safe:
            #dug a bomb
            break # game over
    if safe:
        print("Congratulations!")
    else:
        print("Sorry you lost")
        board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__ == '__main__':
    play()
    


