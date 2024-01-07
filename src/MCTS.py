from copy import deepcopy


class Node:
    def __init__(self, state, parent=None, column_play=None):
        self.parent = parent
        self.state = state
        self.children = []
        self.score = 0
        self.visit = 0
        self.fully_explored = False
        self.column = column_play

    def add_parent(self, node):
        self.parent = node

    def add_children(self, node):
        self.children.append(node)

    def update_node(self, reward):
        self.score += reward
        self.visit += 1


class MonteCarlo:

    def __init__(self, game, iteration, initial_turn):
        self.root = Node(game)
        self.iteration = iteration
        self.initial_turn = initial_turn

    def monte_carlo_tree_search(self):
        for i in range(self.iteration):
            node, turn = self.selection(self.root, 1)
            reward = self.simulation(node.state, turn)
            self.backpropagation(node, reward, turn)

    def selection(self, node, turn):
        while not node.state.game_finish():
            if not node.fully_explored:
                return self.expansion(node), -1 * turn
            else:
                node = self.get_best_child(node)
                turn *= -1
        return node, turn

    def simulation(self, state, turn):
        return 1

    def expansion(self, state_init):
        pass

    def backpropagation(self, node, reward, turn):
        pass

    def get_best_child(self, node):
        pass

    def copy_state(self, state):
        return deepcopy(state)
