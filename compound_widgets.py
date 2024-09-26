import tkinter as tk
from abc import ABC, abstractmethod
from typing import List

from base_classes import BaseWidget
from base_types import TkWidget, Side, Fill, Orientation
from style import WidgetStyle
from widgets import Widget, RadioButton


# compound widget
class CompoundWidget(BaseWidget, ABC):
	@property
	def style(self) -> WidgetStyle:
		return WidgetStyle()

	@abstractmethod
	def render(self, tk_parent: TkWidget) -> TkWidget:
		pass


# ---
class RadioButtonGroup(CompoundWidget):
	def __init__(
			self,
			parent: BaseWidget,
			options: List[str], default: str = None,
			orientation: Orientation = Orientation.Vertical
	):
		super().__init__(parent)

		self._radio_btns: List[RadioButton] = []

		self._options = []
		self._orientation = orientation
		self._value = tk.StringVar(value=default if default is not None else options[0])

		self.set_options(options)

	def render(self, tk_parent: TkWidget) -> tk.Frame:
		_cont = tk.Frame(tk_parent)

		if self._orientation == Orientation.Vertical:
			side = Side.Top
		else:
			side = Side.Left

		for radio_btn in self._radio_btns:
			radio_btn.render(_cont).pack(side=side.value)

		return _cont

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
	@property
	def count(self) -> int:
		return len(self._children)

	def __init__(
			self,
			parent: BaseWidget,
			item_height: int
	):
		super().__init__(parent)

		self._item_height = item_height
		self._children: List[Widget | CompoundWidget] = []

	def add_widget(self, widget: Widget | CompoundWidget):
		self._children.append(widget)

	def render(self, tk_parent: TkWidget) -> tk.Frame:
		_cont_frame = tk.Frame(tk_parent)

		w, h = 0, self.count * self._item_height

		_canvas = tk.Canvas(_cont_frame, scrollregion=(0, 0, w, h))
		_scroll_bar = tk.Scrollbar(_cont_frame, command=_canvas.yview)

		_canvas.config(yscrollcommand=_scroll_bar.set)

		_sub_frame = tk.Frame(_cont_frame)

		for child in self._children:
			child.render(_sub_frame).pack(side=Side.Top.value, expand=True, fill=Fill.No.value)

		_canvas.pack(side=Side.Left.value, expand=True, fill=Fill.Both.value)
		_scroll_bar.pack(side=Side.Right.value, fill=Fill.Y.value)

		_scroll_bar.update_idletasks()

		def on_update(_):
			_canvas.create_window(
				(0, 0),
				window=_sub_frame,
				width=_cont_frame.winfo_width() - _scroll_bar.winfo_width(), height=h,
				anchor='nw'
			)

		_cont_frame.bind('<Configure>', on_update)
		_canvas.bind_all('<MouseWheel>', lambda evt: _canvas.yview_scroll(-int(evt.delta / 60), 'units'))

		return _cont_frame
