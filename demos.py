import math
import random
import tkinter as tk
from ctypes import windll

from layout import AbsoluteLayout, Container, AbsoluteLayoutOptions, FlexLayout, FlexLayoutOptions, GridLayout, GridLayoutOptions
from style import Cursor
from type_classes import Side, Fill
from utils import gen_random_color, gen_gradient, darken, is_dark
from widgets import Button, Label, Entry, TextArea, ComboBox, SpinBox, CheckBox
from window import Window

N_BTNS = 4
CLR_1 = gen_random_color()
CLR_2 = gen_random_color()
BTN_CLRS = gen_gradient(CLR_1, CLR_2, N_BTNS)


def layout_demo():
	win = Window('Layout Demo', (500, 500))

	# ---
	def make_btn(parent: Container, i: int):
		_ = BTN_CLRS[i]
		__ = darken(_, 0.4)

		btn = Button(
			parent=parent,
			text=f'Button {i + 1}',
			style=win.theme.get('button').update(
				background=_,
				background_active=__,
				foreground='white' if is_dark(_) else 'black',
				foreground_active='white' if is_dark(__) else 'black'
			)
		)

		# btn.on_click = lambda: parent.remove_widget(btn.id)

		return btn

	# ---
	container1 = Container(win, layout=AbsoluteLayout())

	for i in range(N_BTNS):
		btn = make_btn(container1, i)

		container1.add_widget(
			btn,
			AbsoluteLayoutOptions(
				pos=(random.randint(0, 500), random.randint(0, 500)),
				size=(random.randint(40, 200), random.randint(10, 100))
			)
		)

	container1.pack(side=Side.Left, expand=True, fill=Fill.Both)

	# ---
	win.mainloop()


def flex_demo():
	win = Window('Flex Demo', (500, 500))

	cont = Container(win, layout=FlexLayout('vertical', 'center', 'center'))

	for i in range(N_BTNS):
		btn = Button(parent=cont, text=f'Button {i + 1}', on_click=lambda: print('Hello, World!'))
		cont.add_widget(btn, FlexLayoutOptions())

	cont.pack(side=Side.Top, expand=True, fill=Fill.Both)

	win.mainloop()


def style_demo():
	win = Window('Style Demo', (500, 500))

	lbl = Label(
		parent=win,
		text='Labul!'
	)
	lbl.pack(expand=True)

	btn = Button(
		parent=win,
		text='Click me!',
		on_click=lambda: print('Clicked!!!')
	)
	btn.pack(expand=True)

	entry = Entry(
		parent=win,
		txt_variable=tk.StringVar()
	)
	entry.pack(expand=True)

	combo_box = ComboBox(parent=win, options=['Apple 🍎', 'Banana 🍌', 'Cucumber 🥒', 'Donut 🍩'])
	combo_box.pack(expand=True)

	spin_box = SpinBox(parent=win, minimum=0, maximum=10, delta=0.5, init_value=4)
	spin_box.pack(expand=True)

	check_box = CheckBox(parent=win, text='You gay?')
	check_box.pack(expand=True)

	txt_area = TextArea(parent=win)
	txt_area.pack(expand=True, fill=Fill.Both)

	win.mainloop()


def cursor_demo():
	cursors = list(Cursor)
	grid_size = math.ceil(math.sqrt(len(cursors)))

	win = Window('Cursor Demo', (500, 500))

	cont = Container(win, layout=GridLayout(rows=grid_size, columns=grid_size))

	print(cursors)

	for i in range(grid_size):
		for j in range(grid_size):
			if i * grid_size + j >= len(cursors) - 1:
				break

			cur_cursor = cursors[i * grid_size + j]
			btn_style = win.theme.get('button').update(cursor=cur_cursor)

			btn = Button(parent=cont, text=f'{cur_cursor.name}', style=btn_style)
			cont.add_widget(btn, GridLayoutOptions(i, j, sticky='nsew'))

	cont.pack(Side.Left, True, Fill.Both)

	win.mainloop()


if __name__ == '__main__':
	windll.shcore.SetProcessDpiAwareness(1)

	cursor_demo()
