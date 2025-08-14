from enum import Enum, auto
from .scene import Scene


class AnimationState(Enum):
    FADE_IN = auto()
    PAUSE = auto()
    FADE_OUT = auto()
    DONE = auto()


class IntroScene(Scene):
    def __init__(self, surface, res):
        super().__init__(surface)
        self.background = res["annexe"]["introBG"]

    def on_enter(self):
        self.duration = {
            AnimationState.FADE_IN: 1.5,
            AnimationState.PAUSE: 3.,
            AnimationState.FADE_OUT: 1.5
        }

        self.state = AnimationState.FADE_IN
        self.alpha = 0

    def on_exit(self):
        pass

    def handle_event(self, event):
        pass

    def update(self, dt):
        self.timer += dt
        
        match self.state:
            case AnimationState.FADE_IN:
                self.alpha = min(255, self.alpha + (255 / self.duration[self.state]) * dt)
                if self.timer >= self.duration[self.state]:
                    self.alpha = 255
                    self.state = AnimationState.PAUSE
                    self.timer = 0
            case AnimationState.PAUSE:
                if self.timer >= self.duration[self.state]:
                    self.state = AnimationState.FADE_OUT
                    self.timer = 0
            case AnimationState.FADE_OUT:
                self.alpha = max(0, self.alpha - (255 / self.duration[self.state]) * dt)
                if self.timer >= self.duration[self.state]:
                    self.alpha = 0
                    self.state = AnimationState.DONE
                    self.timer = 0
            case AnimationState.DONE:
                self.manager.change_scene("animation_main_menu")

    def draw(self):
        self.surface.fill((0, 0, 0))
        self.background.set_alpha(int(self.alpha))
        self.surface.blit(self.background, (0, 0))
