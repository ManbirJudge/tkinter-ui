import tkinter as tk
import warnings
from abc import ABC, abstractmethod
from typing import Dict, Callable, List

from base_classes import BaseWidget
from base_types import TkWidget, WidgetName, WidgetProperty, Orientation, SelectionMode, ActiveStyle, Point, Arrows, CapStyle
from style import WidgetStyle, SupportedStyles, Color


# TODO
# - visibility
# - enable/disable

# widget
class Widget(BaseWidget, ABC):
	# properties
	name: WidgetName
	properties: Dict[str, WidgetProperty]
	supported_styles: SupportedStyles = SupportedStyles(False, False, False, False, False, False, False, False, False, False)

	@property
	def style(self) -> WidgetStyle:
		return self._style

	@property
	def rendered(self) -> bool:
		return self._rendered

	# initialization
	def __init__(self, parent: BaseWidget, style: WidgetStyle = None):
		super().__init__(parent)

		print('Initializing Widget.')

		self._style = style if style is not None else self.theme.get(self.name)
		self._rendered = False
		self._tk_widget = None

	# modification
	def update(self, **ppts):
		"""
		Updates the properties of the Tkinter widget.
		:param ppts: Update properties.
		"""

		for ppt_name in ppts:
			if ppt_name not in list(self.properties.keys()):
				raise Exception(f'\'{ppt_name}\' is not a valid property of {self.__class__.__name__}.')

			ppt = self.properties[ppt_name]
			ppt_new_val = ppts[ppt_name]

			if not isinstance(ppt_new_val, ppt['type']):
				raise Exception(f'\'{ppt_name}\' must be of type \'{ppt["type"]}\'.')

			setattr(self, f'_ppt_{ppt_name}', ppt_new_val)

		if self._rendered:
			self.config_tk_widget()

	# Tk compatibility
	@abstractmethod
	def create_tk_widget(self, tk_parent: TkWidget):
		pass

	def config_tk_widget(self, which_ones: List[str] = None):
		if self._tk_widget is None:
			return

		if which_ones is None:
			which_ones = []

		if len(which_ones) == 0:
			for ppt_name, ppt in self.properties.items():
				if ppt['custom_implementation']:
					custom_func_name = f'config_{ppt_name}'

					if not hasattr(self, custom_func_name):
						raise Exception(f'\'{self.__class__.__name__}\' must have function \'{custom_func_name}\' to configure the property \'{ppt_name}\'.')

					getattr(self, custom_func_name)()

				else:
					self._tk_widget[ppt['tk_name']] = getattr(self, f'_ppt_{ppt_name}')

		else:
			for ppt_name in which_ones:
				if ppt_name not in (self.properties.keys()):
					raise Exception(f'Cannot update \'{ppt_name}\' as it is not a property of \'{self.__class__.__name__}\'.')

				ppt = self.properties[ppt_name]

				# TODO: implement the following code only once (DRY)
				if ppt['custom_implementation']:
					custom_func_name = f'config_{ppt_name}'

					if not hasattr(self, custom_func_name):
						raise Exception(f'\'{self.__class__.__name__}\' must have function \'{custom_func_name}\' to configure the property \'{ppt_name}\'.')

					getattr(self, custom_func_name)()

				else:
					self._tk_widget[ppt['tk_name']] = getattr(self, f'_ppt_{ppt_name}')

	def style_tk_widget(self):
		widget = self._tk_widget
		theme = self.theme

		active_styles_supported = self.supported_styles.active_styles
		select_styles_supported = self.supported_styles.select_styles
		inactive_select_styles_supported = self.supported_styles.inactive_select_styles
		disabled_styles_supported = self.supported_styles.disabled_styles
		read_only_styles_supported = self.supported_styles.read_only_styles

		# background
		if self.supported_styles.bg:
			bg = theme.color_(self.style.background)
			bg_active = theme.color_(self.style.background_active)
			bg_select = theme.color_(self.style.background_select)
			bg_inactive_select = theme.color_(self.style.background_inactive_select)
			bg_disabled = theme.color_(self.style.background_disabled)
			bg_read_only = theme.color_(self.style.background_read_only)

			if bg is not None:
				widget.configure(background=bg)

			if active_styles_supported:
				if bg_active is not None:
					widget.configure(activebackground=bg_active)

			if select_styles_supported:
				if bg_select is not None:
					widget.configure(selectbackground=bg_select)

			if inactive_select_styles_supported:
				if bg_inactive_select is not None:
					widget.configure(inactiveselectbackground=bg_inactive_select)

			if disabled_styles_supported:
				if bg_disabled is not None:
					widget.configure(disabledbackground=bg_disabled)

			if read_only_styles_supported:
				if bg_read_only is not None:
					widget.configure(readonlybackground=bg_read_only)

		# foreground
		if self.supported_styles.fg:
			fg = theme.color_(self.style.foreground)
			fg_active = theme.color_(self.style.foreground_active)
			fg_select = theme.color_(self.style.foreground_select)
			fg_disabled = theme.color_(self.style.foreground_disabled)

			if fg is not None:
				widget.configure(foreground=fg)

			if active_styles_supported:
				if fg_active is not None:
					widget.configure(activeforeground=fg_active)

			if select_styles_supported:
				if fg_select is not None:
					widget.configure(selectforeground=fg_select)

			if disabled_styles_supported:
				if fg_disabled is not None:
					widget.configure(disabledforeground=fg_disabled)

		# font
		if self.supported_styles.font:
			font = self.style.font

			if font is not None:
				widget.configure(font=font)

		# cursor
		widget.configure(cursor=self.style.cursor.value)

		# border
		if self.supported_styles.border:
			border = self.style.border

			if border is not None:
				# clr = border.color if isinstance(border.color, str) else rgb_to_hex(border.color)

				widget.configure(
					borderwidth=border.width,
					relief=border.type.value
				)

				if active_styles_supported:
					# widget.configure(activerelief=border.active_type.value)
					pass

				if select_styles_supported:
					widget.configure(selectborderwidth=border.select_width)

		# highlight
		if self.supported_styles.highlight:
			highlight = self.style.highlight

			if highlight is not None:
				clr = theme.color_(highlight.color)
				bg_clr = theme.color_(highlight.background)

				widget.configure(
					highlightcolor=clr,
					highlightthickness=highlight.width
				)

				if bg_clr is not None:
					widget.configure(highlightbackground=bg_clr)

	def render(self, tk_parent: TkWidget) -> TkWidget:
		if self._rendered:
			raise Exception('Widget is already rendered!')

		self.create_tk_widget(tk_parent)

		self.post_create()

		if self._tk_widget is None:
			raise Exception('TkWidget must not be None!')

		self.config_tk_widget()
		self.style_tk_widget()

		self._rendered = True

		return self._tk_widget

	def post_create(self):
		# For the widgets that required. Ex - ListBox
		pass


