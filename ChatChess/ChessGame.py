import chess
import chess.svg

def gen_board(fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
    board = chess.Board(fen)
    board_img = chess.svg.board((board),size = 600)
    outputfile = open('board.svg', "w")
    outputfile.write(board_img)
    outputfile.close()
    return fen

def get_legal(fen):
    board = chess.Board(fen)
    return [str(list(board.legal_moves)[i]) for i in range(len(list(board.legal_moves)))]

def move(fen, uci):
    board = chess.Board(fen)
    board.push_uci(uci)
    fen = board.fen()

    fen = gen_board(fen)
    return fen