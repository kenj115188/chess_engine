# Purposes of the programme:
    # Takes a move in chees notation and outputs an appropriate and legal
    # countermove
    # Represents the current board status when asked
    # It is OO for didactic purposes

# Notes:
    # Maybe could add an option for specifying a particular pieces arrangement
    # Maybe could add an option for playing human-human, human-AI or AI-AI,
    # current only human-AI
    # Will add Random, MinMax and alfa/beta pruning AI algorthms
    # add evaluate_board function
    # add special moves

###############################################################################

# Pseudocode for the general structure of the programme

# Print splash screen
# Main loop:
    # Ask for user input
    # Process the input and do one of the following:
        # Select AI alogrithm
            # Algorithm selection loop
        # Start a new game:
            # Control loop
        # List saved games and allows user to resume one:
            # Control loop
        # Quit
        # Print an error and restarts the main loop

# Control loop:
    # Has AI algorithm been selected?
        # YES:
            # Continue the control loop
        # NO:
            # Print an error
            # Enter algorithm selection loop
    # Ask for user input
    # Process the input and do one of the following:
        # Print current checkboard status
        # Operate a move on the board:
            # Game loop
        # Return to main loop
        # Print an error and restart the control loop

# Algorithm selection loop:
    # Ask for user input
    # Process the input and do one of the following:
        # Select the choosen algorthm
        # Print an error and restart the algorthm selection loop
        # Return to main menu

# Game loop:
    # Check if the game has ended:
        # Print result
        # return to control loop
    # Check who can move and enter the appropriate loop
        # User move loop
        # AI move loop

# User moves loop:
    # Ask the user to insert a move or quit to control loop
    # Input is converted in the internal representation
    # Assert move validity
    # Operate the move on the board
    # Return to game loop

# AI moves loop:
    # AI loop produces an internal move representation
    # Assert move validity
    # Operate the move on the board
    # Convert AI move in chess representation
    # Print move in chees representation
    # Return to game loop

# AI loop:
    # Ask for piece possible moves
    # Prune the possible moves against the board
    # Choose a move using the selected algorithm
    # Return choosen move

###############################################################################
# General outline of the game representation:
    # The board is represented as a 8*8 matrix (list of lists) of game class
        # The first coordinate is the row, the second the column
    # An empty cell has value 0
    # A cell with a piece contains an object of the appropriate class
    # Maybe in future a way for creating a particular pieces arrangement could
    # be implemented

###############################################################################

letter_xy_table = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7}
xy_letter_table = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H"}
#set a corrispondece x_value:row_name
w,b = "white","black"
out_of_range = "This value is out of the specified range"
p,r,c,b,q,k = "pawn","rook","knight","bishop","queen","king"
#codifies an uniform way for representing an out of range value
automated = False
showing_possibles = False
showing_moves = []
#set the defaults for globals

#convert xy coordinate to conventional notation
def xy_to_letter(coordinate_list):
    x,y = coordinate_list[0],coordinate_list[1]
    try:
        assert ((0<=x<=7) and (0<=y<=7))
        x_letter = xy_letter_table[x]
#add 1 because cells go from 1-8, not 0-7
        letteral_coordinate = str(x_letter)+str(y+1)
        return letteral_coordinate
    except:
        return out_of_range


#extract x from conventional notation
def letter_to_x(letter_coordinate):
    x_letteral = letter_coordinate[1]
    x_value_string = letter_xy_table[x_letteral]
    x = int(x_value_string)
    assert (0<=x<=7)
    return x


#extract y from conventional notation
def letter_to_y(letter_coordinate):
    y_string = letter_coordinate[1]
    y = int(y_string)-1
    assert (0<=y<=7)
    return y


#combines the to previos functions and return a list
def letter_to_xy(letter_coordinate):
    x = letter_to_x(letter_coordinate)
    y = letter_to_y(letter_coordinate)
    coordinate_list = [x,y]

#returns the opposite color of the one given
def opposite_color(color):
    assert color == w or color == b
    if color == w: return b
    elif color == b: return w


#set the global variable current game to point to the game in play
def set_current_game(game):
    global current_game
    current_game = game

#the complicated game class, which builts the checkboard
class game:
    def __init__(self):
