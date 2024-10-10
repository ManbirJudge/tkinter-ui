import tkinter as tk
from abc import ABC, abstractmethod
from uuid import uuid5, uuid1

from PIL import ImageTk
from PIL.Image import Image

from base_types import Point, Arrows, CapStyle, WidgetName, TkWidget
from style import SupportedStyles, Color, Font
from widget import Widget


# TODO: make it better

# ---
# class CanvasEntity(ABC):
# 	@property
# 	def id(self) -> str:
# 		return self.__id
#
# 	def __init__(self):
# 		self.__id = str(uuid1())
#
# 		self.__canvas_id = None
#
# 	@abstractmethod
# 	def draw(self, canvas: 'Canvas'):
# 		pass
#
# 	def bring_forward(self):
# 		assert self.__canvas_id is not None
#
#
# class Line(CanvasEntity):
# 	def __init__(self, pt1: Point, pt2: Point):
# 		super().__init__()
#
# 		self.pt1 = pt1
# 		self.pt2 = pt2
#
# 	def draw(self, canvas: 'Canvas'):
# 		canvas.draw_line(self.pt1, self.pt2)


# ---
class Canvas(Widget):
	name = WidgetName.Canvas
	properties = []
	supported_styles = SupportedStyles(True, False, False, True, True, True, True, True, True, True)

	# ---
	def create_tk_widget(self, tk_parent: TkWidget):
		self._tk_widget = tk.Canvas(tk_parent)

	# ---
	def draw_line(
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

	def draw_rect(
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

	def draw_ellipse(
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

	def draw_arc(
			self,
			pt1: Point,
			pt2: Point,
			outline_color: Color = 'black',
			outline_width: int = 1
	):
		assert self._rendered

		self._tk_widget.create_arc(
			pt1.x, pt1.y,
			pt2.x, pt2.y,
			outline=self.theme.color_(outline_color),
			width=outline_width
		)

	# ---
	def draw_circle(
			self,
			center: Point,
			radius: int,
			outline_color: Color = 'black',
			fill_color: Color = 'white',
			outline_width: int = 1
	):
		self.draw_ellipse(
			Point(center.x - radius, center.y - radius),
			Point(center.x + radius, center.y + radius),
			outline_color,
			fill_color,
			outline_width
		)

	# ---
	def draw_text(self, pt: Point, txt: str, color: Color, font: Font = ('Major Mono Display', 20)):
		self._tk_widget.create_text(
			pt.x, pt.y,
			text=txt,
			font=font,
			fill=self.theme.color_(color),
			anchor='nw'
		)

	def draw_image(self, pt: Point, image: Image):
		"""TODO: not fking working"""

		assert self._rendered

		tk_img = ImageTk.PhotoImage(image)

		self._tk_widget.create_image(pt.x, pt.y, image=tk_img, anchor='nw')

# class Graph(Canvas):
# 	def __init__(self, parent: Object):
# 		super().__init__(parent)
#
# 		self.origin = Point(-1, -1)
#
# 		self.__last_mouse_pos = None
#
# 	def config_tk_widget(self, which_ones: List[str] = None):
# 		super().config_tk_widget(which_ones)
#
# 		def work():
# 			self.origin = Point(self._tk_widget.winfo_width() // 2, self._tk_widget.winfo_height() // 2)
#
# 			self.redraw()
#
# 		self._tk_widget.after(100, work)
#
# 		self._tk_widget.bind('<Configure>', lambda _: self.redraw())
#
# 		self._tk_widget.bind('<B1-Motion>', lambda evt: self.on_drag(evt))
# 		self._tk_widget.bind('<ButtonRelease-1>', lambda _: self.on_drag_end())
#
# 	# ---
# 	def redraw(self):
# 		start = time.time()
#
# 		if not self._rendered:
# 			return
#
# 		self._tk_widget.delete('all')
#
# 		self.draw_axes()
#
# 		end = time.time()
#
# 		print(f'Redrawn in: {(end - start):.2f} s')
#
# 	def draw_axes(self):
# 		# x-axis
# 		self.draw_line(Point(0, self.origin.y), Point(self._tk_widget.winfo_width(), self.origin.y), fill_color='black', arrows=Arrows.AtBoth, outline_width=3)
#
# 		# y-axis
# 		self.draw_line(Point(self.origin.x, 0), Point(self.origin.x, self._tk_widget.winfo_height()), fill_color='black', arrows=Arrows.AtBoth, outline_width=3)
#
# 	# ---
# 	def on_drag(self, drag_evt):
# 		cur_mouse_pos = Point(drag_evt.x, drag_evt.y)
#
# 		if self.__last_mouse_pos is not None:
# 			delta_pos = Point(cur_mouse_pos.x - self.__last_mouse_pos.x, cur_mouse_pos.y - self.__last_mouse_pos.y) \
#
# 			self.origin = Point(self.origin.x + delta_pos.x, self.origin.y + delta_pos.y)
#
# 		self.redraw()
# 		self.__last_mouse_pos = cur_mouse_pos
#
# 	def on_drag_end(self):
# 		self.__last_mouse_pos = None
