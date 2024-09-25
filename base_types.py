import tkinter as tk
from enum import Enum
from typing import Any, TypedDict, Type

# ---
TkWindow = tk.Tk | tk.Toplevel
TkWidget = tk.Widget | tk.Label | tk.Button | tk.Entry | tk.OptionMenu | tk.Scale | tk.Checkbutton | tk.Frame | tk.LabelFrame | tk.Canvas | tk.Listbox | tk.Spinbox | TkWindow


# ---
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


class Orientation(Enum):
	Horizontal = tk.HORIZONTAL
	Vertical = tk.VERTICAL


class State(Enum):
	Normal = tk.NORMAL
	ReadOnly = 'readonly'
	Active = tk.ACTIVE
	Disabled = tk.DISABLED


# ---
class WidgetName(Enum):
	# TODO: maybe extend to base widgets too

	Label = 'label'
	Button = 'button'
	Entry = 'entry'
	ComboBox = 'combo-box'
	SpinBox = 'spin-box'
	CheckBox = 'check-box'
	Spacer = 'spacer'


class WidgetProperty(TypedDict):
	type: Type
	tk_name: str
	custom_implementation: bool  # has no use yet
	default: Any | None
