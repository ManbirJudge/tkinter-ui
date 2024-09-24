import tkinter as tk
from enum import Enum
from typing import Any

Parent = Any  # TODO: Window | Widget


class Side(Enum):
	Left = tk.LEFT
	Right = tk.RIGHT
	Top = tk.TOP
	Bottom = tk.BOTTOM


class Fill(Enum):
	No = tk.NONE
	X = tk.X
	Y = tk.Y
	Both = tk.BOTH


class Anchor(Enum):
	No = None
	North = tk.N
	South = tk.S
	East = tk.E
	West = tk.W