# mixins
class WidgetMixin(ABC):
	def __init__(self, **kwargs):
		if not isinstance(self, Widget):
			raise Exception(f'\'{self.__class__.__name__}\' must be a Widget to apply WidgetMixin.')

		super().__init__(**kwargs)

		print('Initializing WidgetMixin.')


class HasText(WidgetMixin):
	def __init__(self, text: str, **kwargs):
		super().__init__(**kwargs)

		if self.properties.get('text', None) is None:
			raise Exception(f'\'{self.__class__.__name__}\' must have \'text\' property.')

		print('Initializing HasText.')

		self._ppt_text = text

	@property
	def text(self) -> str:
		return self._ppt_text

	@text.setter
	def text(self, text: str):
		self._ppt_text = text
		self.config_tk_widget(which_ones=['text'])


class HasVariableText(WidgetMixin):
	def __init__(self, init_text: str = '', **kwargs):
		super().__init__(**kwargs)

		if self.properties.get('txt_var', None) is None:
			raise Exception(f'\'{self.__class__.__name__}\' must have \'txt_var\' property.')

		self._ppt_txt_var = tk.StringVar(self._tk_widget, init_text)

	@property
	def text(self) -> str:
		return self._ppt_txt_var.get()

	@text.setter
	def text(self, text: str):
		self._ppt_txt_var.set(text)


class HasStrValue(WidgetMixin):
	def __init__(self, init_value: str = '', **kwargs):
		super().__init__(**kwargs)

		if self.properties.get('value', None) is None:
			raise Exception(f'\'{self.__class__.__name__}\' must have \'value\' property.')

		self._ppt_value = tk.StringVar(self._tk_widget, init_value)

	@property
	def value(self) -> str:
		return self._ppt_value.get()

	@value.setter
	def value(self, text: str):
		self._ppt_value.set(text)


