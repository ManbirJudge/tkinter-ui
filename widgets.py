import tkinter as tk
from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, List, Tuple
from uuid import uuid4

from style import WidgetStyle, SupportedStyles
from type_classes import Side, Fill, Parent, Anchor
from window import Window


class State(Enum):
	Normal = tk.NORMAL
	ReadOnly = 'readonly'
	Active = tk.ACTIVE
	Disabled = tk.DISABLED


# base classes
class Widget(ABC):
	@property
	def id(self) -> str:
		return self._id

	@property
	def visible(self) -> bool:
		return self._visible

	@visible.setter
	def visible(self, _visible: bool):
		if _visible:
			raise NotImplementedError()
		else:
			self.tk_widget.place_forget()
			self.tk_widget.pack_forget()
			self.tk_widget.grid_forget()

		self._visible = _visible

	@property
	def state(self) -> State:
		return State(self.tk_widget.cget('state'))

	@state.setter
	def state(self, _state: State):
		self.tk_widget.configure(state=_state.value)

	@property
	def enabled(self) -> bool:
		return self.state == State.Normal

	@enabled.setter
	def enabled(self, _enabled: bool):
		self.tk_widget.configure(state=tk.NORMAL if _enabled else tk.DISABLED)

	@property
	@abstractmethod
	def supported_styles(self) -> SupportedStyles:
		pass

	@property
	def style(self) -> WidgetStyle:
		return self._style

	@property
	def tk_widget(self):
		return self._tk_widget

	@property
	def theme(self):
		return self._parent.theme

	def __init__(self, parent: Parent, style: WidgetStyle | None = None, **kwargs):
		self._id = str(uuid4())
		self._parent = parent
		self._visible = True
		self._style = style
		self._tk_widget = None

		self.on_init(parent, **kwargs)

	@abstractmethod
	def on_init(self, parent: Parent, **kwargs):
		pass

	def apply_style(self):
		widget = self.tk_widget
		theme = self._parent.theme

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

	def pack(self, side: Side = Side.Top, expand: bool = False, fill: Fill = Fill.No, anchor: Anchor = Anchor.No):
		self.apply_style()

		margin_x, margin_y = self._parent.theme.margin_(self.style.margin)
		pad_x, pad_y = self._parent.theme.margin_(self.style.padding)

		self._tk_widget.pack(
			side=side.value,
			expand=expand,
			fill=fill.value,
			anchor=anchor.value,
			padx=margin_x, pady=margin_y,
			ipadx=pad_x, ipady=pad_y
		)

	def grid(self, row: int, column: int, row_span: int = 1, column_span: int = 1, sticky: str = 'N'):
		self.apply_style()

		margin_x, margin_y = self._parent.theme.margin_(self.style.margin)
		pad_x, pad_y = self._parent.theme.margin_(self.style.padding)

		self._tk_widget.grid(
			row=row, column=column,
			rowspan=row_span, columnspan=column_span,
			padx=margin_x, pady=margin_y,
			ipadx=pad_x, ipady=pad_y,
			sticky=sticky
		)

	def place(self, pos: Tuple[int, int], size: Tuple[int | None, int | None] = (None, None)):
		self.apply_style()

		# margin_x, margin_y = margin_(self.style.margin)
		# pad_x, pad_y = margin_(self.style.padding)

		self.tk_widget.place(
			x=pos[0], y=pos[1],
			width=size[0], height=size[1]
		)

	def hide(self):
		self.visible = False

	def show(self):
		self.visible = True


class HasText:
	def __init__(self, text: str, **kwargs):
		self._text = text

		super().__init__(**kwargs)

	# @text.setter
	# def text(self, _text: str):
	# 	self._text = _text

	@property
	def text(self) -> str:
		return self._text


class HasVariableText:
	def __init__(self, txt_variable: tk.StringVar, **kwargs):
		self._txt_variable = txt_variable

		super().__init__(**kwargs)

	@property
	def text(self) -> str:
		return self._txt_variable.get()

	@text.setter
	def text(self, _text: str):
		self._txt_variable.set(_text)

	@property
	def txt_variable(self) -> tk.StringVar:
		return self._txt_variable

	@abstractmethod
	def set_txt_variable(self, _txt_variable: tk.StringVar):
		pass


class Clickable:
	def __init__(self, on_click: Callable = lambda: 'Empty function!', **kwargs):
		self._on_click = on_click

		super().__init__(**kwargs)

	@property
	def on_click(self) -> Callable:
		return self._on_click

	@on_click.setter
	def on_click(self, _command: Callable):
		self._on_click = _command
		self.on_click_listener_changed()

	@abstractmethod
	def on_click_listener_changed(self):
		pass


# widget classes
class Label(HasText, Widget):
	@property
	def supported_styles(self) -> SupportedStyles:
		return SupportedStyles(True, True, True, True, False, False, False, False, False, False)

	def on_init(self, parent: Parent, **kwargs):
		self._style = self._style if self._style is not None else parent.theme.get('label')
		self._tk_widget = tk.Label(parent, text=self.text)


