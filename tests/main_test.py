import sys
import unittest

sys.path.append('../src')
from main import Connect4


class MyTestCase(unittest.TestCase):

    def test_game_finish(self):
        game = Connect4()

        game.set_board(BOARD1)
        self.assertEqual(game.game_finish(), False, "Erreur : BOARD1 devrait retourner False")

        game.set_board(BOARD2)
        self.assertEqual(game.game_finish(), True, "Erreur : BOARD2 devrait retourner True")

        game.set_board(BOARD3)
        self.assertEqual(game.game_finish(), False, "Erreur : BOARD3 devrait retourner False")

        game.set_board(BOARD4)
        self.assertEqual(game.game_finish(), True, "Erreur : BOARD4 devrait retourner True")



BOARD1 = [[0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0]]

BOARD2 = [[1, 0, 0, 0, 0, 0, 0],
          [0, 1, 0, 0, 0, 0, 0],
          [0, 0, 1, 0, 0, 0, 0],
          [0, 0, 0, 1, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0]]

BOARD3 = [[1, 0, 0, 0, 0, 0, 0],
          [1, 1, 1, 0, 0, 0, 0],
          [0, 1, 1, 0, 0, 0, 0],
          [0, 1, 0, -1, 0, 0, 0],
          [0, 0, 0, 0, 0, -1, 0],
          [0, 0, 0, 0, 0, 0, -1]]

BOARD4 = [[1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1]]

if __name__ == '__main__':
    unittest.main()