class HasFloatValue(WidgetMixin):
	def __init__(self, init_value: float = 0.0, **kwargs):
		super().__init__(**kwargs)

		if self.properties.get('value', None) is None:
			raise Exception(f'\'{self.__class__.__name__}\' must have \'value\' property.')

		self._ppt_value = tk.DoubleVar(self._tk_widget, init_value)

	@property
	def value(self) -> float:
		return self._ppt_value.get()

	@value.setter
	def value(self, value: float):
		self._ppt_value.set(value)


class HasBoolValue(WidgetMixin):
	def __init__(self, init_value: bool = False, **kwargs):
		super().__init__(**kwargs)

		if self.properties.get('value', None) is None:
			raise Exception(f'\'{self.__class__.__name__}\' must have \'value\' property.')

		self._ppt_value = tk.BooleanVar(self._tk_widget, init_value)

	@property
	def value(self) -> bool:
		return self._ppt_value.get()

	@value.setter
	def value(self, value: bool):
		self._ppt_value.set(value)


class Clickable(WidgetMixin):
	def __init__(self, click_listener: Callable = None, **kwargs):
		super().__init__(**kwargs)

		if self.properties.get('click_listener', None) is None:
			raise Exception(f'\'{self.__class__.__name__}\' must have \'click_listener\' property.')

		print('Initializing Clickable.')

		self._ppt_click_listener = click_listener

	@property
	def click_listener(self) -> Callable:
		return self._ppt_click_listener

	@click_listener.setter
	def click_listener(self, click_listener: Callable):
		self._ppt_click_listener = click_listener
		self.config_tk_widget(which_ones=['click_listener'])


# widgets
class Button(Clickable, HasText, Widget):
	name = WidgetName.Button
	properties = {
		'text': {
			'type': str,
			'tk_name': 'text',
			'custom_implementation': False
		},
		'click_listener': {
			'type': Callable,
			'tk_name': 'command',
			'custom_implementation': False
		}
	}
	supported_styles = SupportedStyles(True, True, True, True, False, True, False, False, True, False)

	def create_tk_widget(self, tk_parent: TkWidget):
		self._tk_widget = tk.Button(master=tk_parent)


class Entry(HasVariableText, Widget):
	name = WidgetName.Entry
	properties = {
		'txt_var': {
			'type': tk.StringVar,
			'tk_name': 'textvariable',
			'custom_implementation': False
		}
	}
	supported_styles = SupportedStyles(True, True, True, True, True, False, True, True, True, True)

	def create_tk_widget(self, tk_parent: TkWidget):
		self._tk_widget = tk.Entry(master=tk_parent)


class ComboBox(HasVariableText, Widget):
	name = WidgetName.ComboBox
	properties = {
		'txt_var': {
			'type': str,
			'tk_name': 'textvariable',
			'custom_implementation': False
		},
		'options': {
			'type': list,
			'tk_name': None,
			'custom_implementation': True
		}
	}
	supported_styles = SupportedStyles(True, True, True, True, False, True, False, False, True, False)

	def __init__(self, options: List[str], **kwargs):
		super().__init__(**kwargs)

		self._ppt_options = options

	def create_tk_widget(self, tk_parent: TkWidget):
		self._tk_widget = tk.OptionMenu(tk_parent, None, None)

	def config_options(self):
		menu = self._tk_widget['menu']
		menu.delete(0, 'end')

		def gen_cmd(_: str):
			return lambda: self._ppt_txt_var.set(_)

		for option in self._ppt_options:
			menu.add_command(
				label=option,
				command=gen_cmd(option)
			)


class SpinBox(HasFloatValue, Widget):
	name = WidgetName.SpinBox
	properties: Dict[str, WidgetProperty] = {
		'minimum': {
			'type': float,
			'tk_name': 'from_',
			'custom_implementation': False
		},
		'maximum': {
			'type': float,
			'tk_name': 'to',
			'custom_implementation': False
		},
		'delta': {
			'type': float,
			'tk_name': 'increment',
			'custom_implementation': False
		},
		'txt_fmt': {
			'type': str,
			'tk_name': 'format',
			'custom_implementation': False,
			'default': '%.2f'
		},
		'value': {
			'type': float,
			'tk_name': 'textvariable',
			'custom_implementation': False
		}
	}
	supported_styles = SupportedStyles(True, True, True, True, True, True, True, True, True, True)

	def __init__(self, minimum: float, maximum: float, delta: float, txt_fmt: str = None, **kwargs):
		super().__init__(**kwargs)

		self._ppt_minimum = minimum
		self._ppt_maximum = maximum
		self._ppt_delta = delta
		self._ppt_txt_fmt = txt_fmt if txt_fmt is not None else self.properties['txt_fmt']['default']

	def create_tk_widget(self, tk_parent: TkWidget):
		self._tk_widget = tk.Spinbox(tk_parent)


