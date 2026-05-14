import sys
import pygame
import numpy as np

pygame.init()

# Colors
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)

#Proporition & Size
WIDTH = 600
HEIGHT = 700
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS 
CIRCLE_RADIUS = SQUARE_SIZE // 3 
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')
font = pygame.font.Font(None, 36)

board = np.zeros((BOARD_ROWS, BOARD_COLS), dtype=int)
scores = {'player': 0, 'ai': 0, 'draws': 0}
player = 1
game_over = False
clock = pygame.time.Clock()


def draw_lines(color=WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(
            screen,
            color,
            (0, SQUARE_SIZE * i),
            (WIDTH, SQUARE_SIZE * i),
            LINE_WIDTH
        )
        pygame.draw.line(
            screen,
            color,
            (SQUARE_SIZE * i, 0),
            (SQUARE_SIZE * i, WIDTH),
            LINE_WIDTH
        )


def draw_figures(color=WHITE):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            y = row * SQUARE_SIZE + SQUARE_SIZE // 2

            if board[row][col] == 1:
                pygame.draw.circle(
                    screen,
                    color,
                    (x, y),
                    CIRCLE_RADIUS,
                    CIRCLE_WIDTH
                )
            elif board[row][col] == 2:
                offset = SQUARE_SIZE // 4
                pygame.draw.line(
                    screen,
                    color,
                    (x - offset, y - offset),
                    (x + offset, y + offset),
                    CROSS_WIDTH
                )
                pygame.draw.line(
                    screen,
                    color,
                    (x - offset, y + offset),
                    (x + offset, y - offset),
                    CROSS_WIDTH
                )


def draw_score():
    pygame.draw.rect(screen, BLUE, (0, WIDTH, WIDTH, 100))

    texts = [
        (f"Player: {scores['player']}", (20, WIDTH + 10)),
        (f"AI: {scores['ai']}", (20, WIDTH + 40)),
        (f"Draws: {scores['draws']}", (250, WIDTH + 10)),
        ("Press R to Restart", (250, WIDTH + 40))
    ]

    for text, pos in texts:
        screen.blit(font.render(text, True, WHITE), pos)


def mark_square(row, col, p):#هنا حطينا اللاعب او ال aI في المربع
    board[row][col] = p


def available_square(row, col):# هنا بعمل CHECK علي كل مربع فاضي ولا لا 
    return board[row][col] == 0


def is_board_full(check_board=None):
    if check_board is None:
        check_board = board
    return not np.any(check_board == 0)


def check_win(p, check_board=None):
    if check_board is None:
        check_board = board

    for i in range(3):
        if np.all(check_board[i, :] == p) or np.all(check_board[:, i] == p):
            return True

    if check_board[0][0] == p and check_board[1][1] == p and check_board[2][2] == p:
        return True

    if check_board[0][2] == p and check_board[1][1] == p and check_board[2][0] == p:
        return True

    return False


def minimax(minimax_board, is_maximizing):
    if check_win(2, minimax_board):
        return 1
    if check_win(1, minimax_board):
        return -1
    if is_board_full(minimax_board):
        return 0

    best_score = -1000 if is_maximizing else 1000
    p = 2 if is_maximizing else 1

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if minimax_board[row][col] == 0:
                minimax_board[row][col] = p
                score = minimax(minimax_board, not is_maximizing)
                minimax_board[row][col] = 0

                if is_maximizing:
                    best_score = max(best_score, score)
                else:
                    best_score = min(best_score, score)

    return best_score


def best_move():
    best_score = -1000
    move = None

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board.copy(), False)
                board[row][col] = 0

                if score > best_score:
                    best_score = score
                    move = (row, col)

    if move:
        mark_square(move[0], move[1], 2)
        return True
    return False


def restart_game():
    global board, game_over, player
    board = np.zeros((BOARD_ROWS, BOARD_COLS), dtype=int)
    game_over = False
    player = 1


def get_game_color():
    if check_win(1):
        return GREEN
    elif check_win(2):
        return RED
    else:
        return GRAY


def handle_player_move(mouseY, mouseX):
    global player, game_over                           

    if mouseY >= 3 or not available_square(mouseY, mouseX):
        return

    mark_square(mouseY, mouseX, player)

    if check_win(player):
        game_over = True
        scores['player'] += 1
    elif is_board_full():
        game_over = True
        scores['draws'] += 1
    else:
        player = 2
        if best_move():
            if check_win(2):
                game_over = True
                scores['ai'] += 1
            elif is_board_full():
                game_over = True
                scores['draws'] += 1
        player = 1


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = event.pos[1] // SQUARE_SIZE
            handle_player_move(mouseY, mouseX)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            restart_game()

    screen.fill(BLACK)

    if game_over:
        color = get_game_color()
        draw_lines(color)
        draw_figures(color)
    else:
        draw_lines()
        draw_figures()

    draw_score()
    pygame.display.update()
    clock.tick(60)