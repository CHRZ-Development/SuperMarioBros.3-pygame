from typing import Protocol

from ..scene_manager import SceneManager


class Scene(Protocol):
    def __init__(self, surface):
        super().__init__()
        self.manager = SceneManager()
        self.surface = surface
        self.timer = .0

    def handle_event(self, event): ...
    def update(self, dt): ...
    def draw(self): ...
    def on_enter(self): ...
    def on_exit(self): ...
