import tkinter as tk
from abc import ABC
from typing import List

from base_types import TkWidget, Side, Fill, Orientation, CompoundWidgetName
from base_widget import BaseWidget, BaseWidgetProperty
from object import Object
from style import CompoundWidgetStyle
from widget import Widget, RadioButton


# ---
class CompoundWidgetProperty(BaseWidgetProperty):
	pass


class CompoundWidget(BaseWidget, ABC):
	name: CompoundWidgetName
	properties: List[CompoundWidgetProperty]

	# ---
	@property
	def style(self) -> CompoundWidgetStyle:
		return self._style

	# constructor
	def __init__(self, parent: Object = None, style: CompoundWidgetStyle = None):
		super().__init__(parent, style)


# ---
class RadioButtonGroup(CompoundWidget):
	name = CompoundWidgetName.RadioButtonGroup
	properties = []

	def __init__(
			self,
			parent: Object,
			options: List[str], default: str = None,
			orientation: Orientation = Orientation.Vertical
	):
		super().__init__(parent)

		self._radio_btns: List[RadioButton] = []

		self._options = []
		self._orientation = orientation
		self._value = tk.StringVar(value=default if default is not None else options[0])

		self.set_options(options)

	def create_tk_widget(self, tk_parent: TkWidget):
		self._tk_widget = tk.Frame(tk_parent)

		if self._orientation == Orientation.Vertical:
			side = Side.Top
		else:
			side = Side.Left

		for radio_btn in self._radio_btns:
			radio_btn.render(self._tk_widget).pack(side=side.value)

	def config_tk_widget(self, which_ones: List[str] = None):
		pass

	def style_tk_widget(self):
		pass

	@property
	def value(self) -> str:
		return self._value.get()

	@value.setter
	def value(self, value: str):
		self._value.set(value)

	def set_options(self, options: List[str]):
		self._options = options
		self._radio_btns = [RadioButton(parent=self, text=option, value=option, variable=self._value) for option in self._options]


class Scrollable(CompoundWidget):
	name = CompoundWidgetName.Scrollable
	properties = []

	@property
	def count(self) -> int:
		return len(self._children)

	def __init__(
			self,
			parent: Object,
			item_height: int
	):
		super().__init__(parent)

		self._item_height = item_height
		self._children: List[Widget | CompoundWidget] = []

	def add_widget(self, widget: Widget | CompoundWidget):
		self._children.append(widget)

	def create_tk_widget(self, tk_parent: TkWidget):
		self._tk_widget = tk.Frame(tk_parent)

		w, h = 0, self.count * self._item_height

		_canvas = tk.Canvas(self._tk_widget, scrollregion=(0, 0, w, h))
		_scroll_bar = tk.Scrollbar(self._tk_widget, command=_canvas.yview)

		_canvas.config(yscrollcommand=_scroll_bar.set)

		_sub_frame = tk.Frame(self._tk_widget)

		for child in self._children:
			child.render(_sub_frame).pack(side=Side.Top.value, expand=True, fill=Fill.No.value)

		_canvas.pack(side=Side.Left.value, expand=True, fill=Fill.Both.value)
		_scroll_bar.pack(side=Side.Right.value, fill=Fill.Y.value)

		_scroll_bar.update_idletasks()

		def on_update(_):
			_canvas.create_window(
				(0, 0),
				window=_sub_frame,
				width=self._tk_widget.winfo_width() - _scroll_bar.winfo_width(), height=h,
				anchor='nw'
			)

		self._tk_widget.bind('<Configure>', on_update)
		_canvas.bind_all('<MouseWheel>', lambda evt: _canvas.yview_scroll(-int(evt.delta / 60), 'units'))

	def config_tk_widget(self, which_ones: List[str] = None):
		pass

	def style_tk_widget(self):
		pass
