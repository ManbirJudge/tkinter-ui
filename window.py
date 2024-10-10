import tkinter as tk
from abc import ABC, abstractmethod
from typing import Tuple, Literal, List

from base_types import TkWindow
from base_widget import PackProperties, PlaceProperties
from compound_widget import CompoundWidget
from object import Object
from style import Theme, THEME
from widget import Widget


# base window
class WindowLike(Object, ABC):
	# ---
	def __init__(self, title: str, size: Tuple[int, int], pos: Tuple[int, int] = None):
		super().__init__(None)

		self._tk_win = self.create_tk_win()

		self._children: List[Tuple[Widget | CompoundWidget, str, PackProperties | PlaceProperties]] = []

		self.set_title(title)
		self.set_size(size)

		if pos is not None:
			self.set_pos(pos)

	# ---
	@abstractmethod
	def create_tk_win(self) -> TkWindow:
		pass

	def set_title(self, title: str):
		self._tk_win.title(title)

	def set_size(self, size: Tuple[int, int]):
		self._tk_win.geometry(f'{size[0]}x{size[1]}')

	def set_pos(self, pos: Tuple[int, int]):
		size = self._tk_win.size

		self._tk_win.geometry(f'{size[0]}x{size[1]}+{pos[0]}+{pos[1]}')

	# ---
	def add_widget(self, widget: Widget | CompoundWidget, placement_method: Literal['place', 'pack'], ppts: PackProperties | PlaceProperties):
		self._children.append((widget, placement_method, ppts))

	# ---
	def show(self):
		for _, __, ___ in self._children:
			margin_x, margin_y = self.theme.margin_(_.style.margin)
			pad_x, pad_y = self.theme.margin_(_.style.padding)

			if __ == 'pack':
				assert isinstance(___, PackProperties)

				_.render(self._tk_win).pack(
					side=___.side.value,
					expand=___.expand,
					fill=___.fill.value,
					padx=margin_x, pady=margin_y,
					ipadx=pad_x, ipady=pad_y
				)

			elif __ == 'place':
				assert isinstance(___, PlaceProperties)

				_.render(self._tk_win).pack(
					x=___.pos[0], y=___.pos[1],
					width=___.size[0], height=___.size[1],
					padx=margin_x, pady=margin_y,
					ipadx=pad_x, ipady=pad_y
				)

			else:
				raise ValueError(f'\'{__}\' is not a valid placement method.')

		self._tk_win.mainloop()


# window
class MainWindow(WindowLike):
	@property
	def theme(self) -> Theme:
		return self._theme

	def __init__(self, title: str, size: Tuple[int, int], theme: Theme = THEME):
		self._theme = theme

		super().__init__(title, size)

	def create_tk_win(self):
		_ = tk.Tk()

		_.configure(bg=self.theme.color_('.bg'))

		return _
