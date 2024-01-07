import random
import pygame
import sys

pygame.init()
YELLOW_COLOR = 220, 215, 20
RED_COLOR = 255, 0, 0
EMPTY_COLOR = 255, 255, 255
BOARD_COLOR = 0, 0, 255


# yellow -> 1
# red -> -1

class Connect4:
    def __init__(self):
        self._rows = 6
        self._cols = 7
        self._board = None
        self._current_turn = None
        self.reset()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((700, 600))
        pygame.display.set_caption("Connect4")

    def play(self):
        game_over = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and game_over:
                        self.reset()
                        game_over = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not game_over:
                        posx, posy = pygame.mouse.get_pos()
                        column_width = self.screen.get_width() / 7
                        column = int(posx // column_width)
                        next_empty_position = self.next_empty_position(column)
                        if next_empty_position is not None:
                            if next_empty_position is not None:
                                self.make_move(column)
                                result = self.check_win((next_empty_position, column))
                                print(result)
                            if result is not None:
                                game_over = True
                                if result == self._current_turn:
                                    print(f"gg a {self.get_color_player()}")
                                else:
                                    print("it's a draw")
                            else:
                                self._current_turn *= -1
                self.display_board()
                pygame.display.flip()
                self.clock.tick(60)

    def next_empty_position(self, column):
        for i in range(len(self._board) - 1, -1, -1):
            if self._board[i][column] == 0:
                return i
        return None

    def get_color_player(self):
        if self._current_turn == -1:
            return "red"
        return "yellow"

    def reset(self):
        self._board = [[0 for _ in range(self._cols)] for _ in range(self._rows)]
        print(self._board)
        self._current_turn = random.choice((-1, 1))

    def check_win(self, pos):
        r = pos[0]
        c = pos[1]
        player = self._board[r][c]

        # Horizontal check
        for col in range(c - 3, c + 1):
            if col >= 0 and col + 3 < self._cols:
                if all(self._board[r][col + i] == player for i in range(4)):
                    return player

        # Vertical check
        for row in range(r - 3, r + 1):
            if row >= 0 and row + 3 < self._rows:
                if all(self._board[row + i][c] == player for i in range(4)):
                    return player

        # Diagonal checks
        for i in range(-3, 1):
            # Diagonal down-right
            if c + i >= 0 and r + i >= 0 and c + i + 3 < self._cols and r + i + 3 < self._rows:
                if all(self._board[r + i + j][c + i + j] == player for j in range(4)):
                    return player

            # Diagonal up-right
            for i in range(-3, 1):
                if c + i >= 0 and r - i - 3 >= 0 and c + i + 3 < self._cols and r - i < self._rows:
                    if all(0 <= r - i - j < self._rows and 0 <= c + i + j < self._cols and self._board[r - i - j][c + i + j] == player for j in range(4)):
                        return player

        # Draw check
        if all(0 not in row for row in self._board):
            return 0

        return None

    def make_move(self, column):
        self._board[self.next_empty_position(column)][column] = self._current_turn

    def get_free_columns(self):
        return [i for i in range(7) if self._board[0][i] == 0]

    def display_board(self):
        self.screen.fill(BOARD_COLOR)
        x_csl = self.screen.get_width() / 7
        y_scl = self.screen.get_height() / 6
        for i in range(6):
            for j in range(7):
                number = self._board[i][j]
                pygame.draw.circle(self.screen, self.get_color(number), (j * x_csl + x_csl / 2, i * y_scl + y_scl / 2),
                                   40)

    @staticmethod
    def get_color(number):
        if number == 1:
            return YELLOW_COLOR
        if number == -1:
            return RED_COLOR
        return EMPTY_COLOR

    def get_state(self):
        return self._board

    def set_board(self, board):
        self._board = board

    def game_finish(self):
        for i in range(6):
            for j in range(7):
                if self._board[i][j] != 0:
                    if self.check_win((i, j)) is not None:
                        return True
        return False


if __name__ == '__main__':
    game = Connect4()
    game.play()
