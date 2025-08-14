from enum import Enum, auto
from pygame import Surface, Vector2

from ..font import Font

from .scene import Scene


class AnimationState(Enum):
    PAUSE = auto()
    HORIZONTAL_SHRINK = auto()
    STARS = auto()


class AnimationLevelsScene(Scene):
    def __init__(self, surface, res):
        super().__init__(surface)

        mario = res["entities"]["mario"].subsurface((16, 16), (16, 16))

        font = Font()
        self.stats = Surface((surface.get_width() / 2, surface.get_height() / 2))
        self.stats.fill((175, 232, 226))
        # TODO: improve font render
        font.draw_msg(self.stats, [self.stats.get_width() / 2, 0], "PUT LEVEL NAME")
        self.stats.blit(mario, (self.stats.get_width() - 16, self.stats.get_height() / 2))
        font.draw_msg(self.stats, [self.stats.get_width() / 2 + 32, self.stats.get_height() / 2], "PUT LIFES LEFT")
        font.draw_msg(self.stats, [50, self.stats.get_height() / 2], "MARIO")

    def on_enter(self):
        self.duration = {
            AnimationState.PAUSE: 3,
            AnimationState.HORIZONTAL_SHRINK: .1,
            AnimationState.STARS: 2
        }
        
        self.state = AnimationState.PAUSE
        
        self.stats_shrink_start_pos = Vector2(self.stats.get_width(), self.stats.get_height())
        self.stats_shrink_end_pos = Vector2(0, self.stats.get_height())
        self.stats_shrink_current_pos = self.stats_shrink_start_pos.copy()

    def on_exit(self):
        return super().on_exit()

    def handle_event(self, event):
        pass

    def update(self, dt):
        self.timer += dt
        
        match self.state:
            case AnimationState.PAUSE:
                if self.timer >= self.duration[self.state]:
                    self.timer = 0
                    self.state = AnimationState.HORIZONTAL_SHRINK
            case AnimationState.HORIZONTAL_SHRINK:
                t = min(self.timer / self.duration[self.state], 1.)
                self.stats_shrink_current_pos = self.stats_shrink_start_pos.lerp(self.stats_shrink_end_pos, t)
                if self.timer >= self.duration[self.state]:
                    self.timer = 0
                    self.state = AnimationState.STARS

    def draw(self):
        self.surface.fill((0, 0, 0))

        if self.state != AnimationState.STARS:
            self.surface.blit(self.stats.subsurface((0, 0), self.stats_shrink_current_pos), (self.surface.get_width() / 2 - self.stats.get_width() / 2, self.surface.get_height() / 2 - self.stats.get_height() / 2))
