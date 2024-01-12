import random
import math


class Node:
    def __init__(self, state, parent=None, column_play=None):
        self.parent = parent
        self.state = state
        self.children = []
        self.children_moves = []
        self.reward = 0
        self.visits = 0
        self.column = column_play
        self.last_move = None

    def add_parent(self, node):
        self.parent = node

    def add_child(self, child_state, move):
        child = Node(child_state, parent=self)
        self.children.append(child)
        self.children_moves.append(move)

    def update_node(self, reward):
        self.reward += reward
        self.visits += 1

    def fully_explored(self):
        if len(self.children) == len(self.state.get_free_columns()):
            return True
        return False

    def __str__(self):
        return f"Noeud({self.reward},{self.visits})"

    def __repr__(self):
        return f"Noeud({self.reward},{self.visits})"


class MonteCarlo:

    def __init__(self, game, iteration):
        self.root = Node(game)  # definit le noeud de depart avec l'etat initial du jeu
        self.iteration = iteration  # le nombre d'iterations de recherches

    def monte_carlo_tree_search(self):

        # return random.choice(self.root.state.get_free_columns())
        # pour le nombre d'iterations
        for i in range(self.iteration):
            node, turn = self.selection(self.root, 1)  # on selectionne un noeud
            reward = self.simulation(node, turn)  # puis on determine son score en le simulant
            self.backpropagation(node, reward, turn)  # on retropropage le resultat sur tous les parents

        ans = self.get_best_child(self.root)
        return ans.state.last_move[1]

    def selection(self, node, turn):
        while not node.state.game_finish():
            if not node.fully_explored():
                return self.expansion(node, turn), -1 * turn
            else:
                node = self.get_best_child(node)
                turn *= -1
        return node, turn

    def simulation(self, node, turn):
        state = node.state.copy_state()
        while not state.game_finish():
            free_cols = state.get_free_columns()
            col = random.choice(free_cols)
            state.make_move(col, turn)
            turn *= -1

        result = state.check_win(state.last_move)
        reward_bool = result == 1 or result == -1
        if reward_bool and turn == -1:
            reward = 1
        elif reward_bool and turn == 1:
            reward = -1
        else:
            reward = 0
        return reward

    def expansion(self, node, turn):
        new_state = None
        free_columns = node.state.get_free_columns()
        for col in free_columns:
            if col not in node.children_moves:
                new_state = node.state.copy_state()
                new_state.make_move(col, turn)
                break
        node.add_child(new_state, col)
        return node.children[-1]

    def backpropagation(self, node, reward, turn):
        while node != None:
            node.visits += 1
            node.reward -= turn * reward
            # node.reward += reward
            node = node.parent
            turn *= -1
        return

    def get_best_child(self, node):
        best_score = -float("inf")
        best_children = []
        for c in node.children:
            exploitation = c.reward / c.visits
            exploration = math.sqrt(math.log2(node.visits) / c.visits)
            score = exploitation + 2.0 * exploration  # 2.0 exploration parameter
            if score == best_score:
                best_children.append(c)
            elif score > best_score:
                best_children = [c]
                best_score = score
        res = random.choice(best_children)
        return res
