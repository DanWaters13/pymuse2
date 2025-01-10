from src.core.view import View
from src.core.button import Button
from pathlib import Path

class ComponentView(View):
    def __init__(self, canvas=None, config_path = Path("config")/"view.json"):
        super().__init__(canvas, config_path)

    def add_component(self, component: Button):
        self.add_child(component)
