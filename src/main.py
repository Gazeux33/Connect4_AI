import random
from copy import deepcopy
import pygame
import sys

from MCTS import MonteCarlo



pygame.init()
YELLOW_COLOR = 220, 215, 20
RED_COLOR = 255, 0, 0
EMPTY_COLOR = 255, 255, 255
BOARD_COLOR = 0, 0, 255


# yellow -> 1
# red -> -1

def get_color_player(number):
    if number == -1:
        return "red"
    return "yellow"


class Connect4:
    def __init__(self):
        self._rows = 6
        self._cols = 7
        self._board = None
        self._current_turn = None
        self.reset()
        self.last_move = None
        self.game_over = False

        pygame.display.set_caption("Connect4")

    def play(self):
        screen = pygame.display.set_mode((700, 600))
        player_number = random.choice([1, -1])
        ia_number = 1
        if player_number == 1:
            ia_number = -1

        print(f"ia color:{get_color_player(ia_number)}")
        print(f"player color:{get_color_player(player_number)}")

        while True:
            play = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.game_over:
                        self.reset()
                if event.type == pygame.MOUSEBUTTONDOWN and self._current_turn == player_number and not self.game_over:
                    move = self.player_play(screen, pygame.mouse.get_pos())
                    self.next_turn(move)
                    play = True

            if self._current_turn == ia_number and not self.game_over and not play:
                move = self.ia_play()
                self.next_turn(move)

            self.display_board(screen)
            pygame.display.flip()

    def ia_play(self):
        ia = MonteCarlo(self, 1000)
        column = ia.monte_carlo_tree_search()
        return self.make_move(column, self._current_turn)

    def player_play(self, screen, pos_mouse):
        pos_x, pos_y = pos_mouse
        column_width = screen.get_width() / 7
        column = int(pos_x // column_width)
        next_empty_position = self.next_empty_position(column)
        if next_empty_position is not None:
            return self.make_move(column, self._current_turn)

    def next_turn(self, move):
        if self.check_win(move):
            self.game_over = True
            print(f"gg a {get_color_player(self._current_turn)}")
        elif self.game_finish():
            self.game_over = True
            print(f"it's a draw")
        else:
            self._current_turn *= -1
            print()

    def check_draw(self):
        for row in self._board:
            for element in row:
                if element == 0:
                    return False
        return True

    def next_empty_position(self, column):
        for i in range(len(self._board) - 1, -1, -1):
            if self._board[i][column] == 0:
                return i
        return None

    def reset(self):
        self._board = [[0 for _ in range(self._cols)] for _ in range(self._rows)]
        self._current_turn = random.choice((-1, 1))
        self.game_over = False

    def check_win(self, pos):
        r = pos[0]
        c = pos[1]
        player = self._board[r][c]

        # Horizontal check
        for col in range(c - 3, c + 1):
            if col >= 0 and col + 3 < self._cols:
                if all(self._board[r][col + i] == player for i in range(4)):
                    return True

        # Vertical check
        for row in range(r - 3, r + 1):
            if row >= 0 and row + 3 < self._rows:
                if all(self._board[row + i][c] == player for i in range(4)):
                    return True

        # Diagonal checks
        for i in range(-3, 1):
            # Diagonal down-right
            if c + i >= 0 and r + i >= 0 and c + i + 3 < self._cols and r + i + 3 < self._rows:
                if all(self._board[r + i + j][c + i + j] == player for j in range(4)):
                    return True

            # Diagonal up-right
            for i in range(-3, 1):
                if c + i >= 0 and r - i - 3 >= 0 and c + i + 3 < self._cols and r - i < self._rows:
                    if all(0 <= r - i - j < self._rows and 0 <= c + i + j < self._cols and self._board[r - i - j][
                        c + i + j] == player for j in range(4)):
                        return True
        return False

    def make_move(self, column, turn):
        r = self.next_empty_position(column)
        self._board[r][column] = turn
        self.last_move = r, column
        return r, column

    def get_free_columns(self):
        return [i for i in range(7) if self._board[0][i] == 0]

    def display_board(self, screen):
        screen.fill(BOARD_COLOR)
        x_csl = screen.get_width() / 7
        y_scl = screen.get_height() / 6
        for i in range(6):
            for j in range(7):
                number = self._board[i][j]
                pygame.draw.circle(screen, self.get_color(number), (j * x_csl + x_csl / 2, i * y_scl + y_scl / 2),
                                   40)

    @staticmethod
    def get_color(number):
        if number == 1:
            return YELLOW_COLOR
        if number == -1:
            return RED_COLOR
        return EMPTY_COLOR

    def copy_state(self):
        return deepcopy(self)

    def set_board(self, board):
        self._board = board

    def print_board(self):
        for row in self._board:
            print(row)

    def game_finish(self):
        if self.check_draw():
            return True
        for i in range(6):
            for j in range(7):
                if self._board[i][j] != 0:
                    if self.check_win((i, j)):
                        return True
        return False


if __name__ == '__main__':
    game = Connect4()
    game.play()
