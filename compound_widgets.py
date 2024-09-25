from abc import ABC, abstractmethod

from base_classes import BaseWidget
from base_types import TkWidget


# compound widget
class CompoundWidget(BaseWidget, ABC):
	@abstractmethod
	def render(self, tk_parent: TkWidget) -> TkWidget:
		pass

# ---
# class Scrollable(Container):
# 	def __init__(
# 			self,
# 			item_height: int,
# 			**kwargs
# 	):
# 		self._item_height = item_height
#
# 		super().__init__(**kwargs)
#
# 	def on_init(self, parent: Parent, **kwargs):
# 		self._style = WidgetStyle()
# 		self._tk_widget = tk.Frame(parent if isinstance(parent, Window) else parent.tk_widget)
#
# 		self._canvas = tk.Canvas(
# 			self._tk_widget,
# 			scrollregion=(
# 				0, 0,
# 				self._tk_widget.winfo_width(), self.count * self._item_height
# 			),
# 			background='red'
# 		)
#
# 	def add_widget(self, widget: Widget, **kwargs):
# 		super().add_widget(widget)
#
# 		self._canvas.configure(scrollregion=(
# 			0, 0,
# 			self._tk_widget.winfo_width(), self.count * self._item_height
# 		))
#
# 	def pack(self, side: Side = Side.Top, expand: bool = False, fill: Fill = Fill.No, anchor: Anchor = Anchor.No):
# 		for child in self._children:
# 			print(child)
# 			child.pack(expand=True, fill=Fill.Both)
#
# 		self._canvas.pack(expand=True, fill=tk.BOTH)
#
# 		super().pack(side, expand, fill, anchor)
