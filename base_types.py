import tkinter as tk
from collections import namedtuple
from enum import Enum

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


class SelectionMode(Enum):
	Single = tk.SINGLE
	Multiple = tk.MULTIPLE


class ActiveStyle(Enum):
	No = tk.NONE
	Underline = tk.UNDERLINE
	DashedOutline = tk.DOTBOX


# ---
class BaseWidgetName(Enum):
	pass


class WidgetName(BaseWidgetName):
	Label = 'label'
	Button = 'button'
	Entry = 'entry'
	ComboBox = 'combo-box'
	SpinBox = 'spin-box'
	CheckBox = 'check-box'
	RadioButton = 'radio-button'
	Slider = 'slider'
	ListBox = 'list-box'
	Canvas = 'canvas'


class CompoundWidgetName(BaseWidgetName):
	Container = ''
	RadioButtonGroup = 'radio-btn-group'
	Scrollable = 'scrollable'


# ---
Point = namedtuple('Point', 'x y')


class Arrows(Enum):
	No = None
	AtFront = 'first'
	AtRear = 'last'
	AtBoth = 'both'


class CapStyle(Enum):
	Round = 'round'
	Projecting = 'projecting'
	Ass = 'butt'
