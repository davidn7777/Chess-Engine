'''
Base chess game for 2 human players with no model implemetation
'''
import pygame
import sys
import chess
import chess.svg
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

starting_order = {}

for i in range(8):
    for j in range(8):
        starting_order[i, j] = None

#rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

def board_from_fen(fen):
    i = 0
    j = 0
    for char in fen:
        if char == '/':
            j += 1
            i = 0
        elif char.isnumeric():
            spaces = int(char) #char == '8'
            for pivot in range(spaces):
                starting_order[i, j] = None
                i += 1
        elif char.isalpha():
            starting_order[i, j] = char_to_pygame_image(char)
            i += 1
        else:
            break

def char_to_pygame_image(char):
    if char == 'p':
        return pygame.image.load('../src/img/b_pawn.png')
    elif char == 'r':
        return pygame.image.load('../src/img/b_rook.png')
    elif char == 'n':
        return pygame.image.load('../src/img/b_knight.png')
    elif char == 'b':
        return pygame.image.load('../src/img/b_bishop.png')
    elif char == 'q':
        return pygame.image.load('../src/img/b_queen.png')
    elif char == 'k':
        return pygame.image.load('../src/img/b_king.png')
    elif char == 'P':
        return pygame.image.load('../src/img/w_pawn.png')
    elif char == 'R':
        return pygame.image.load('../src/img/w_rook.png')
    elif char == 'N':
        return pygame.image.load('../src/img/w_knight.png')
    elif char == 'B':
        return pygame.image.load('../src/img/w_bishop.png')
    elif char == 'Q':
        return pygame.image.load('../src/img/w_queen.png')
    elif char == 'K':
        return pygame.image.load('../src/img/w_king.png')


class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.colour = WHITE
        self.occupied = None

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.colour, (self.x, self.y, WIDTH / 8, WIDTH / 8))

    def setup(self, WIN):
        if starting_order[(self.row, self.col)]:
            if starting_order[(self.row, self.col)] == None:
                pass
            else:
                WIN.blit(starting_order[(self.row, self.col)], (self.x, self.y))
        """
        For now it is drawing a rectangle but eventually we are going to need it
        to use blit to draw the chess pieces instead
        """

def make_grid(rows, width):
    grid = []
    gap = WIDTH // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(j, i, gap)
            grid[i].append(node)
            if (i + j) % 2 == 1:
                grid[i][j].colour = GREY
    return grid
"""
This is creating the nodes thats are on the board(so the chess tiles)
I've put them into a 2d array which is identical to the dimesions of the chessboard
"""

def draw_grid(win, rows, width):
    gap = width // 8
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))
    """
    The nodes are all white so this we need to draw the grey lines that separate all the chess tiles
    from each other and that is what this function does
    """

def update_display(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)
            spot.setup(win)
    draw_grid(win, rows, width)
    pygame.display.update()

def Find_Node(pos, WIDTH):
    interval = WIDTH / 8
    y, x = pos
    rows = y // interval
    columns = x // interval
    return int(rows), int(columns)


"""
This takes in 2 co-ordinate parameters which you can get as the position of the piece and then the position of the node it is moving to
you can get those co-ordinates using my old function for swap
"""

def selected_square(x, y):
    y = 8 - y
    y = str(y)
    alpha_x = ""

    alpha_x = str(chr(x+97))
    AN = alpha_x + y

    return AN

def valid_selection(selection,count,grid,board):
    highlights = []
    identifier = "'" + selection

    if identifier in str(list(board.legal_moves)):
        #print("Valid Selection")
        selection1 = selection

        for i in range(len(list(board.legal_moves))):
            check = str(list(board.legal_moves)[i])[0:2]
            if selection1 == check:
                highlights.append(str(list(board.legal_moves)[i])[2:4])
        #print(highlights)


        for j in range(len(highlights)):
            ypos = int(highlights[j][1]) - 1

            if highlights[j][0] == "a":
                xpos = 0
            elif highlights[j][0] == "b":
                xpos = 1
            elif highlights[j][0] == "c":
                xpos = 2
            elif highlights[j][0] == "d":
                xpos = 3
            elif highlights[j][0] == "e":
                xpos = 4
            elif highlights[j][0] == "f":
                xpos = 5
            elif highlights[j][0] == "g":
                xpos = 6
            elif highlights[j][0] == "h":
                xpos = 7

            grid[7-ypos][xpos].colour = BLUE  

        #print(ypos)
            

    else:
        #print("Invalid Selection")
        count = 0
    return selection, count, grid

def remove_highlight(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i+j)%2 == 0:
                grid[i][j].colour = WHITE
            else:
                grid[i][j].colour = GREY
    return grid



def main():
    board = chess.Board()

    fen_start = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    board = chess.Board(fen_start)
    board_from_fen(fen_start)

    """ 
    This is creating the window that we are playing on, it takes a tuple argument which is the dimensions of the window so in this case 800 x 800px
    """

    pygame.display.set_caption("Chiggity Chess")

    selected = False
    select_move = ''
    moves = 0
    piece_to_move=[]
    grid = make_grid(8, WIDTH)
    count = 0
    
    #print(str(list(board.legal_moves)))
    while True:
        pygame.time.delay(50) ##stops cpu dying
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            """
            This quits the program if the player closes the window
            """

            if event.type == pygame.MOUSEBUTTONDOWN:
                count = count + 1
                pos = pygame.mouse.get_pos()
                x, y = Find_Node(pos, WIDTH)
                selection = selected_square(x, y)
                #print("Alpha-Numeric: ", selection)
                selected = False
                if (count % 2) == 0: 
                    selection2 = selection
                    if selection2 == selection1:
                        count = 0
                        #print("Invalid Selection")
                        remove_highlight(grid)
                else:
                    selection1, count, grid = valid_selection(selection,count,grid,board)
                
                if count == 2:
                    select_move = selection1 + selection2
                #print(select_move)
                if len(select_move) == 4:
                    if chess.Move.from_uci(select_move) in board.legal_moves:
                        board.push_uci(select_move)
                        #print("Move Sucessful")
                        remove_highlight(grid)
                        select_move = ''
                        #print(board.fen())
                        fen = board.fen()
                        board_from_fen(fen)
                        count = 0
                    else:
                        select_move = ''
                        #print("Move Failed")
                        remove_highlight(grid)
                        count = 0

            update_display(WIN, grid, 8, WIDTH)



WHITE = (240, 216, 191)
GREY = (186, 85, 70)
BLUE = (220, 172, 230)
BLACK = (0, 0, 0)
WIDTH = 504

WIN = pygame.display.set_mode((WIDTH, WIDTH))

main()