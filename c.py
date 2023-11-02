import pygame
pygame.init()
from util import *


WIDTH, HEIGHT = 800, 800  # Size of the game window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

BOARD = pygame.image.load('path_to_board_image.png')
# Similarly, load images for all pieces
B_PAWN = pygame.image.load('path_to_black_pawn_image.png')
B_ROOK = pygame.image.load('path_to_black_rook_image.png')
B_KNIGHT = pygame.image.load('path_to_black_knight_image.png')
B_BISHOP = pygame.image.load('path_to_black_bishop_image.png')
B_QUEEN = pygame.image.load('path_to_black_queen_image.png')
B_KING = pygame.image.load('path_to_black_king_image.png')

W_PAWN = pygame.image.load('path_to_white_pawn_image.png')
W_ROOK = pygame.image.load('path_to_white_rook_image.png')
W_KNIGHT = pygame.image.load('path_to_white_knight_image.png')
W_BISHOP = pygame.image.load('path_to_white_bishop_image.png')
W_QUEEN = pygame.image.load('path_to_white_queen_image.png')
W_KING = pygame.image.load('path_to_white_king_image.png')


class Piece:
    def __init__(self, color, type):
        self.color = color
        self.type = type

    def __str__(self):
        return f"{self.color[0]}{self.type[0]}"

board = [[None for _ in range(8)] for _ in range(8)]


for i in range(8):
    board[1][i] = Piece("black", "pawn")
    board[6][i] = Piece("white", "pawn")

# Rooks
board[0][0], board[0][7] = Piece("black", "rook"), Piece("black", "rook")
board[7][0], board[7][7] = Piece("white", "rook"), Piece("white", "rook")

# Knights
board[0][1], board[0][6] = Piece("black", "knight"), Piece("black", "knight")
board[7][1], board[7][6] = Piece("white", "knight"), Piece("white", "knight")

# Bishops
board[0][2], board[0][5] = Piece("black", "bishop"), Piece("black", "bishop")
board[7][2], board[7][5] = Piece("white", "bishop"), Piece("white", "bishop")

# Queens
board[0][3] = Piece("black", "queen")
board[7][3] = Piece("white", "queen")

# Kings
board[0][4] = Piece("black", "king")
board[7][4] = Piece("white", "king")






# ... similarly for other pieces
def valid_moves(piece, x, y):
    moves = []
    # Example for pawn:
    if piece.type == "pawn":
        if piece.color == "white":
            if y > 0 and not board[y-1][x]:
                moves.append((x, y-1))
            # Add conditions for capturing, en passant, etc.
        else:
            if y < 7 and not board[y+1][x]:
                moves.append((x, y+1))

    if piece.type == "rook":
        if piece.color == "white":
            if y > 0 and not board[y - 1][x]:
                moves.append((x, y - 1))

        else:
            if y < 7 and not board[y + 1][x]:
                moves.append((x, y + 1))

    if piece.type == "bishop":
        if piece.color == "white":
            if y > 0 and not board[y - 1][x]:
                moves.append((x, y - 1))
        else:
            if y < 7 and not board[y + 1][x]:
                moves.append((x, y + 1))
    if piece.type == "queen":
        if piece.color == "white":
            if y > 0 and not board[y - 1][x]:
                moves.append((x, y - 1))
        else:
            if y < 7 and not board[y + 1][x]:
                moves.append((x, y + 1))
    if piece.type == "king":
        if piece.color == "white":
            if y > 0 and not board[y - 1][x]:
                moves.append((x, y - 1))
        else:
            if y < 7 and not board[y + 1][x]:
                moves.append((x, y + 1))





    return moves












def draw_window():
    win.blit(BOARD, (0, 0))
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            x, y = j * 100, i * 100
            if piece:
                if piece.color == "white":
                    if piece.type == "pawn":
                        win.blit(W_PAWN, (x, y))
                    elif piece.type == "rook":
                        win.blit(W_ROOK, (x, y))
                    elif piece.type == "knight":
                        win.blit(W_KNIGHT, (x, y))
                    elif piece.type == "bishop":
                        win.blit(W_BISHOP, (x, y))
                    elif piece.type == "queen":
                        win.blit(W_QUEEN, (x, y))
                    elif piece.type == "king":
                        win.blit(W_KING, (x, y))
                else:
                    if piece.type == "pawn":
                        win.blit(B_PAWN, (x, y))
                    elif piece.type == "rook":
                        win.blit(B_ROOK, (x, y))
                    elif piece.type == "knight":
                        win.blit(B_KNIGHT, (x, y))
                    elif piece.type == "bishop":
                        win.blit(B_BISHOP, (x, y))
                    elif piece.type == "queen":
                        win.blit(B_QUEEN, (x, y))
                    elif piece.type == "king":
                        win.blit(B_KING, (x, y))
    pygame.display.update()


selected_piece = None
selected_position = None


# ... [The rest of the code remains unchanged]

def main():
    global selected_piece, selected_position
    current_turn = "white"
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // 100, y // 100
                if not selected_piece:
                    if board[row][col] and board[row][col].color == current_turn:
                        selected_piece = board[row][col]
                        selected_position = (row, col)
                else:
                    if (row, col) in valid_moves(selected_piece, selected_position[0], selected_position[1]):
                        board[row][col] = selected_piece
                        board[selected_position[0]][selected_position[1]] = None
                        selected_piece = None
                        selected_position = None
                        current_turn = "black" if current_turn == "white" else "white"
                    else:
                        print("Invalid move!")

        draw_window()

if __name__ == "__main__":
    main()
    pygame.quit()

