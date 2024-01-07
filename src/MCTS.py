import random


class Node:
    def __init__(self, state, parent=None, column_play=None):
        self.parent = parent
        self.state = state
        self.children = []
        self.children_moves = []
        self.score = 0
        self.visit = 0
        self.fully_explored = False
        self.column = column_play
        self.last_move = None

    def add_parent(self, node):
        self.parent = node

    def add_child(self, child_state, move):
        child = Node(child_state, parent=self)
        self.children.append(child)
        self.children_moves.append(move)

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

    def simulation(self, state_init, turn):
        state = state_init.copy_state()
        while not state.last_move or not state.check_win(state.last_move):
            free_cols = state.get_free_columns()
            col = random.choice(free_cols)
            state.make_move(col)
            turn *= -1

        result = state.check_win(state.last_move)
        reward_bool = result==1 or result==-1
        if reward_bool and turn == -1:
            reward = 1
        elif reward_bool and turn == 1:
            reward = -1
        else:
            reward = 0
        return reward

    def expansion(self,node):
        free_columns = node.state.get_free_columns()
        for col in free_columns:
            if col not in node.children_moves:
                new_state = node.state.copy_state()
                new_state.make_move(col)
                break
        node.add_child(new_state,col)
        return node.children[-1]

    def backpropagation(self, node, reward, turn):
        pass

    def get_best_child(self, node):
        pass


