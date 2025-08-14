from pygame import KEYDOWN, K_a, QUIT, Vector2, Surface, SRCALPHA
from enum import Enum, auto
from math import sin

from .scene import Scene
from ..font import Font


class AnimationState(Enum):
    PAUSE = auto()
    CURTAIN_UP = auto()
    BACKGROUND_SHOW = auto()
    TITLE_ANIM = auto()
    PRESS_A = auto()
    DONE = auto()


class AnimationMainMenuScene(Scene):
    def __init__(self, surface, res):
        super().__init__(surface)
        self.font = Font()
        sheet = res["tiles"]["titleScreenSheet"]
        self.shadow_curtain = sheet.subsurface((257, 0), (256, 187))
        self.curtain = Surface((512, 187), SRCALPHA)
        self.curtain.blit(sheet.subsurface((0, 0), (256, 187)), (0, 0))
        self.curtain.blit(sheet.subsurface((0, 0), (256, 187)), (256, 0))
        self.floor = Surface((512, 37))
        self.floor.blit(sheet.subsurface((0, 188), (256, 37)), (0, 0))
        self.floor.blit(sheet.subsurface((0, 188), (256, 37)), (256, 0))
        self.small_cloud = sheet.subsurface((180, 285), (16, 8))
        self.cloud = sheet.subsurface((180, 268), (32, 16))
        self.small_cactus = sheet.subsurface((257, 188), (64, 64))
        self.cactus = sheet.subsurface((322, 188), (63, 93))
        self.title = Surface((179, 113), SRCALPHA)
        self.title.blit(sheet.subsurface((0, 226), (179, 72)), (0, 0))
        self.title.blit(sheet.subsurface((180, 226), (42, 41)), (self.title.get_width() / 2 - 20.5, 72))

    def on_enter(self):
        self.duration = {
            AnimationState.PAUSE: 1,
            AnimationState.CURTAIN_UP: 2,
            AnimationState.TITLE_ANIM: 1,
            AnimationState.BACKGROUND_SHOW: 0,
            AnimationState.PRESS_A: 0
        }

        self.state = AnimationState.PAUSE

        self.curtain_start_pos = Vector2(0, 0)
        self.curtain_end_pos = Vector2(0, -171)
        self.curtain_current_pos = self.curtain_start_pos.copy()

        self.title_start_pos = Vector2(self.surface.get_width() / 2 - self.title.get_width() / 2, -self.title.get_height())
        self.title_end_pos = Vector2(self.surface.get_width() / 2 - self.title.get_width() / 2, self.surface.get_height() / 2 - self.title.get_width() / 2)
        self.title_current_pos = self.title_start_pos.copy()

    def on_exit(self):
        pass

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_a:
                self.manager.change_scene("main_menu")

    def update(self, dt):
        self.timer += dt

        match self.state:
            case AnimationState.PAUSE:
                if self.timer >= self.duration[self.state]:
                    self.timer = 0
                    self.state = AnimationState.CURTAIN_UP
            case AnimationState.CURTAIN_UP:
                t = min(self.timer / self.duration[self.state], 1.)
                self.curtain_current_pos = self.curtain_start_pos.lerp(self.curtain_end_pos, t)
                if self.timer >= self.duration[self.state]:
                    self.timer = 0
                    self.state = AnimationState.BACKGROUND_SHOW
            case AnimationState.BACKGROUND_SHOW:
                if self.timer >= self.duration[self.state]:
                    self.timer = 0
                    self.state = AnimationState.TITLE_ANIM
            case AnimationState.TITLE_ANIM:
                t = min(self.timer / self.duration[self.state], 1.)
                self.title_current_pos = self.title_start_pos.lerp(self.title_end_pos, t)
                if self.timer >= self.duration[self.state]:
                    self.timer = 0
                    self.state = AnimationState.PRESS_A
            case AnimationState.PRESS_A:
                if self.timer >= self.duration[self.state]:
                    self.timer = 0
                    self.state = AnimationState.DONE
            case AnimationState.DONE:
                self.manager.change_scene("main_menu")

    def draw(self):
        w = self.surface.get_width()
        h = self.surface.get_height()

        if self.state not in [AnimationState.PAUSE, AnimationState.CURTAIN_UP]:
            self.surface.fill((255, 219, 161))
        else:
            self.surface.fill((0, 0, 0))    

        self.surface.blit(self.curtain, self.curtain_current_pos)

        if self.state not in [AnimationState.PAUSE, AnimationState.CURTAIN_UP]:
            self.surface.blit(self.cloud, (w / 3.5 - 22, (h / 4 - 12) + sin(self.timer / 2) * 5))
            self.surface.blit(self.small_cloud, (w / 3.5 + 185, (h / 4 + 22) + sin(self.timer / 2) * 3.5))
            self.surface.blit(self.small_cactus, (0, h - 101))
            self.surface.blit(self.cactus, (w - 63, h - 130))

        self.surface.blit(self.floor, (0, 203))

        if self.state != AnimationState.BACKGROUND_SHOW:
            self.surface.blit(self.title, self.title_current_pos)

        if self.state == AnimationState.PRESS_A:
            h_msg = h / 4 + 105
            w_msg = w / 2.6
            press_msg = {
                'P': [w_msg + sin(self.timer), h_msg],
                'R': [w_msg + sin(self.timer - 1) * 2 + 7, h_msg],
                'E': [w_msg + sin(self.timer - 2) * 2 + 7 * 2, h_msg],
                'S': [w_msg + sin(self.timer - 3) * 2 + 7 * 3, h_msg],
                'S_': [w_msg + sin(self.timer - 4) * 2 + 7 * 4, h_msg],
                'A': [w_msg + sin(self.timer - 5) * 2 + 7 * 5 + 5, h_msg],
                'T': [w_msg + sin(self.timer - 6) * 2 + 7 * 6 + 10, h_msg],
                'O': [w_msg + sin(self.timer - 7) * 2 + 7 * 7 + 10, h_msg],
                'S__': [w_msg + sin(self.timer - 8) * 2 + 7 * 8 + 15, h_msg],
                'T_': [w_msg + sin(self.timer - 9) * 2 + 7 * 9 + 15, h_msg],
                'A_': [w_msg + sin(self.timer - 10) * 2 + 7 * 10 + 15, h_msg],
                'R_': [w_msg + sin(self.timer - 11) * 2 + 7 * 11 + 15, h_msg],
                'T__': [w_msg + sin(self.timer - 12) * 2 + 7 * 12 + 15, h_msg],
            }

            for letter, pos in press_msg.items():
                clean_letter = letter.replace("_", "")
                self.font.draw_msg(self.surface, pos, clean_letter)
