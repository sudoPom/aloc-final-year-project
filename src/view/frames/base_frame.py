import tkinter as tk
from typing import Callable, TypeVar

from controller.controller import Controller
from model.components.component import Component
from view.update_menu_handler import UpdateFormHandler


class BaseFrame(tk.Frame):
    Component = TypeVar("Component", bound=Component)
    """
    BaseFrame class represents the base frame for a component in the GUI.

    Methods:
    - __init__(parent, controller, re_render_func, component, render_settings, **kwargs): Initializes a BaseFrame object.
    - create_widgets(): Creates widgets for the frame.
    - get_controller(): Returns the controller.
    - get_component(): Returns the component.
    - get_re_render_func(): Returns the re-render function.
    - get_parent(): Returns the parent widget.
    - get_menu(): Returns the associated menu.
    - trigger_re_render(): Triggers re-rendering of the frame.
    - show_menu(event): Displays the associated menu.
    - change_component_type(component_type): Changes the type of the associated component.
    - extend_component(): Extends the associated component.
    - add_delete_button(): Adds a delete button to the menu.
    - destruct(): Deletes the associated component.
    - add_update_button(): Adds an update button to the menu.
    - add_type_submenu(): Adds a submenu for changing the component type.
    - add_chain_options(): Adds options for chain components to the menu.
    - get_display_text(): Returns the display text of the associated component.
    - render(x, y): Renders the frame at the specified coordinates.
    """

    def __init__(
        self,
        parent: tk.Canvas,
        controller: Controller,
        re_render_func: Callable,
        component: Component,
        render_settings: set,
        **kwargs,
    ):
        """
        Initializes a BaseFrame object.

        Args:
        - parent (tk.Widget): The parent widget.
        - controller (Controller): The controller managing component actions.
        - re_render_func (Callable): The function for re-rendering.
        - component (Component): The component associated with the frame.
        - render_settings (set): The settings for rendering the frame.
        - **kwargs: Additional keyword arguments.
        """
        super().__init__(parent, **kwargs)
        self.__parent = parent
        self.__controller = controller
        self.__re_render_func = re_render_func
        self.__menu = tk.Menu(self, tearoff=0)
        self.__component = component
        self.__widget_handler = UpdateFormHandler()
        self.__render_settings = render_settings
        self.create_widgets()

    def create_widgets(self):
        """
        Creates widgets for the frame.
        """
        button = tk.Button(
            self,
            text=self.__component.get_type().get_display_text(),
            bg=self.__component.get_type().get_colour(),
        )
        button.grid(row=0, column=0, sticky=tk.W)
        if "updatable" in self.__render_settings:
            self.add_update_button()
        if "multi-typed" in self.__render_settings:
            self.add_type_submenu()
        if "chain_component" in self.__render_settings:
            self.add_chain_options()
        if "deletable" in self.__render_settings:
            self.add_delete_button()
        button.bind("<Button-1>", self.show_menu)

    def get_controller(self) -> Controller:
        """
        Returns the controller.

        Returns:
        - Controller: The controller managing component actions.
        """
        return self.__controller

    def get_component(self) -> Component:
        """
        Returns the component.

        Returns:
        - Component: The component associated with the frame.
        """
        return self.__component

    def get_re_render_func(self) -> Callable:
        """
        Returns the re-render function.

        Returns:
        - Callable: The function for re-rendering.
        """
        return self.__re_render_func

    def get_parent(self) -> tk.Canvas:
        """
        Returns the parent widget.

        Returns:
        - tk.Widget: The parent widget.
        """
        return self.__parent

    def get_menu(self) -> tk.Menu:
        """
        Returns the associated menu.

        Returns:
        - tk.Menu: The associated menu.
        """
        return self.__menu

    def trigger_re_render(self):
        """
        Triggers re-rendering of the frame.
        """
        self.__re_render_func()

    def show_menu(self, event):
        """
        Displays the associated menu.

        Args:
        - event: The event that triggered the menu.
        """
        self.__menu.tk_popup(event.x_root, event.y_root)

    def change_component_type(self, component_type):
        """
        Changes the type of the associated component.

        Args:
        - component_type: The new type of the component.
        """
        Controller.change_component_type(self.__component, component_type)
        self.trigger_re_render()

    def extend_component(self):
        """
        Extends the associated component.
        """
        self.__controller.extend_chain_component(self.__component)
        self.trigger_re_render()

    def add_delete_button(self):
        """
        Adds a delete button to the menu.
        """
        self.__menu.add_command(label="Delete", command=self.destruct)

    def destruct(self):
        """
        Deletes the associated component.
        """
        self.__controller.delete_component(self.__component.get_id())
        self.trigger_re_render()

    def add_update_button(self):
        """
        Adds an update button to the menu.
        """
        self.__menu.add_command(
            label="Update",
            command=lambda: self.__widget_handler.create_update_form(
                self, self.__component, self.__re_render_func, self.__controller
            ),
        )

    def add_type_submenu(self):
        """
        Adds a submenu for changing the component type.
        """
        menu = tk.Menu(self.__menu, tearoff=0)
        type_names = [
            type_spec.get_name() for type_spec in self.__component.get_types()
        ]
        for type_name in type_names:
            menu.add_command(
                label=type_name,
                command=lambda c_type=type_name: self.change_component_type(c_type),
            )
        self.__menu.add_cascade(label="Change component type", menu=menu)

    def add_chain_options(self):
        """
        Adds options for chain components to the menu.
        """
        menu = tk.Menu(self.__menu, tearoff=0)
        menu.add_command(
            label="Extend component", command=lambda: self.extend_component()
        )
        self.__menu.add_cascade(label="Component chain options...", menu=menu)

    def get_display_text(self):
        """
        Returns the display text of the associated component.

        Returns:
        - str: The display text.
        """
        return self.__component.get_display_text()

    def render(self, x, y):
        """
        Renders the frame at the specified coordinates.

        Args:
        - x: The x-coordinate.
        - y: The y-coordinate.

        Returns:
        - int: The required height of the frame.
        """
        display_text = self.get_display_text()
        self.__parent.create_window(x, y, anchor=tk.NW, window=self)
        self.__parent.update()
        if not display_text:
            return self.winfo_reqheight()
        label = tk.Message(self, font=("Arial", 10), text=display_text, width=500)
        label.grid(row=1, column=0, sticky=tk.W)
        self.__parent.update()
        return self.winfo_reqheight()