from uuid import uuid4

from style import Theme


class Object:
	# ---
	@property
	def id(self) -> str:
		return self._id

	@property
	def parent(self) -> 'Object':  # or None
		return self._parent

	@property
	def theme(self) -> Theme:
		if self.parent is None:
			raise NotImplementedError('Root objects must implement their own \'theme\' property.')

		return self.parent.theme

	# ---
	def __init__(self, parent: 'Object' = None):
		self._id = str(uuid4())
		self._parent = parent
