from ctypes import windll

from base_classes import PackProperties
from base_types import Fill
from layout import Container, FlexLayout, FlexLayoutOptions
from widgets import Button, Entry, ComboBox, SpinBox, CheckBox
from window import MainWindow

# N_BTNS = 4
# CLR_1 = gen_random_color()
# CLR_2 = gen_random_color()
# BTN_CLRS = gen_gradient(CLR_1, CLR_2, N_BTNS)
#
# def layout_demo():
# 	win = Window('Layout Demo', (500, 500))
#
# 	# ---
# 	def make_btn(parent: Container, i: int):
# 		_ = BTN_CLRS[i]
# 		__ = darken(_, 0.4)
#
# 		btn = OldButton(
# 			parent=parent,
# 			text=f'Button {i + 1}',
# 			style=win.theme.get('button').update(background=_, background_active=__, foreground='white' if is_dark(_) else 'black', foreground_active='white' if is_dark(__) else 'black')
# 		)
#
# 		# btn.click_listener = lambda: parent.remove_widget(btn.id)
#
# 		return btn
#
# 	# ---
# 	container1 = Container(win, layout=AbsoluteLayout())
#
# 	for i in range(N_BTNS):
# 		btn = make_btn(container1, i)
#
# 		container1.add_widget(
# 			btn,
# 			AbsoluteLayoutOptions(
# 				pos=(random.randint(0, 500), random.randint(0, 500)),
# 				size=(random.randint(40, 200), random.randint(10, 100))
# 			)
# 		)
#
# 	container1.pack(side=Side.Left, expand=True, fill=Fill.Both)
#
# 	# ---
# 	win.mainloop()
#
#
# def flex_demo():
# 	win = Window('Flex Demo', (500, 500))
#
# 	cont = Container(win, layout=FlexLayout('vertical', 'center', 'center'))
#
# 	for i in range(N_BTNS):
# 		btn = OldButton(parent=cont, text=f'Button {i + 1}', click_listener=lambda: print('Hello, World!'))
# 		cont.add_widget(btn, FlexLayoutOptions())
#
# 	cont.pack(side=Side.Top, expand=True, fill=Fill.Both)
#
# 	win.mainloop()
#
#
# def style_demo():
# 	win = Window('Style Demo', (500, 500))
#
# 	lbl = Label(
# 		parent=win,
# 		text='Labul!'
# 	)
# 	lbl.pack(expand=True)
#
# 	btn = OldButton(
# 		parent=win,
# 		text='Click me!',
# 		click_listener=lambda: print('Clicked!!!')
# 	)
# 	btn.pack(expand=True)
#
# 	entry = OldEntry(
# 		parent=win,
# 		txt_variable=tk.StringVar()
# 	)
# 	entry.pack(expand=True)
#
# 	combo_box = OldComboBox(parent=win, options=['Apple 🍎', 'Banana 🍌', 'Cucumber 🥒', 'Donut 🍩'])
# 	combo_box.pack(expand=True)
#
# 	spin_box = SpinBox(parent=win, minimum=0, maximum=10, delta=0.5, init_value=4)
# 	spin_box.pack(expand=True)
#
# 	check_box = CheckBox(parent=win, text='You gay?')
# 	check_box.pack(expand=True)
#
# 	txt_area = TextArea(parent=win)
# 	txt_area.pack(expand=True, fill=Fill.Both)
#
# 	win.mainloop()
#
#
# def cursor_demo():
# 	cursors = list(Cursor)
# 	grid_size = math.ceil(math.sqrt(len(cursors)))
#
# 	win = Window('Cursor Demo', (500, 500))
#
# 	cont = Container(win, layout=GridLayout(rows=grid_size, columns=grid_size))
#
# 	print(cursors)
#
# 	for i in range(grid_size):
# 		for j in range(grid_size):
# 			if i * grid_size + j >= len(cursors) - 1:
# 				break
#
# 			cur_cursor = cursors[i * grid_size + j]
# 			btn_style = win.theme.get('button').update(cursor=cur_cursor)
#
# 			btn = OldButton(parent=cont, text=f'{cur_cursor.name}', style=btn_style)
# 			cont.add_widget(btn, GridLayoutOptions(i, j, sticky='nsew'))
#
# 	cont.pack(Side.Left, True, Fill.Both)
#
# 	win.mainloop()
#
#
# def radio_btn_demo():
# 	win = Window('RadioButton Demo', (500, 500))
#
# 	txt_var = tk.StringVar(win, 'Physics')
#
# 	options = ['Physics', 'Chemistry', 'Mathematics', 'Biology']
#
# 	for option in options:
# 		radio_btn = tk.Radiobutton(win, text=option, variable=txt_var, value=option, indicator=random.choice([0, 1]))
# 		radio_btn.pack()
#
# 	OldButton(parent=win, text='Submit', click_listener=lambda: print(txt_var.get())).pack()
#
# 	win.mainloop()
#
#
# def scrollable_demo():
# 	win = Window('Scrollable Demo', (500, 500))
#
# 	scrollable = Scrollable(parent=win, item_height=40)
#
# 	for i in range(N_BTNS):
# 		scrollable.add_widget(OldButton(parent=scrollable, text=f'Button {i}'))
#
# 	scrollable.pack(expand=True, fill=Fill.Both)
#
# 	win.mainloop()

DEBUG_COUNT = 4

count = 0


def new_widgets_demo():
	win = MainWindow(title='New Widgets Demo', size=(500, 500))

	cont = Container(win, FlexLayout('vertical', 'space-evenly'))

	entry = Entry(parent=win)
	combo = ComboBox(parent=win, options=['A', 'B', 'C'])
	spin = SpinBox(parent=win, minimum=-10, maximum=10, delta=0.25, init_value=5)
	check = CheckBox(parent=win, text='You gay?')
	btn = Button(
		parent=win,
		text='Click me!',
		click_listener=lambda: print(entry.text, combo.text, spin.value, check.value)
	)

	cont.add_widget(entry, FlexLayoutOptions())
	cont.add_widget(combo, FlexLayoutOptions())
	cont.add_widget(spin, FlexLayoutOptions())
	cont.add_widget(check, FlexLayoutOptions())
	cont.add_widget(btn, FlexLayoutOptions())

	win.add_widget(cont, 'pack', PackProperties(expand=True, fill=Fill.Both))

	win.show()


def new_layout_demo():
	win = MainWindow('Layout Demo', (500, 500))

	cont = Container(win, layout=FlexLayout('vertical', justification='space-evenly'))

	for i in range(DEBUG_COUNT):
		btn = Button(parent=cont, text=f'Button {i}', click_listener=lambda: print('Hello!'))

		cont.add_widget(btn, FlexLayoutOptions())

	win.add_widget(cont, 'pack', PackProperties(expand=True, fill=Fill.Both))

	win.show()


if __name__ == '__main__':
	windll.shcore.SetProcessDpiAwareness(1)

	new_widgets_demo()