class CheckBox(HasBoolValue, Clickable, HasText, Widget):
	name = WidgetName.CheckBox
	properties = {
		'text': {
			'type': str,
			'tk_name': 'text',
			'custom_implementation': False
		},
		'click_listener': {
			'type': Callable,
			'tk_name': 'command',
			'custom_implementation': False
		},
		'value': {
			'type': bool,
			'tk_name': 'variable',
			'custom_implementation': False
		}
	}
	supported_styles = SupportedStyles(True, True, True, True, False, True, False, False, True, False)

	def create_tk_widget(self, tk_parent: TkWidget):
		self._tk_widget = tk.Checkbutton(tk_parent)


class Slider(HasFloatValue, Widget):
	name = WidgetName.Slider
	properties = {
		'orientation': {
			'type': Orientation,
			'tk_name': None,
			'custom_implementation': True
		},
		'value': {
			'type': float,
			'tk_name': 'variable',
			'custom_implementation': False
		},

		'minimum': {
			'type': float,
			'tk_name': 'from_',
			'custom_implementation': False
		},
		'maximum': {
			'type': float,
			'tk_name': 'to',
			'custom_implementation': False
		},
		'delta': {
			'type': float,
			'tk_name': 'resolution',
			'custom_implementation': False
		},
		'show_val': {
			'type': bool,
			'tk_name': 'showval',
			'custom_implementation': False
		}
	}
	supported_styles = SupportedStyles(True, True, True, True, True, False, False, False, True, True)

	def __init__(
			self,
			orientation: Orientation = Orientation.Horizontal,
			minimum: float = 0.0,
			maximum: float = 100.0,
			delta: float = 0.5,
			show_val: bool = False,
			**kwargs
	):
		super().__init__(**kwargs)

		self._ppt_orientation = orientation
		self._ppt_minimum = minimum
		self._ppt_maximum = maximum
		self._ppt_delta = delta
		self._ppt_show_val = show_val

	def create_tk_widget(self, tk_parent: TkWidget):
		self._tk_widget = tk.Scale(tk_parent)

	def config_orientation(self):
		self._tk_widget.configure(orient=self._ppt_orientation.value)


class RadioButton(HasText, Widget):
	name = WidgetName.RadioButton
	supported_styles = SupportedStyles(True, True, True, True, True, True, False, False, True, True)
	properties = {
		'text': {
			'type': str,
			'tk_name': 'text',
			'custom_implementation': False
		},
		'value': {
			'type': str,
			'tk_name': 'value',
			'custom_implementation': False
		},
		'variable': {
			'type': tk.StringVar,
			'tk_name': 'variable',
			'custom_implementation': False
		}
	}

	def __init__(self, value: str, variable: tk.StringVar, **kwargs):
		super().__init__(**kwargs)

		self._ppt_value = value
		self._ppt_variable = variable

	def create_tk_widget(self, tk_parent: TkWidget):
		self._tk_widget = tk.Radiobutton(tk_parent)


