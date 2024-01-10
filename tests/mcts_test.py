import sys
import unittest

sys.path.append('../src')
from main import Connect4
from MCTS import MonteCarlo


class MyTestCase(unittest.TestCase):

    def test_game_finish(self):
        game = Connect4()
        game.set_board(BOARD1)
        monte_carlo = MonteCarlo(game,10_000)
        ans = monte_carlo.monte_carlo_tree_search()
        print(ans)




BOARD1 = [[0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0]]



if __name__ == '__main__':
    unittest.main()