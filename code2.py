import random
import math


class RandomAgent:
    """Agent that picks a random available move.  You should be able to beat it."""

    def get_move(self, state, depth=None):
        possibles = [m for m, v in state.successors()]
        return random.choice(possibles)


class HumanAgent:
    """Prompts user to supply a valid move."""

    def get_move(self, state, depth=None):
        move__state = dict(state.successors())
        prompt = "Kindly enter your move {}: ".format(sorted(move__state.keys()))
        move = int(input(prompt))
        return move, move__state[move]


class ComputerAgent:
    """Artificially intelligent agent that uses minimax to select the best move."""

    def get_move(self, state, depth=None):
        """Select the best available move, based on minimax value."""
        nextp = state.next_player()
        best_util = -math.inf if nextp == 1 else math.inf
        best_move = None
        best_state = None

        for move, state in state.successors():
            util = self.minimax(state, depth)
            if ((nextp == 1) and (util > best_util)) or ((nextp == -1) and (util < best_util)):
                best_util, best_move, best_state = util, move, state
        return best_move, best_state

    def minimax(self, state, depth):
        """Determine the minimax utility value the given state.

        Args:
            state: a connect4.GameState object representing the current board
            depth: the maximum depth of the game tree that minimax should traverse before
                estimating the utility using the evaluation() function.  If depth is 0, no
                traversal is performed, and minimax returns the results of a call to evaluation().
                If depth is None, the entire game tree is traversed.

        Returns: the minimax utility value of the state
        """
        #
        # Fill this in!
        #

        # score = state.winner()
        # result = []
        # if score is not None:
        #     return score, []
        #
        # if depth == 0:
        #     if state.winner() is not None:
        #         return state.winner(), result
        #     else:
        #         return 0, result
        if depth == 0 or state.winner() is not None:
            return self.evaluation(state)
        else:
            if depth is not None:
                if state.next_player() == 1:
                    max_value = -math.inf
                    for move, board in state.successors():
                        value = self.minimax(board, depth - 1)
                        max_value = max(max_value, value)
                    return max_value
                else:
                    min_value = math.inf
                    for move, board in state.successors():
                        value = self.minimax(board, depth - 1)
                        min_value = min(min_value, value)
                    return min_value
            else:
                if state.next_player() == 1:
                    max_value = -math.inf
                    for move, board in state.successors():
                        max_value = max(max_value, self.minimax(board, depth))
                    return max_value
                else:
                    min_value = math.inf
                    for move, board in state.successors():
                        min_value = min(min_value, self.minimax(board, depth))
                    return min_value

    def evaluation(self, state):
        """Estimate the utility value of the game state based on features.

        N.B.: This method must run in O(1) time!

        Args:
            state: a connect4.GameState object representing the current board

        Returns: a heusristic estimate of the utility value of the state
        """
        #
        # Fill this in!
        #

        if state.winner() is not None:
            if state.winner() == 1:
                possible = state.num_rows * state.num_cols + 20
                for r in range(state.num_rows):
                    for c in range(state.num_cols):
                        if state.board[r][c] != 0:
                            possible = possible - 1

                return possible
            return state.winner()
        else:
            add = False
            number = 0
            for r in range(state.num_rows):
                count = 0
                for c in range(state.num_cols):
                    # print("r {}, c {}".format(r, c))
                    # print(list(range(c, c+self.num_win)))
                    if state.board[r][c] == 1:
                        count += 1
                        if count > number:
                            number = count
                        if c + 1 < state.num_cols and state.board[r][c + 1] == -1 or c + 1 >= state.num_cols:
                            if number > 0:
                                number = number - 1
                        elif c - 1 >= 0 and state.board[r][c - 1] == -1 or c - 1 < 0:
                            if number > 0:
                                number = number - 1
                    else:
                        count = 0
                        continue

            for c in range(state.num_cols):
                count = 0
                for r in range(state.num_rows):

                    if state.board[r][c] == 1:
                        count += 1

                        if count > number:
                            number = count
                        if r + 1 < state.num_rows and state.board[r + 1][c] == -1 or r + 1 >= state.num_rows:
                            if number > 0:
                                number = number - 1
                        elif r - 1 >= 0 and state.board[r - 1][c] == -1 or r - 1 < 0:
                            if number > 0:
                                number = number - 1
                    else:
                        count = 0
                        continue
            count = 0
            for r in range(state.num_rows):
                for c in range(state.num_cols):
                    if state.board[r][c] != 1:
                        count = 0
                        continue

                    # Checks positive slope diagonals
                    if state.board[r][c] == 1:
                        count += 1
                        if r + 3 < state.num_rows and c + 3 < state.num_cols:
                            for i in range(1, 4):
                                if state.board[r + i][c + i] == state.board[r][c]:
                                    count += 1
                                    col = c + i
                                    row = r + i
                                    if col + 1 < state.num_cols and row + 1 < state.num_rows and state.board[row + 1][
                                        col + 1] == -1 or (row + 1 >= state.num_rows and col + 1 >= state.num_cols):
                                        if count > 0:
                                            count -= 1
                                    elif col - 1 >= 0 and row - 1 >= 0 and state.board[row - 1][col - 1] == -1 or (
                                            row - 1 < 0 and col - 1 < 0):
                                        if count > 0:
                                            count -= 1
                        if number < count:
                            number = count

                        # Checks negative slope diagonals
                        count = 1
                        if r + 3 < state.num_rows and c >= 3:
                            for i in range(1, 4):
                                if state.board[r + i][c - i] == state.board[r][c]:
                                    count += 1
                                    row = r + i
                                    col = c - i

                                    if col - 1 >= 0 and row + 1 < state.num_rows and state.board[r + 1][c - 1] == -1 or (col-1<0 and row+1>= state.num_rows):
                                        if count > 0:
                                            count -= 1
                                    elif col + 1 < state.num_cols and row - 1 >= 0 and state.board[row - 1][
                                        col + 1] == -1 or (col+1>=state.num_cols and row-1<0):
                                        if count > 0:
                                            count -= 1

                        if number < count:
                            number = count

            return number


