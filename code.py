import sys
from code2 import RandomAgent, HumanAgent, ComputerAgent, ComputerPruneAgent
import test


class GameState:
    """Class representing a single sate of a Connect4-esque game.

    For details on the game, see: https://en.wikipedia.org/wiki/Connect_Four

    Once created, a game state object should usually not be modified; instead, use the successors()
    function to generate reachable states.

    The board is stored as a 2D list, containing 1's representing Player 1's pieces and -1's
    for Player 2 (unused spaces are 0).
    """

    def __init__(self, nrows=6, ncols=7, nwin=4):
        """Constructor for Connect4 state.

        Args:
            nrows: number of rows in the board
            ncols: number of columns in the board
            nwin: the number of tokens each player must get in a row to win
        """
        self.num_rows = nrows
        self.num_cols = ncols
        self.num_win = nwin
        self.board = [[0 for x in range(ncols)] for y in range(nrows)]

    def copy(self):
        """Create a duplicate of this game state."""
        clone = GameState(self.num_rows, self.num_cols, self.num_win)
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                clone.board[r][c] = self.board[r][c]
        return clone

    def next_player(self):
        """Determines who's move it is based on the board state.

        Returns: 1 if Player 1 goes next, -1 if it's Player 2's turn
        """
        return 1 if sum(sum(self.board, [])) == 0 else -1  # 1 for Player 1, -1 for Player 2

    def create_successor(self, col):
        """Create the successor state that follows from a given move."""
        player = self.next_player()
        successor = self.copy()
        row = 0
        while (successor.board[row][col] != 0) and (row < successor.num_rows - 1):
            row += 1
        successor.board[row][col] = player
        return successor

    def successors(self):
        """Generates successor state objects for all valid moves from this board.

        Returns: a _sorted_ list of (move, state) tuples
        """
        move_states = []
        for col in range(self.num_cols):
            if self.board[self.num_rows - 1][col] == 0:
                move_states.append((col, self.create_successor(col)))
        return move_states

    def winner(self):
        """Determines if either player has won the game by getting num_win tokens in a row.

        Returns: 1 if Player 1 wins
                -1 if Player 2 wins
                 0 if the board is full (indicating a tie)
                 None otherwise
        """

        # check horizontals
        for r in range(self.num_rows):
            for c in range(self.num_cols - self.num_win + 1):
                # print("r {}, c {}".format(r, c))
                # print(list(range(c, c+self.num_win)))
                val_sum = sum([self.board[r][x] for x in range(c, c + self.num_win)])
                if abs(val_sum) == self.num_win:
                    return 1 if val_sum > 0 else -1

        # check verticals
        for c in range(self.num_cols):
            for r in range(self.num_rows - self.num_win + 1):
                val_sum = sum([self.board[y][c] for y in range(r, r + self.num_win)])
                if abs(val_sum) == self.num_win:
                    return 1 if val_sum > 0 else -1

        # check diags

        # original code:
        # for r in range(self.num_rows):
        #     for c in range(self.num_cols):
        #         if (r < self.num_rows-self.num_win+1) and (c < self.num_cols-self.num_win+1):
        #             val_sum = sum([ self.board[r+d][c+d] for d in range(self.num_win) ])
        #             if abs(val_sum) == self.num_win:
        #                 return 1 if val_sum > 0 else -1
        #
        #         if (r > self.num_win-1) and (c > self.num_win-1):
        #             val_sum = sum([ self.board[r-d][c-d] for d in range(self.num_win) ])
        #             if abs(val_sum) == self.num_win:
        #                 return 1 if val_sum > 0 else -1

        # hard-coded to 4-in-a-row
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if self.board[r][c] == 0:
                    continue
                count = 0
                # Checks positive slope diagonals
                if r + 3 < self.num_rows and c + 3 < self.num_cols:
                    for i in range(1, 4):
                        if self.board[r + i][c + i] == self.board[r][c]:
                            count += 1
                if count >= 3:
                    return self.board[r][c]
                count = 0
                # Checks negative slope diagonals
                if r + 3 < self.num_rows and c >= 3:
                    for i in range(1, 4):
                        if self.board[r + i][c - i] == self.board[r][c]:
                            count += 1
                if count >= 3:
                    return self.board[r][c]

        # check for open spaces
        if self.is_full():
            return 0
        else:
            return None

    def is_full(self):
        """Checks to see if there are available moves left."""
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if self.board[r][c] == 0:
                    return False
        return True

    def __str__(self):
        symbols = {-1: "O", 1: "X", 0: "-"}
        s = ""
        for r in range(self.num_rows - 1, -1, -1):
            s += "\n"
            for c in range(self.num_cols):
                s += "  " + symbols[self.board[r][c]]

        s += "\n  " + "." * (self.num_cols * 3 - 2) + "\n"
        for c in range(self.num_cols):
            s += "  " + str(c)
        s += "\n"
        return s


def play_game(player1, player2, depth=None, state=None):
    """Run a Connect4 game.

    Player objects can be of any class that defines a get_move(state, depth) method that returns
    a move, state tuple.
    """
    if state is None:
        state = GameState()
    print(state)

    turn = 0
    while state.winner() is None:
        player_next = player1 if state.next_player() == 1 else player2
        move, state = player_next.get_move(state, depth)
        print("Turn {}: Player {} moves {}".format(turn, 1 if state.next_player() == -1 else 2, move))
        print(state)

        win = state.winner()
        if win == 0:
            print("It's a tie.")
        elif win == 1:
            print("Player 1 wins!")
        elif win == -1:
            print("Player 2 wins!")
        turn += 1

    #############################################


if __name__ == "__main__":
    agent_codes = {'r': RandomAgent,
                   'h': HumanAgent,
                   'c': ComputerAgent,
                   'p': ComputerPruneAgent}
    play1 = agent_codes[sys.argv[1]]()
    play2 = agent_codes[sys.argv[2]]()
    depth_lim = None if len(sys.argv) < 4 else int(sys.argv[3])  # optional argument
    start_state = None # change this to test.board1 to use a test state instead of a blank board

    play_game(play1, play2, depth_lim, start_state)