#create an 8*8 empty list of lists
        self.board = []
        for y in range (0,8):
            self.row = []
            for x in range (0,8):
                self.row.append(0)
            self.board.append(self.row)
#create a counter variable with value 0
        self.counter = 0
#at creation, the board is assumed to be the current game
        set_current_game(self)

#add pieces in specified positions and gives them properties
    def add_piece(self,piece_name,color,coordinate_list):
        x,y = coordinate_list[0],coordinate_list[1]
        if automated == False:
            assert (piece_name == p or r or c or b or q or k)
            assert color == w or b
            assert 0<=x,y<=7
#assert input validity if the human is playing
        if piece_name == p: self.board[x][y] = pawn()
        elif piece_name == r: self.board[x][y] = rook()
        elif piece_name == c: self.board[x][y] = knight()
        elif piece_name == b: self.board[x][y] = bishop()
        elif piece_name == q: self.board[x][y] = queen()
        elif piece_name == k: self.board[x][y] = king()
#add the right object depending on input
        self.board[x][y].update_position(coordinate_list)
        self.board[x][y].give_color(color)

#place all pieces in the starting position on the board, creating piece objects
    def initialise(self):
        self.add_piece(r,w,[0,0])
        self.add_piece(c,w,[1,0])
        self.add_piece(b,w,[2,0])
        self.add_piece(q,w,[3,0])
        self.add_piece(k,w,[4,0])
        self.add_piece(b,w,[5,0])
        self.add_piece(c,w,[6,0])
        self.add_piece(r,w,[7,0])
        for x in range(0,8):
            self.add_piece(p,w,[x,1])
        self.add_piece(r,b,[0,7])
        self.add_piece(c,b,[1,7])
        self.add_piece(b,b,[2,7])
        self.add_piece(q,b,[3,7])
        self.add_piece(k,b,[4,7])
        self.add_piece(b,b,[5,7])
        self.add_piece(c,b,[6,7])
        self.add_piece(r,b,[7,7])
        for x in range(0,8):
            self.add_piece(p,b,[x,6])

#empty the board and reset the counter
    def empty_board(self):
        for y in range (0,8):
            for x in range (0,8):
                self.board[x][y] = 0
        self.counter = 0

# give a score to the current status of the board
    def evaluate_board(self):
        board_value = 0
        for y in range(0,8):
            for x in range(0,8):
                square_content = self.read([x,y])
                try:
                    if square_content.piece_color == w:
                        board_value += square_content.piece_value
                    if square_content.piece_color == b:
                        board_value -= square_content.piece_value
#0 is equally good for balck and white, <0 is good for black, >0 is good for
#white
                except:
                    if square_content == 0: pass
                    else: raise AssertionError("Unexpected value at "
                                               +str([x,y])+
                                               ": "+str(square_content))
        return board_value

#removes a piece form the board
    def remove_piece(self,coordinate_list):
        x,y = coordinate_list[0],coordinate_list[1]
        self.board[x][y] = 0

#take a position, read its content, move the piece on the board to the
#specified position and update the piece internal memory
    def move_piece(self,starting_position,arriving_position):
        my_piece = self.read(starting_position)
        my_color = my_piece.piece_color
        piece_type = my_piece.name
        if automated == False:
            my_piece.calculate_piece_possibles()
#refresh the available moves
            possible_moves = my_piece.piece_possibles
            assert arriving_position in possible_moves
# assert move validity if the human is playing
        self.remove_piece(starting_position)
        self.add_piece(piece_type,my_color,arriving_position)
#update the board removing a piece from the starting position and adding it at
#the destination, if an opponent piece is captured it is just sovrascribed, no
#need to explicitly destroy it
        self.counter += 1
# increment counter variable by 1

#return the content of a cell
    def read(self,coordinate_list):
        try:
            x,y = coordinate_list[0],coordinate_list[1]
            assert(x>=0 and y>=0)
#otherways it calls non-existent squares from the end of the list
            return self.board [x][y]
        except: return out_of_range

#human-readable representation of the checkboard
    def show_board(self):
       # │ ─┌ ┐ └ ┘ ┬ ┴ ├ ┤ ┼
        print("  ┌───┬───┬───┬───┬───┬───┬───┬───┐")
        for y in range(7,-1,-1):
