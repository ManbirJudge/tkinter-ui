from copy import deepcopy
from dataclasses import dataclass, fields, field
from enum import Enum
from types import UnionType
from typing import Tuple, Optional, Dict, Any
import tkinter as tk

from base_types import WidgetName, BaseWidgetName, CompoundWidgetName
from utils import rgb_to_hex

# TODO
# - insert styles
# - button background
# - element border width
# - select - color, mode, image, border width

# ---
Color = str | Tuple[int, int, int] | Tuple[int, int, int, int]

Margin = int | str | Tuple[int | str | None, int | str | None] | None
Padding = Margin
Font = str | Tuple['str', int] | Tuple['str', int, 'str'] | None


class Cursor(Enum):
	# common
	Arrow = 'arrow'
	Pencil = 'pencil'
	IBeam = 'xterm'
	Watch = 'watch'

	# arrows and pointers
	ArrowTopRight = 'arrow'  # custom
	ArrowTopLeft = 'top_left_arrow'

	ArrowVerticalDouble = 'double_arrow'

	ArrowDraftSmall = 'draft_small'
	ArrowDraftLarge = 'draft_large'

	ArrowQuestion = 'question_arrow'

	PtrCenter = 'center_ptr'
	PtrLeft = 'left_ptr'
	PtrRight = 'right_ptr'

	# resize arrows
	ArrowResizeUp = 'sb_up_arrow'
	ArrowResizeDown = 'sb_down_arrow'
	ArrowResizeLeft = 'sb_left_arrow'
	ArrowResizeRight = 'sb_right_arrow'

	ArrowResizeVerticalDouble = 'sb_v_double_arrow'
	ArrowResizeHorizontalDouble = 'sb_h_double_arrow'

	# crosses
	Cross = 'cross'
	CrossX = 'X_cursor'
	CrossReverse = 'cross_reverse'
	Crosshair = 'crosshair'
	CrossDiamond = 'diamond_cross'
	CrossIron = 'iron_cross'
	CrossT = 'tcross'

	# hands
	Hand1 = 'hand1'
	Hand2 = 'hand2'

	# sides
	SideTop = 'top_side'
	SideBottom = 'bottom_side'
	SideLeft = 'left_side'
	SideRight = 'right_side'

	# corners
	CornerTopLeft = 'top_left_corner'
	CornerTopRight = 'top_right_corner'
	CornerBottomLeft = 'bottom_left_corner'
	CornerBottomRight = 'bottom_right_corner'

	# angles
	AngleTopLeft = 'ul_angle'
	AngleTopRight = 'ur_angle'
	AngleBottomLeft = 'll_angle'
	AngleBottomRight = 'lr_angle'

	# common icons
	IcExchange = 'exchange'
	IcResize = 'fleur'
	IcHeart = 'heart'
	IcIc = 'Icon'
	IcPirate = 'pirate'
	IcPlus = 'plus'
	IcSailboat = 'sailboat'
	IcSizing = 'sizing'

	# Ts
	TTop = 'top_tee'
	TBottom = 'bottom_tee'
	TLeft = 'left_tee'
	TRight = 'right_tee'

	# based arrows
	ArrowBasedUp = 'based_arrow_up'
	ArrowBasedDown = 'based_arrow_down'

	# vehicles
	Boat = 'boat'
	Shuttle = 'shuttle'

	# animals
	Gobbler = 'gobbler'
	Gumby = 'gumby'
	Spider = 'spider'
	Man = 'man'

	# common objects
	Clock = 'clock'
	CoffeeMug = 'coffee_mug'
	Mouse = 'mouse'
	SprayCan = 'spraycan'
	Star = 'star'
	Trek = 'trek'
	Umbrella = 'umbrella'

	# mouse buttons
	MouseBtnLeft = 'leftbutton'
	MouseBtnMiddle = 'middlebutton'
	MouseBtnRight = 'rightbutton'

	# others
	Bogosity = 'bogosity'
	Circle = 'circle'
	RTLLogo = 'rtl_logo'

	BoxSpiral = 'box_spiral'
	BoxDraped = 'draped_box'

	Dot = 'dot'
	DotBox = 'dotbox'