class Button(Clickable, HasText, Widget):
	@property
	def supported_styles(self) -> SupportedStyles:
		return SupportedStyles(True, True, True, True, False, True, False, False, True, False)

	def on_init(self, parent: Parent, **kwargs):
		self._style = self._style if self._style is not None else parent.theme.get('button')
		self._tk_widget = tk.Button(parent if isinstance(parent, Window) else parent.tk_widget, text=self.text, command=self.on_click)

	def on_click_listener_changed(self):
		self.tk_widget.configure(command=self.on_click)


class Entry(HasVariableText, Widget):
	@property
	def supported_styles(self) -> SupportedStyles:
		return SupportedStyles(True, True, True, True, True, False, True, True, True, True)

	def on_init(self, parent: Parent, **kwargs):
		self._style = self._style if self._style is not None else parent.theme.get('entry')
		self._tk_widget = tk.Entry(parent, textvariable=self.txt_variable)

	def set_txt_variable(self, _txt_variable: tk.StringVar):
		self._txt_variable = _txt_variable
		self._tk_widget.configure(textvariable=self._txt_variable)


class TextArea(Widget):
	@property
	def supported_styles(self) -> SupportedStyles:
		return SupportedStyles(True, True, True, True, True, False, True, True, True, True)

	def on_init(self, parent: Parent, **kwargs):
		self._style = self._style if self._style is not None else parent.theme.get('text-area')
		self._tk_widget = tk.Text(parent, )

	def insert_text(self, txt: str, at: int | str):
		if isinstance(at, int):
			at = str(float(at))

		self._tk_widget.insert(at, txt)

	def append_text(self, txt: str):
		self.insert_text(txt, tk.END)

	def append_line(self, txt: str):
		self.append_text(f'{txt}\n')

	def get_text(self, from_: int | str, to: int | str) -> str:
		if isinstance(from_, int):
			from_ = str(float(from_))

		return self._tk_widget.get(from_, to)

	def get_all_text(self) -> str:
		return self.get_text(1, tk.END)

	def delete_text(self, from_: int | str, to: int | str):
		if isinstance(from_, int):
			from_ = str(float(from_))

		self._tk_widget.delete(from_, to)

	def clear(self):
		self.delete_text(1, tk.END)


class ComboBox(Widget):
	@property
	def supported_styles(self) -> SupportedStyles:
		return SupportedStyles(True, True, True, True, False, True, False, False, True, False)

	def __init__(self, parent: Parent, options: List[str], init_selection: int = 0, **kwargs):
		self._options = options
		self._value = tk.StringVar(value=self._options[init_selection])

		super().__init__(parent=parent, **kwargs)

	def on_init(self, parent: Parent, **kwargs):
		self._style = self._style if self._style is not None else parent.theme.get('combo-box')
		self._tk_widget = tk.OptionMenu(parent, self._value, *self._options)

	@property
	def value(self) -> str:
		return self._value.get()

	@property
	def selected_index(self) -> int:
		return self._options.index(self.value)


class SpinBox(Widget):
	@property
	def supported_styles(self) -> SupportedStyles:
		return SupportedStyles(True, True, True, True, True, True, True, True, True, True)

	def __init__(
			self,
			parent: Parent,
			minimum: int | float = 0.0,
			maximum: int | float = 100.0,
			delta: int | float = 1.0,
			init_value: int | float = 4.0,
			**kwargs
	):
		self.minimum = minimum
		self.maximum = maximum
		self.delta = delta

		self._value = tk.StringVar(value=str(init_value))

		super().__init__(parent=parent, **kwargs)

	def on_init(self, parent: Parent, **kwargs):
		self._style = self._style if self._style is not None else parent.theme.get('spin-box')
		self._tk_widget = tk.Spinbox(
			parent,
			from_=float(self.minimum),
			to=float(self.maximum),
			increment=float(self.delta),
			textvariable=self._value
		)

	@property
	def value(self) -> float:
		return float(self._value.get())

	@value.setter
	def value(self, _value: int | float):
		self._value.set(str(_value))


class CheckBox(Clickable, HasText, Widget):
	@property
	def supported_styles(self) -> SupportedStyles:
		return SupportedStyles(True, True, True, True, False, True, False, False, True, False)

	def __init__(self, parent: Parent, checked: bool = False, **kwargs):
		self._checked = tk.BooleanVar(parent, checked)

		super().__init__(parent=parent, **kwargs)

	def on_init(self, parent: Parent, **kwargs):
		self._style = self._style if self._style is not None else parent.theme.get('check-box')
		self._tk_widget = tk.Checkbutton(parent, text=self.text, variable=self._checked, command=self.on_click)

	@property
	def checked(self) -> bool:
		return self._checked.get()

	@checked.setter
	def checked(self, _checked: bool):
		self._checked.set(_checked)

	def on_click_listener_changed(self):
		self.tk_widget.configure(command=self.on_click)


class RadioButton:
	def __init__(self):
		raise NotImplementedError()
