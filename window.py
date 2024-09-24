import tkinter as tk
from typing import Tuple

from style import Theme, THEME


class Window(tk.Tk):
	def __init__(self, title: str, size: Tuple[int, int], theme: Theme = THEME):
		super().__init__()

		self.set_title(title)
		self.set_size(size)
		self.theme = theme

		self.configure(background='white')

	def set_title(self, title: str):
		self.title(title)

	def set_size(self, size: Tuple[int, int]):
		self.geometry(f'{size[0]}x{size[1]}')