#the 3rd argument is the incremnent of the range, which has to go backwards in
#order to put white at the bottom
            print(str(y+1),end="")
            for x in range(0,8):
                try:
                    if showing_possibles == False:
#default value
                        print(" │ ",end="")
#| symbol preceding the element, without \n (end="")
                        if self.board[x][y].piece_color == w:
                            print(self.board[x][y].symbol[0],end="")
                        elif self.board[x][y].piece_color == b:
                            print(self.board[x][y].symbol[1],end="")
#the first character of the .symbol string is for white, the second for black
                    elif showing_possibles == True:
#True only if the function is called by piece.show_piece_possibles()
                        if [x,y] in showing_moves:
#if the current position is among the ones in which the current piece can move
                            if self.board[x][y] == 0:
#if the square is empty the formatting is the same as always because we will
#add just an x
                                print(" │ ",end="")
                            else:
                                print(" │",end="")
#if the square is already occupied i want to print a space less, because i will
#print both an x an the occupying piece
                                if self.board[x][y].piece_color == w:
                                    print(self.board[x][y].symbol[0],end="")
                                elif self.board[x][y].piece_color == b:
                                    print(self.board[x][y].symbol[1],end="")
#the usual if cycle for printing the right color
                            print("x",end="")
#print x in the treathened squares
                        else:
#if current square is not treathened by current piece, do the usual cycle
                            print(" │ ",end="")
                            if self.board[x][y].piece_color == w:
                                print(self.board[x][y].symbol[0],end="")
                            elif self.board[x][y].piece_color == b:
                                print(self.board[x][y].symbol[1],end="")
                except: print(" ",end="")
#leave a blank space for empty cells, which raise an error
            print(" │ ")
#print the row number at the end of the row itself, and prints a different row
#for the last iteration
            if y>0: print("  ├───┼───┼───┼───┼───┼───┼───┼───┤")
            elif y==0: print("  └───┴───┴───┴───┴───┴───┴───┴───┘")
#add a delimiting line after each row
        print ("    A   B   C   D   E   F   G   H")
#a representation of the columns, written under them

########## All the classes for the different figures of the game
#this class is common to all pieces and sets shared properties
class piece:
    def give_color(self,color):
        self.piece_color = color
        if self.piece_color == w:
#the direction variables is used for keeping track of the forward
#direction, mainly for pawns
            self.direction = 1
        elif self.piece_color == b:
            self.direction = -1
        else:
            raise AssertionError("The color variable at square " +
                                 self.position  + " has an unexpected value: "
                                 + self.piece_color)

#stores the position in [x,y] format
    def update_position(self,coordinate_list):
        self.position = coordinate_list

#human readable form of the previous function
    def read_position_letteral(self):
        letter_coordinate = xy_to_letter(self.position)
        return letter_coordinate

#prints a chessboard with x on the possible moves for the piece from the
#current position
    def show_piece_possibles(self):
        global showing_possibles
        global showing_moves
#these globals are used by the game.show_board() function
        showing_possibles = True
        showing_moves = self.calculate_piece_possibles()
        current_game.show_board()
        showing_possibles = False
        showing_moves = []

#this class comprehends pieces capable of moving for a variable amount of
#squares in a given direction
class long_range_piece(piece):
#horizontal sliding
    def h_slide(self,directional_length):
        x,y = self.position[0],self.position[1]
        final_x = x + directional_length
        final_y = y
        return  [final_x,final_y]

#vertical sliding
    def v_slide(self,directional_length):
        x,y = self.position[0],self.position[1]
        final_x = x
        final_y = y + directional_length
        return  [final_x,final_y]

#left-down/right-up sliding
    def ru_slide(self,directional_length):
        x,y = self.position[0],self.position[1]
        final_x = x + directional_length
        final_y = y + directional_length
        return  [final_x,final_y]

#right-down/left-up sliding
    def lu_slide(self,directional_length):
        x,y = self.position[0],self.position[1]
        final_x = x - directional_length
        final_y = y + directional_length
        return  [final_x,final_y]

#take a list of moves and calculate the ending positions accordingly
    def calculate_piece_possibles(self):
        self.piece_possibles = []
        for move in self.all_moves:
#loop trough all the moves
            for direction in [1,-1]:
#calculate both in the fw and rv directions
                for length in range(1,8):
#8 is the maximum range possible in the board
#the innermost loop is length, beacause I want to stop calculating the given
#direction after an unsuccesfull trial
                    directional_length = length*direction
                    my_move = move(directional_length)
                    new_square_content = current_game.read(my_move)
                    try:
                        assert new_square_content == 0
#avoid adding to the list squares not existing or not empty
                        self.piece_possibles.append(my_move)
                    except:
                        try:
                            assert (new_square_content.piece_color ==
                                   opposite_color(self.piece_color))
                            self.piece_possibles.append(my_move)
                            break
#even if there is a piece i can move and eat it if it's not mine, but then I
#have to break because i can eat only the first one that I encounter
                        except: break
#the first positions calculated are the nearest ones, breaking the loop avoids
#wasting time in calculating impossible positions
        return self.piece_possibles

class pawn(piece):
# create human readable name variable for the current piece
    def __init__(self):
        self.name = p
        self.symbol = "♙♟"
        self.all_moves = (self.move_u1,self.move_ur,
                          self.move_ul)
        self.piece_value = 1

#list of all allowed moves
#simple advancement by 1
    def move_u1(self):
        x,y = self.position[0],self.position[1]
        final_x = x
        final_y = y + 1*self.direction
        my_move = [final_x,final_y]
        new_square_content = current_game.read(my_move)
        try:
            assert new_square_content == 0
            self.move_is_allowed = True
#can move in this direction only if there is an empty square
        except: self.move_is_allowed = False
        return my_move

#eat right
    def move_ur(self):
        x,y = self.position[0],self.position[1]
        final_x = x + 1*self.direction
        final_y = y + 1*self.direction
        my_move = [final_x,final_y]
        new_square_content = current_game.read(my_move)
        try:
            assert (new_square_content.piece_color ==
                   opposite_color(self.piece_color))
#can move in this direction only if there is an opponent
            self.move_is_allowed = True
        except: self.move_is_allowed = False
        return my_move

#eat left
    def move_ul(self):
        x,y = self.position[0],self.position[1]
        final_x = x - 1*self.direction
        final_y = y + 1*self.direction
        my_move = [final_x,final_y]
        new_square_content = current_game.read(my_move)
        try:
            assert (new_square_content.piece_color ==
                   opposite_color(self.piece_color))
#can move in this direction only if there is an opponent
            self.move_is_allowed = True
        except: self.move_is_allowed = False
        return my_move

#special moves
#advancement by 2 at the beginning
   # def move_u2(self):
   #     final_x = self.x + 2*self.direction
   #     final_y = self.y
   #     return xy_to_letter(final_x,final_y)

# return a list of possible ending positions using the coded moves
    def calculate_piece_possibles(self):
        self.piece_possibles = []
        for move in self.all_moves:
            my_move = move()
            new_square_content = current_game.read(my_move)
            try:
                assert self.move_is_allowed == True
#the conditions for each move are coded in the moves themselves, because of
#their complexity
                self.piece_possibles.append(my_move)
            except: pass
        return self.piece_possibles


class rook(long_range_piece):
    def __init__(self):
        self.name = r
        self.symbol = "♖♜"
        self.all_moves = (self.h_slide,self.v_slide)
#rook moves straight
        self.piece_value = 5

class knight(piece):
    def __init__(self):
        self.name = c
        self.symbol = "♘♞"
        self.piece_value = 3

    def calculate_piece_possibles(self):
        self.piece_possibles = []
        x,y = self.position[0],self.position[1]
        self.all_moves = ()
        for a in (1,-1):
            for b in (2,-2):
                increment = (a,b)
                for i in (0,1):
                    x_increment,y_increment = increment[i],increment[1-i]
#possible increments of both x and y are 2 and 1, in both directions
#if x is 1 y is 3, and vice-versa
                    final_x = x + x_increment
                    final_y = y + y_increment
                    my_move = [final_x,final_y]
                    new_square_content = current_game.read(my_move)
                    try:
                        assert new_square_content == 0
