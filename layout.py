import tkinter as tk
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple, Literal, Any

from base_classes import BaseWidget
from base_types import TkWidget, Anchor, Side, Fill
from compound_widgets import CompoundWidget
from style import WidgetStyle
from widgets import Widget


# layout options classes
@dataclass
class AbsoluteLayoutOptions:
	pos: Tuple[int, int]
	size: Tuple[int | None, int | None]


@dataclass
class GridLayoutOptions:
	row: int
	column: int
	row_span: int = 1
	column_span: int = 1
	sticky: str = None


@dataclass
class FlexLayoutOptions:
	flex: float = 0  # TODO: implement 😓


# layouts
class Layout(ABC):
	properties_class = None

	@abstractmethod
	def render_children(self, cont: TkWidget, children: List[Tuple[Widget | CompoundWidget, Any]]):
		# TODO: margin/padding
		pass


class AbsoluteLayout(Layout):
	properties_class = AbsoluteLayoutOptions

	def render_children(self, tk_container: TkWidget, children: List[Tuple[Widget | CompoundWidget, AbsoluteLayoutOptions]]):
		for child, ppts in children:
			child.render(tk_container).place(
				x=ppts.pos[0], y=ppts.pos[1],
				width=ppts.size[0], height=ppts.size[1]
			)


class GridLayout(Layout):
	properties_class = GridLayoutOptions

	def __init__(self, rows: int, columns: int):
		# TODO: row/column properties

		self.rows = rows
		self.columns = columns

	def render_children(self, tk_container: TkWidget, children: List[Tuple[Widget | CompoundWidget, GridLayoutOptions]]):
		tk_container.grid_rowconfigure(list(range(self.rows)), weight=1, uniform='a')
		tk_container.grid_columnconfigure(list(range(self.columns)), weight=1, uniform='b')

		for child, ppts in children:
			child.render(tk_container).grid(row=ppts.row, column=ppts.column, row_span=ppts.row_span, column_span=ppts.column_span, sticky=ppts.sticky)


class FlexLayout(Layout):
	properties_class = FlexLayoutOptions

	def __init__(
		self,
		direction: Literal['vertical', 'horizontal'] = 'horizontal',
		justification: Literal['start', 'center', 'end', 'space-evenly', 'space-between', 'space-around'] = 'center',
		alignment: Literal['start', 'center', 'end'] = 'center',
	):
		self.direction = direction
		self.justification = justification
		self.alignment = alignment

	def render_children(self, tk_container: TkWidget, children: List[Tuple[Widget | CompoundWidget, FlexLayoutOptions]]):
		if self.direction == 'horizontal':
			if self.alignment == 'start':
				anchor = Anchor.North
			elif self.alignment == 'center':
				anchor = Anchor.No
			elif self.alignment == 'end':
				anchor = Anchor.South
			else:
				raise Exception('Fuck off.')

			if self.justification == 'start':
				for child, _ in children:
					child.render(tk_container).pack(side=Side.Left.value, anchor=anchor.value)

			elif self.justification == 'center':
				tk.Frame(tk_container, bg=tk_container['bg']).pack(side=Side.Left.value, expand=True, fill=Fill.Both.value, anchor=anchor.value)

				for child, _ in children:
					child.render(tk_container).pack(side=Side.Left.value, anchor=anchor.value)

				tk.Frame(tk_container, bg=tk_container['bg']).pack(side=Side.Left.value, expand=True, fill=Fill.Both.value, anchor=anchor.value)

			elif self.justification == 'end':
				for child, _ in children:
					child.render(tk_container).pack(side=Side.Right.value, anchor=anchor.value)

			elif self.justification == 'space-around':
				for child, _ in children:
					child.render(tk_container).pack(side=Side.Left.value, expand=True, anchor=anchor.value)

			elif self.justification == 'space-between':
				for i, (child, _) in enumerate(children):
					child.render(tk_container).pack(side=Side.Left.value, anchor=anchor.value)

					if not i == len(children) - 1:
						tk.Frame(tk_container).pack(side=Side.Left.value, expand=True, fill=Fill.Both.value, anchor=anchor.value)

			elif self.justification == 'space-evenly':
				tk.Frame(tk_container).pack(side=Side.Left.value, expand=True, fill=Fill.Both.value, anchor=anchor.value)

				for child, _ in children:
					child.render(tk_container).pack(side=Side.Left.value, anchor=anchor.value)

					tk.Frame(tk_container).pack(side=Side.Left.value, expand=True, fill=Fill.Both.value, anchor=anchor.value)

			else:
				raise Exception('Fuck off.')

		if self.direction == 'vertical':
			if self.alignment == 'start':
				anchor = Anchor.West
			elif self.alignment == 'center':
				anchor = Anchor.No
			elif self.alignment == 'end':
				anchor = Anchor.East
			else:
				raise Exception('Fuck off.')

			if self.justification == 'start':
				for child, _ in children:
					child.render(tk_container).pack(side=Side.Top.value, anchor=anchor.value)

			elif self.justification == 'center':
				tk.Frame(tk_container).pack(side=Side.Top.value, expand=True, fill=Fill.Both.value, anchor=anchor.value)

				for child, _ in children:
					child.render(tk_container).pack(side=Side.Top.value, anchor=anchor.value)

				tk.Frame(tk_container).pack(side=Side.Top.value, expand=True, fill=Fill.Both.value, anchor=anchor.value)

			elif self.justification == 'end':
				for child, _ in children:
					child.render(tk_container).pack(side=Side.Bottom.value, anchor=anchor.value)

			elif self.justification == 'space-around':
				for child, _ in children:
					child.render(tk_container).pack(side=Side.Top.value, expand=True, anchor=anchor.value)

			elif self.justification == 'space-between':
				for i, (child, _) in enumerate(children):
					child.render(tk_container).pack(side=Side.Top.value, anchor=anchor.value)

					if not i == len(children) - 1:
						tk.Frame(tk_container).pack(side=Side.Top.value, expand=True, fill=Fill.Both.value, anchor=anchor.value)

			elif self.justification == 'space-evenly':
				tk.Frame(tk_container).pack(side=Side.Top.value, expand=True, fill=Fill.Both.value, anchor=anchor.value)

				for child, _ in children:
					child.render(tk_container).pack(side=Side.Top.value, anchor=anchor.value)

					tk.Frame(tk_container).pack(side=Side.Top.value, expand=True, fill=Fill.Both.value, anchor=anchor.value)

			else:
				raise Exception('Fuck off.')


# containers
class Container(CompoundWidget):
	@property
	def style(self) -> WidgetStyle:
		return WidgetStyle()

	@property
	def count(self) -> int:
		return len(self._children)

	def __init__(self, parent: BaseWidget, layout: Layout):
		super().__init__(parent)

		self._layout = layout
		self._children: List[Tuple[Widget | CompoundWidget, layout.properties_class]] = []

	def add_widget(self, widget: Widget | CompoundWidget, layout_ppts):
		assert isinstance(layout_ppts, self._layout.properties_class)

		self._children.append((widget, layout_ppts))

	def render(self, tk_parent: TkWidget) -> TkWidget:
		_frame = tk.Frame(tk_parent)

		self._layout.render_children(_frame, self._children)

		return _frame
