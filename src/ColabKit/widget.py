from IPython.display import display
import ipywidgets as widgets


def button(text, tip, style, func, *param) -> widgets.Button:
    button = widgets.Button(
        description=text, button_style=style, tooltip=tip, icon='erase')

    def on_button_click(b):
        func(*param)
    button.on_click(on_button_click)
    display(button)
    return button
