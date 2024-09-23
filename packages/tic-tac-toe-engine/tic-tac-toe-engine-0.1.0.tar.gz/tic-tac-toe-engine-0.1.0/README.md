
# Tic Tac Toe Engine


Implementation of the rules of the game "Tic tac toe".

This project can be use as:
- An engine for a game (Both CLI and paired with a game library like Pygame).
- A tool for AI training.

This project implements all the logic needed to play the tic tac toe game.

Example usage (a CLI implementation):

```python
from tic_tac_toe_engine import Engine
from typing import Union



def print_board(board: list[Union[str, None]]) -> None:
	""" Print the board """	

	print("") # Some space

	for i in range(0, 9, 3):
		row = " | ".join(board[j] if board[j] is not None else str(j) for j in range(i, i + 3))
		print(row)
		if i < 6:  # Add a line between rows, but not after the last row
			print("-" * 9)


engine = Engine()

while True:
	print_board(engine.board)
	print(f"\n{engine.current_player} moves.")
	move = int(input("Enter your move (0 - 8): "))

	engine.play_move(move)

	if engine.is_over():
		print_board(engine.board) # Print again to reflect the ending
		
		if engine.is_tie():
			print("It's a tie")

		else:
			print(f"{engine.winner} wins!")

		break
```