class ComputerPruneAgent(ComputerAgent):
    """Smarter computer agent that uses minimax with alpha-beta pruning to select the best move."""

    def minimax(self, state, depth):
        util, pruned = self.minimax_prune(state, depth)
        print(pruned)
        return util

    def minimax_prune(self, state, depth):
        """Determine the minimax utility value the given state using alpha-beta pruning.

        N.B.: When exploring the game tree and expanding nodes, you must consider the child nodes
        in the order that they are returned by GameState.successors().  That is, you cannot prune
        the state reached by moving to column 4 before you've explored the state reached by a move
        to to column 1.

        Args: see ComputerAgent.minimax() above


        Returns: the minimax utility value of the state, along with a list of state objects that
            were not expanded due to pruning.
        """
        #
        # Fill this in!
        #

        score = state.winner()
        result = []
        if score is not None:
            return score, result

        if depth == 0:
            if state.winner() is not None:
                return state.winner(), result
            else:
                return 0, result

        elif depth is not None:
            if state.next_player() == 1:
                max_value = -math.inf
                for move, board in state.successors():
                    util, pruned = self.minimax_prune(board, depth - 1)
                    if util < max_value:
                        if pruned is not None:
                            for index in pruned:
                                result.append(index)
                        result.append(board)
                        return max_value, result

                    max_value = max(max_value, util)

                return max_value, result
            else:
                min_value = math.inf
                for move, board in state.successors():
                    util, pruned = self.minimax_prune(board, depth - 1)
                    if util > min_value:
                        if pruned is not None:
                            for index in pruned:
                                result.append(index)
                        result.append(board)
                        return min_value, result
                    min_value = min(min_value, util)

                return min_value, result
        else:
            if state.next_player() == 1:
                max_value = -math.inf
                for move, board in state.successors():
                    util, pruned = self.minimax_prune(board, depth)
                    if util < max_value:
                        if pruned is not None:
                            for index in pruned:
                                result.append(index)
                        result.append(board)
                        return max_value, result
                    max_value = max(max_value, util)

                return max_value, result
            else:
                min_value = math.inf
                for move, board in state.successors():
                    util, pruned = self.minimax_prune(board, depth)
                    if util > min_value:
                        if pruned is not None:
                            for index in pruned:
                                result.append(index)
                        result.append(board)
                        return min_value, result
                    min_value = min(min_value, util)
                return min_value, result