class ListBox(Widget):
	# TODO: add scrollbar

	name = WidgetName.ListBox
	properties = {
		'selection_mode': {
			'type': SelectionMode,
			'tk_name': None,
			'custom_implementation': True
		},
		'active_item_style': {
			'type': ActiveStyle,
			'tk_name': None,
			'custom_implementation': True
		}
	}
	supported_styles = SupportedStyles(True, True, True, True, True, True, True, True, True, True)

	# ---
	def __init__(self, items: List[str], selection_mode: SelectionMode = SelectionMode.Single, active_item_style: ActiveStyle = ActiveStyle.No, **kwargs):
		super().__init__(**kwargs)

		self._items = items

		self._ppt_selection_mode = selection_mode
		self._ppt_active_item_style = active_item_style

	def create_tk_widget(self, tk_parent: TkWidget):
		self._tk_widget = tk.Listbox(tk_parent)

	def post_create(self):
		self.add_items_to_list_box()

	# ---
	def add_items_to_list_box(self):
		self._tk_widget.insert(tk.END, *self._items)

	def config_selection_mode(self):
		self._tk_widget.configure(selectmode=self._ppt_selection_mode.value)

	def config_active_item_style(self):
		self._tk_widget.configure(activestyle=self._ppt_active_item_style.value)

	# ---
	def style_tk_widget(self):
		super().style_tk_widget()

		self._tk_widget.configure(selectborderwidth=0, activestyle='none')

	# ---
	@property
	def count(self) -> int:
		return len(self._items)

	@property
	def selected_count(self) -> int:
		return len(self.selected_indices)

	@property
	def selected_items(self) -> List[str]:
		if not self._rendered:
			# TODO: maybe remove the restriction
			raise Exception('ListBox must be rendered to get selected items.')

		return [self._items[i] for i in self.selected_indices]

	@property
	def selected_indices(self) -> List[int]:
		if not self._rendered:
			raise Exception('ListBox must be rendered to get selected indices.')

		return list(self._tk_widget.curselection())

	# ---
	def select_index(self, i: int):
		self.select_indices(i, i)

	def select_indices(self, start: int, end: int):
		if not self._rendered:
			raise Exception('ListBox must be rendered to select indices.')

		if self._ppt_selection_mode == SelectionMode.Single:
			warnings.warn('Selecting multiple indices while in \'single\' selection mode. Operation cancelled!', RuntimeWarning)
			return

		self._tk_widget.selection_set(start, end)

	def select_all(self):
		self.select_indices(0, self.count - 1)

	# ---
	def unselect_index(self, i: int):
		self.unselect_indices(i, i)

	def unselect_indices(self, start: int, end: int):
		if not self._rendered:
			raise Exception('ListBox must be rendered to unselect indices.')

		self._tk_widget.selection_clear(start, end)

	def unselect_all(self):
		self.unselect_indices(0, self.count - 1)

	# ---
	def remove_item(self, i: int):
		self.remove_items(i, i)

	def remove_items(self, start: int, end: int):
		del self._items[start:end]

		if self._rendered:
			self._tk_widget.delete(start, end)

	def remove_all_items(self):
		self.remove_items(0, self.count - 1)

	# ---
	def set_items(self, new_items: List[str]):
		self.unselect_all()
		self.remove_all_items()

		self._items = new_items

		if self._rendered:
			self.add_items_to_list_box()

	# ---
	def add_item(self, item: str, i: int):
		self.add_items([item], i)

	def add_items(self, items: List[str], i: int):
		self._items[i:i] = items

		if self._rendered:
			self._tk_widget.insert(i, *items)

	def append_item(self, item: str):
		self.append_items([item])

	def append_items(self, items: List[str]):
		self.add_items(items, self.count - 1)


class Canvas(Widget):
	name = WidgetName.Canvas
	properties = {}
	supported_styles = SupportedStyles(True, False, False, True, True, True, True, True, True, True)

	# ---
	def create_tk_widget(self, tk_parent: TkWidget):
		self._tk_widget = tk.Canvas(tk_parent)

	# ---
	def create_line(
			self,
			pt1: Point,
			pt2: Point,
			fill_color: Color = 'white',
			outline_width: int = 1,

			arrows: Arrows = Arrows.No,
			cap_style: CapStyle = CapStyle.Round
	):
		assert self._rendered

		self._tk_widget.create_line(
			pt1.x, pt1.y,
			pt2.x, pt2.y,
			fill=self.theme.color_(fill_color),
			width=outline_width,
			arrow=arrows.value,
			capstyle=cap_style.value,
			smooth=True
		)

	def create_rect(
			self,
			pt1: Point,
			pt2: Point,
			outline_color: Color = 'black',
			fill_color: Color = 'white',
			outline_width: int = 1
	):
		assert self._rendered

		self._tk_widget.create_rectangle(
			pt1.x, pt1.y,
			pt2.x, pt2.y,
			fill=self.theme.color_(fill_color),
			outline=self.theme.color_(outline_color),
			width=outline_width
		)

	def create_ellipse(
			self,
			pt1: Point,
			pt2: Point,
			outline_color: Color = 'black',
			fill_color: Color = 'white',
			outline_width: int = 1
	):
		assert self._rendered

		self._tk_widget.create_oval(
			pt1.x, pt1.y,
			pt2.x, pt2.y,
			fill=self.theme.color_(fill_color),
			outline=self.theme.color_(outline_color),
			width=outline_width
		)
