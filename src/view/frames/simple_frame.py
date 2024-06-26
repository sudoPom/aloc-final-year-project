import tkinter as tk
from typing import Callable

from src.controller.controller import Controller
from src.model.components.simple_component import SimpleComponent
from src.view.frames.base_frame import BaseFrame
from src.view.update_menu_handler import UpdateFormHandler


class SimpleFrame(BaseFrame):
    """
    Widget for interacting with a SimpleFrame

    Args:
        parent (:obj:`tk.Canvas`): The parent canvas.
        controller (:obj:`Controller`): The controller managing component actions.
        re_render_func (:obj:`Callable`): The function for re-rendering.
        component (:obj:`SimpleComponent`): The component associated with the frame.
    """

    def __init__(
        self,
        parent: tk.Canvas,
        controller: Controller,
        re_render_func: Callable,
        component: SimpleComponent,
    ):
        super().__init__(parent, controller, re_render_func, component)
        self.__widget_handler = UpdateFormHandler()

    def create_widget(self):
        """
        Creates the widget for this frame.
        """
        button = tk.Button(
            self,
            text=self.get_component().get_form().get_display_text(),
            bg=self.get_component().get_form().get_colour(),
        )
        button.grid(row=0, column=0, sticky=tk.W)
        self.add_update_button()
        self.add_type_submenu()
        self.add_delete_button()
        button.bind("<Button-1>", self.show_menu)

    def add_update_button(self):
        """
        Adds an update button to the menu.
        """
        component = self.get_component()
        assert isinstance(component, SimpleComponent)
        menu = self.get_menu()
        menu.add_command(
            label="Update",
            command=lambda: self.__widget_handler.create_update_form(
                component,
                self.get_re_render_func(),
                self.get_controller(),
            ),
        )

    def render(self, x, y) -> int:
        """
        Renders the frame at the specified coordinates.

        Args:
            x: The x-coordinate to render the widget on the canvas.
            y: The y-coordinate to render the widget on the canvas.

        Returns:
            int: The height of the frame on the canvas.
        """
        display_text = self.get_display_text()
        parent = self.get_parent()
        parent.create_window(x, y, anchor=tk.NW, window=self)
        parent.update()
        if not display_text:
            return self.winfo_reqheight()
        label = tk.Message(self, font=("Arial", 10), text=display_text, width=500)
        label.grid(row=1, column=0, sticky=tk.W)
        parent.update()
        return y + self.winfo_reqheight()
