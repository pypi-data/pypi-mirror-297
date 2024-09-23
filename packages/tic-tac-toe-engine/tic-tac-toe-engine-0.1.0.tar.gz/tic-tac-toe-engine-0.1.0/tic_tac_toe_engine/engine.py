from random import choice
from typing import Union

from .exceptions import InvalidMovementError, InvalidPositionError
from .position import Position



WINNING_CASES = [
	[0, 1, 2], [3, 4, 5], [6, 7, 8], # Horizontal
	[0, 3, 6], [1, 4, 7], [2, 5, 8], # Vertical
	[0, 4, 8], [2, 4, 6] # Diagonal
]


class Engine(object):
	""" Implementation of the rules of Tic Tac Toe """
		
	def __init__(self) -> None:

		self._players = ["X", "O"]
		self.restart() # Initialize the board

	@property
	def board(self):
		""" Return a copy of the current board state """

		# @property to prevent direct assignation to self._board
		return self._board.copy()


	def restart(self) -> None:
		""" Restart the game state """

		self.current_player = choice(self._players)
		self._board = [None, None, None, None, None, None, None, None, None]

		self.winner = None
		self.loser = None


	def play_move(self, position: Union[int, tuple[int, int]]) -> None:
		"""  Play a move on the board (Assume self.current_player is making the move).
		
		Args:
			position: The position of the target square. This method accepts two types of positions:
				- Index based: The index of the target square (0 - 8).
				- Coordinate based: The coordinates of the target square. The middle square is considered to be (0, 0).
		Raises: 
			InvalidMovementError: if the target square was already occupied.
			InvalidPosition: if the position is not valid.
		"""

		# Convert to index based position if needed
		if type(position) is tuple:
			position = Position.to_index(position)

		# Out of the board
		if (not Position.is_valid(position)):
			raise InvalidPositionError("The square is out of the board (3x3).")
		
		# Alredy occupied
		if (self._board[position] is not None):
			raise InvalidMovementError("The square is alredy occupied.")

		self._board[position] = self.current_player
		self.current_player = "X" if self.current_player == "O" else "O"
	

	def available_moves(self, index_based_position=True) -> list[int | tuple[int, int]]:
		""" Return the available moves on the board 
		
		Args:
			index_based_position: If True, return moves as indices (0-8).
								  If False, return moves as coordinates (x, y),
								  where the middle square is considered to be (0, 0).

		Returns:
			A list with the available moves, either as indices or coordinates,
			depending on the value of index_based_position.
		"""

		available_moves = []

		for i, square in enumerate(self._board):
			if square is None: # Empty square
				available_moves.append(i)
			
		if not index_based_position:
			available_moves = [Position.to_coordinates(position) for position in available_moves]

		return available_moves


	def _check_win(self) -> bool:
		""" Check if any player has won. Set the winner and loser attributes accordingly """

		for player in self._players:
			for case in WINNING_CASES:
				if all(self._board[index] == player for index in case):
					self.winner = player
					self.loser = self._players[0] if player == self._players[1] else self._players[1]

					return True

		return False


	def is_over(self) -> bool:
		""" Check if the game is over, either by a win or because there are no available moves """

		return self._check_win() or len(self.available_moves()) == 0

	def is_tie(self) -> bool:
		""" Check if the game ended in a tie """

		return (not self._check_win()) and len(self.available_moves()) == 0