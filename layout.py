import tkinter as tk
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple, Literal

from style import SupportedStyles, WidgetStyle
from type_classes import Side, Fill, Parent, Anchor
from widgets import Widget, HasText
from window import Window


# spacer widget
class Spacer(Widget):
	@property
	def supported_styles(self) -> SupportedStyles:
		return SupportedStyles(True, False, False, False, False, False, False, False, False, False)

	def on_init(self, parent: Parent, **kwargs):
		self._style = WidgetStyle()
		self._tk_widget = tk.Frame(master=parent if isinstance(parent, Window) else parent.tk_widget)


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
	flex: float = 0


# layouts
class Layout(ABC):
	properties_class = None

	@abstractmethod
	def lay_out_children(self, cont: Widget, children: List[Widget], children_layout_ppts: list):
		pass


class AbsoluteLayout(Layout):
	properties_class = AbsoluteLayoutOptions

	def lay_out_children(self, cont: Widget, children: List[Widget], children_layout_ppts: List[AbsoluteLayoutOptions]):
		for child, ppts in zip(children, children_layout_ppts):
			child.place(ppts.pos, ppts.size)


class GridLayout(Layout):
	properties_class = GridLayoutOptions

	def __init__(self, rows: int, columns: int):
		# TODO: row/column properties

		self.rows = rows
		self.columns = columns

	def lay_out_children(self, cont: Widget, children: List[Widget], children_layout_ppts: List[GridLayoutOptions]):
		cont.tk_widget.grid_rowconfigure(list(range(self.rows)), weight=1, uniform='a')
		cont.tk_widget.grid_columnconfigure(list(range(self.columns)), weight=1, uniform='b')

		for child, ppts in zip(children, children_layout_ppts):
			child.grid(row=ppts.row, column=ppts.column, row_span=ppts.row_span, column_span=ppts.column_span, sticky=ppts.sticky)


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

	def lay_out_children(
			self,
			cont: Widget,
			children: List[Widget],
			children_layout_ppts: List[FlexLayoutOptions]
	):
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
				for child in children:
					child.pack(Side.Left, anchor=anchor)

			elif self.justification == 'center':
				Spacer(cont).pack(side=Side.Left, expand=True, fill=Fill.Both, anchor=anchor)

				for child in children:
					child.pack(Side.Left, anchor=anchor)

				Spacer(cont).pack(side=Side.Left, expand=True, fill=Fill.Both, anchor=anchor)

			elif self.justification == 'end':
				for child in children:
					child.pack(Side.Right, anchor=anchor)

			elif self.justification == 'space-around':
				for child in children:
					child.pack(Side.Left, True, anchor=anchor)

			elif self.justification == 'space-between':
				for i, child in enumerate(children):
					child.pack(Side.Left, anchor=anchor)

					if not i == len(children) - 1:
						Spacer(cont).pack(side=Side.Left, expand=True, fill=Fill.Both, anchor=anchor)

			elif self.justification == 'space-evenly':
				Spacer(cont).pack(side=Side.Left, expand=True, fill=Fill.Both, anchor=anchor)

				for i, child in enumerate(children):
					child.pack(Side.Left, anchor=anchor)
					Spacer(cont).pack(side=Side.Left, expand=True, fill=Fill.Both, anchor=anchor)

			else:
				print('Fuck off.')

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
				for child in children:
					child.pack(Side.Top, anchor=anchor)

			elif self.justification == 'center':
				Spacer(cont).pack(side=Side.Top, expand=True, fill=Fill.Both, anchor=anchor)

				for child in children:
					child.pack(Side.Top, anchor=anchor)

				Spacer(cont).pack(side=Side.Top, expand=True, fill=Fill.Both, anchor=anchor)

			elif self.justification == 'end':
				for child in children:
					child.pack(Side.Bottom, anchor=anchor)

			elif self.justification == 'space-around':
				for child in children:
					child.pack(Side.Top, True, anchor=anchor)

			elif self.justification == 'space-between':
				for i, child in enumerate(children):
					child.pack(Side.Top, anchor=anchor)

					if not i == len(children) - 1:
						Spacer(cont).pack(side=Side.Top, expand=True, fill=Fill.Both, anchor=anchor)

			elif self.justification == 'space-evenly':
				Spacer(cont).pack(side=Side.Top, expand=True, fill=Fill.Both, anchor=anchor)

				for i, child in enumerate(children):
					child.pack(Side.Top, anchor=anchor)
					Spacer(cont).pack(side=Side.Top, expand=True, fill=Fill.Both, anchor=anchor)

			else:
				print('Fuck off.')


# widgets
class Container(Widget):
	@property
	def supported_styles(self) -> SupportedStyles:
		return SupportedStyles(True, False, False, False, False, False, False, False, False, False)

	def __init__(self, parent: Parent, layout: Layout, **kwargs):
		super().__init__(parent, **kwargs)

		self._layout = layout
		self._children: List[Widget] = []
		self._children_layout_ppts: List[layout.properties_class()] = []

	def on_init(self, parent: Parent, **kwargs):
		self._style = WidgetStyle()
		self._tk_widget = tk.Frame(parent)

	def add_widget(self, widget: Widget, layout_ppts):
		self._children.append(widget)

		assert isinstance(layout_ppts, self._layout.properties_class)
		self._children_layout_ppts.append(layout_ppts)

	def remove_widget(self, id_: str):
		i, child = next(((_, __) for (_, __) in enumerate(self._children) if __.id == id_), (None, None))

		if child is None:
			raise Exception(f'Children with ID {id_} not found.')

		self._children.pop(i)
		child[0].hide()

	def pack(self, side: Side = Side.Top, expand: bool = False, fill: Fill = Fill.No, anchor: Anchor = Anchor.No):
		self._layout.lay_out_children(self, self._children, self._children_layout_ppts)
		super().pack(side, expand, fill, anchor)

	def grid(self, row: int, column: int, row_span: int = 1, column_span: int = 1, sticky: str = 'N'):
		self._layout.lay_out_children(self, self._children, self._children_layout_ppts)
		super().grid(row, column, row_span, column_span, sticky)


class LabelContainer(HasText, Container):
	def on_init(self, parent: Parent, **kwargs):
		self._tk_widget = tk.LabelFrame(parent, text=self.text)