class BorderType(Enum):
	Flat = tk.FLAT
	Raised = tk.RAISED
	Sunken = tk.SUNKEN
	Groove = tk.GROOVE
	Ridge = tk.RIDGE
	Solid = tk.SOLID


# ---
@dataclass
class Border:
	width: int
	type: BorderType = BorderType.Flat

	active_type: Optional[BorderType] = None
	select_width: Optional[int] = None

	def __post_init__(self):
		if self.active_type is None:
			self.active_type = self.type

		if self.select_width is None:
			self.select_width = self.width

	@staticmethod
	def default():
		return Border(2, BorderType.Solid)


@dataclass
class Highlight:
	color: Color
	width: int
	background: Color | None = None

	@staticmethod
	def default():
		return Highlight('black', 0)


# ---
@dataclass
class SupportedStyles:
	bg: bool
	fg: bool
	font: bool
	border: bool
	highlight: bool

	active_styles: bool
	select_styles: bool
	inactive_select_styles: bool
	disabled_styles: bool
	read_only_styles: bool


# ---
@dataclass
class BaseWidgetStyle:
	background: Color | None = None
	foreground: Color | None = None
	padding: Margin = None
	margin: Margin = None
	font: Font = ('Comic Sans MS', 10)
	cursor: Cursor = Cursor.Arrow
	border: Border = field(default_factory=Border.default)
	highlight: Highlight = field(default_factory=Highlight.default)

	background_active: Color | None = None
	background_select: Color | None = None
	background_inactive_select: Color | None = None
	background_disabled: Color | None = None
	background_read_only: Color | None = None

	foreground_active: Color | None = None
	foreground_select: Color | None = None
	foreground_disabled: Color | None = None

	def update(self, **kwargs):
		valid_fields = {f.name: f.type for f in fields(self)}

		for key, value in kwargs.items():
			if key in valid_fields:
				valid_type = valid_fields[key]

				type_not_valid = False

				if isinstance(valid_type, UnionType) and type(value) not in valid_type.__args__:
					type_not_valid = True
				else:
					if not isinstance(value, valid_type):
						type_not_valid = True

				if type_not_valid:
					raise TypeError(f'\'{key}\' must be of type {valid_type}.')

				setattr(self, key, value)

			else:
				raise AttributeError(f'WidgetStyle has no attribute \'{key}\'')

		return self


@dataclass
class WidgetStyle(BaseWidgetStyle):
	pass


@dataclass
class CompoundWidgetStyle(BaseWidgetStyle):
	additional_styles: Dict[str, Any] = field(default_factory=lambda: {})


# ---
@dataclass
class Theme:
	margin: Dict[str, int]
	color: Dict[str, Color]
	widget: Dict[WidgetName, WidgetStyle]
	compound_widget: Dict[CompoundWidgetName, CompoundWidgetStyle]

	def get(self, name: BaseWidgetName) -> BaseWidgetStyle:
		if isinstance(name, WidgetName):
			return deepcopy(self.widget.get(name, WidgetStyle()))
		elif isinstance(name, CompoundWidgetName):
			return deepcopy(self.compound_widget.get(name, CompoundWidgetStyle()))
		else:
			raise TypeError()

	def margin__(self, margin: str | int | None) -> int:
		if margin is None:
			return 0

		if isinstance(margin, str):
			margin = self.margin[margin]
		elif isinstance(margin, int):
			margin = margin
		else:
			raise TypeError('Margin must be a (valid) string or numerical.')

		return margin

	def margin_(self, margin: Margin) -> Tuple[int, int]:
		if margin is None:
			return 0, 0

		if isinstance(margin, tuple):
			x = self.margin__(margin[0])
			y = self.margin__(margin[1])
		else:
			x = y = self.margin__(margin)

		return x, y

	def color_(self, color_: Color | None) -> str | None:
		if color_ is None:
			return None

		if isinstance(color_, Tuple):
			return rgb_to_hex(color_)

		color_ = str(color_)

		if color_.startswith('.'):
			return self.color.get(color_.removeprefix('.'), '#f0f')

		return color_