#avoid adding to the list squares not existing or not empty
                        self.piece_possibles.append(my_move)
                    except:
                        try:
                            assert (new_square_content.piece_color ==
                                   opposite_color(self.piece_color))
                            self.piece_possibles.append(my_move)
#even if there is a piece i can move and eat it if it's not mine
                        except: pass
        return self.piece_possibles


class bishop(long_range_piece):
    def __init__(self):
        self.name = b
        self.symbol = "♗♝"
        self.all_moves = (self.ru_slide,self.lu_slide)
#bishop moves diagonally
        self.piece_value = 3

class queen(long_range_piece):
    def __init__(self):
        self.name = q
        self.symbol = "♕♛"
        self.all_moves = (self.h_slide,self.v_slide,self.ru_slide,self.lu_slide)
#queen moves in all directions
        self.piece_value = 8

class king(piece):
    def __init__(self):
        self.name = k
        self.symbol = "♔♚"
        self.piece_possibles = []
        self.all_moves = (self.move_d,self.move_l,self.move_r,self.move_u,
                          self.move_dl,self.move_dr,self.move_ul,self.move_ur)
        self.piece_value = 1000

#list of all allowed moves (up,down,left,right and the 4 diagonals)
    def move_u(self):
        x,y = self.position[0],self.position[1]
        final_x = x
        final_y = y + 1
        return  [final_x,final_y]

    def move_d(self):
        x,y = self.position[0],self.position[1]
        final_x = x
        final_y = y - 1
        return  [final_x,final_y]

    def move_l(self):
        x,y = self.position[0],self.position[1]
        final_x = x - 1
        final_y = y
        return  [final_x,final_y]

    def move_r(self):
        x,y = self.position[0],self.position[1]
        final_x = x + 1
        final_y = y
        return  [final_x,final_y]

    def move_ul(self):
        x,y = self.position[0],self.position[1]
        final_x = x - 1
        final_y = y + 1
        return  [final_x,final_y]

    def move_ur(self):
        x,y = self.position[0],self.position[1]
        final_x = x + 1
        final_y = y + 1
        return  [final_x,final_y]

    def move_dl(self):
        x,y = self.position[0],self.position[1]
        final_x = x - 1
        final_y = y - 1
        return  [final_x,final_y]

    def move_dr(self):
        x,y = self.position[0],self.position[1]
        final_x = x + 1
        final_y = y - 1
        return  [final_x,final_y]

# return a list of possible ending positions using the coded moves
    def calculate_piece_possibles(self):
        self.piece_possibles = []
        for move in self.all_moves:
            my_move = move()
            new_square_content = current_game.read(my_move)
            try:
                assert new_square_content == 0
#avoid adding to the list squares not existing or not empty
                self.piece_possibles.append(my_move)
            except:
                try:
                    assert (new_square_content.piece_color ==
                            opposite_color(self.piece_color))
                    self.piece_possibles.append(my_move)
#even if there is a piece i can move and eat it if it's not mine
                except: pass
        return self.piece_possibles

###############################################################################
###############################################################################
###############################################################################
# Test code area
game1 = game()
current_game.initialise()
current_game.show_board()
#current_game.empty_board()
#current_game.show_board()
#current_game.add_piece(c,w,[6,2])
#current_piece = current_game.board[6][2]
#current_piece.show_piece_possibles()
print("\nboard evaluation: "+str(current_game.evaluate_board()))
#print(current_piece.position)
#print(current_piece.name)
#current_piece.calculate_piece_possibles()
#moves = []
#for i in current_piece.piece_possibles:
#    moves.append(xy_to_letter(i))
#print (moves)
#current_game.move_piece([4,4],[7,7])
#current_game.show_board()
#current_piece = current_game.board[7][7]
#print(current_piece.position)
#print(current_piece.name)
#current_piece.calculate_piece_possibles()
#moves = []
#for i in current_piece.piece_possibles:
#    moves.append(xy_to_letter(i))
#print (moves)
#print(game1.board[0][0].position)
#print(game1.board[0][0].piece_possibles())
#for x in range(0,8):
#    for y in range(0,8):
#        print(game1.board[x][y])
#        try:
#            print(game1.board[x][y].position)
#            print(game1.board[x][y].color)
#        except:
#            print("empty cell")
