from typing import Union




class Position(object):
	""" A static class that exposes useful position methods """

	@staticmethod
	def to_index(coordinate: tuple[int, int]) -> int:
		""" Convert an coordinate-based position to an index-based one """
	
		return (4 + coordinate[0]) + (3 * coordinate[1] * -1)

	@staticmethod
	def to_coordinates(position: int) -> tuple[int, int]:
		""" Convert an index-based position to an coordinate-based one """

		x = ((position % 3) - 1)
		y = (position // 3 - 1) * -1

		return (x, y)

	@staticmethod
	def is_valid(position: Union[int, tuple[int, int]]) -> bool:
		""" Check wether or not the given position is within the boundaries of the 3x3 grid """

		# Convert to index-based for an easier check
		if type(position) is tuple:
			position = Position.to_index(position)

		return position > -1 and position < 9