THEME = Theme(
	{
		'xsm': 2,
		'sm': 3,
		'n': 5,
		'lg': 8,
		'xl': 11
	},
	{
		'bg': 'white',
		'on-bg': 'black',
		'primary-bg': '#fad2d7',
		'on-primary-bg': 'black',
		'primary': '#fa324d',
		'on-primary': 'white',
		'primary-alt': '#bf283c',
		'on-primary-alt': 'white',
	},
	{
		WidgetName.Label: WidgetStyle(
			margin=(0, 0),
			padding=('sm', 'sm'),
			background='.bg',
			foreground='.on-bg',
			border=Border(width=0),
			cursor=Cursor.Arrow
		),
		WidgetName.Button: WidgetStyle(
			margin=('n', 'sm'),
			padding=('lg', 'sm'),
			background='.primary',
			foreground='.on-primary',
			background_active='.primary-alt',
			foreground_active='.on-primary-alt',
			border=Border(width=1, type=BorderType.Raised),
			cursor=Cursor.Hand2
		),
		WidgetName.Entry: WidgetStyle(
			margin=('n', 'sm'),
			padding=('n', 'n'),
			background='.primary-bg',
			foreground='.on-primary-bg',
			background_select='.primary',
			foreground_select='.on-primary',
			border=Border(width=1, type=BorderType.Solid),
			cursor=Cursor.IBeam
		),
		# 'text-area': WidgetStyle(
		# 	margin=('n', 'n'),
		# 	padding=('n', 'n'),
		# 	background='.primary-bg',
		# 	foreground='.on-primary-bg',
		# 	background_select='.primary',
		# 	foreground_select='.on-primary',
		# 	border=Border(width=1, type=BorderType.Solid),
		# 	cursor=Cursor.IBeam
		# ),
		WidgetName.ComboBox: WidgetStyle(
			margin=('n', 'sm'),
			padding=('n', 'n'),
			background='.primary-bg',
			foreground='.on-primary-bg',
			background_active='.primary',
			foreground_active='.on-primary',
			border=Border(width=1, type=BorderType.Solid),
			cursor=Cursor.Hand2
		),
		WidgetName.SpinBox: WidgetStyle(
			margin=('n', 'sm'),
			padding=('n', 'n'),
			background='.primary-bg',
			foreground='.on-primary-bg',
			background_select='.primary',
			foreground_select='.on-primary',
			border=Border(width=1, type=BorderType.Solid),
			cursor=Cursor.IBeam
		),
		WidgetName.CheckBox: WidgetStyle(
			margin=('n', 'sm'),
			padding=('lg', 'sm'),
			background='#f7e4e6',
			foreground='.on-bg',
			background_active='.primary-bg',
			foreground_active='.on-primary-bg',
			border=Border(width=1, type=BorderType.Solid),
			cursor=Cursor.Hand2
		),
		WidgetName.Slider: WidgetStyle(
			margin=('sm', 'sm'),
			padding=(0, 0),
			background='.bg',
			foreground='.on-bg',
			background_select='.primary',
			foreground_select='.on-primary',
			border=Border(width=1, type=BorderType.Solid)
		),
		WidgetName.RadioButton: WidgetStyle(
			margin=('sm', 'sm'),
			padding=(0, 0),
			background='.bg',
			foreground='.on-bg',
			background_active='.primary-bg',
			foreground_active='.on-primary-bg',
			border=Border(width=0, type=BorderType.Flat),
			cursor=Cursor.Hand2
		),
		WidgetName.ListBox: WidgetStyle(
			margin=('n', 'n'),
			padding=(0, 0),
			background='.bg',
			foreground='.on-bg',
			border=Border(width=1, type=BorderType.Solid),
			background_select='.primary-bg',
			foreground_select='.on-primary-bg'
		),
		WidgetName.Canvas: WidgetStyle(
			margin=('n', 'n'),
			padding=(0, 0),
			background='.bg',
			border=Border(width=1, type=BorderType.Solid)
		)
	},
	{}
)
