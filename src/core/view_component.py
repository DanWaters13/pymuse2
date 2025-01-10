from src.core.view import View
from src.core.button import Button

class ComponentView(View):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)

    def add_component(self, component: Button):
        self.add_child(component)
