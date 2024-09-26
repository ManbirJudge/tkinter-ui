from abc import ABC
from dataclasses import dataclass
from typing import Optional, Tuple
from uuid import uuid4

from base_types import Side, Fill, Anchor
from style import Theme


# base widget
class BaseWidget(ABC):
	# properties
	@property
	def id(self) -> str:
		return self._id

	@property
	def parent(self) -> 'BaseWidget':  # or None
		return self._parent

	@property
	def theme(self) -> Theme:
		if self.parent is None:
			raise NotImplementedError('Root widgets must implement their own \'theme\' property.')

		return self.parent.theme

	# constructor
	def __init__(self, parent: Optional['BaseWidget']):
		print('Initializing BaseWidget.')

		self._id = str(uuid4())
		self._parent = parent  # can be None


# base layout classes
@dataclass
class PackProperties:
	side: Side = Side.Top
	expand: bool = False
	fill: Fill = Fill.No
	anchor: Anchor = Anchor.No


@dataclass
class PlaceProperties:
	pos: Tuple[int, int]
	size: Tuple[int, int]
