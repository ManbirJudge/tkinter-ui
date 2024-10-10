from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, Dict, Type, Any, TypedDict, List

from base_types import Side, Fill, Anchor, TkWidget, BaseWidgetName
from object import Object
from style import BaseWidgetStyle


# ---
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


# ---
class BaseWidgetProperty(TypedDict):
	name: str
	type: Type
	default: Any


class BaseWidget(Object, ABC):
	name: BaseWidgetName
	properties: Dict[str, BaseWidgetProperty]

	# ---
	@property
	def style(self) -> BaseWidgetStyle:
		return self._style

	@property
	def rendered(self) -> bool:
		return self._rendered

	# constructor
	def __init__(self, parent: Object = None, style: BaseWidgetStyle = None):
		super().__init__(parent)

		self._style = style if style is not None else self.theme.get(self.name)
		self._rendered = False
		self._visible = False
		self._tk_widget = None

	# Tk compatibility
	@abstractmethod
	def create_tk_widget(self, tk_parent: TkWidget):
		"""Creates self._tk_widget for rendering."""
		pass

	def post_create(self):
		pass

	@abstractmethod
	def config_tk_widget(self, which_ones: List[str] = None):
		"""Configures self._tk_widget."""

		if self._tk_widget is None:
			return

	@abstractmethod
	def style_tk_widget(self):
		"""Styles self._tk_widget."""

		if self._tk_widget is None:
			return

	def render(self, tk_parent: TkWidget) -> TkWidget:
		if self._rendered:
			raise Exception('Widget is already rendered!')

		self.create_tk_widget(tk_parent)

		self.post_create()

		self.config_tk_widget()
		self.style_tk_widget()

		self._rendered = True

		self.show()

		return self._tk_widget

	# visibility
	def hide(self):
		self._visible = False

	def show(self):
		self._visible = True

	@property
	def visible(self) -> bool:
		return self._visible

	@visible.setter
	def visible(self, visible: bool):
		if visible:
			self.show()
		else:
			self.hide()
