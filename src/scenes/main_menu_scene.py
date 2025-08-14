from math import sin
from pygame import SRCALPHA, Surface, KEYDOWN, K_a

from ..font import Font
from .scene import Scene


class MainMenuScene(Scene):
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
        return super().on_enter()

    def on_exit(self):
        return super().on_exit()

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_a:
                self.manager.change_scene("animation_levels")

    def update(self, dt):
        self.timer += dt

    def draw(self):
        w = self.surface.get_width()
        h = self.surface.get_height()

        self.surface.fill((255, 219, 161))
        self.surface.blit(self.curtain, (0, -171))
        self.surface.blit(self.cloud, (w / 3.5 - 22, (h / 4 - 12) + sin(self.timer / 2) * 5))
        self.surface.blit(self.small_cloud, (w / 3.5 + 185, (h / 4 + 22) + sin(self.timer / 2) * 3.5))
        self.surface.blit(self.small_cactus, (0, h - 101))
        self.surface.blit(self.cactus, (w - 63, h - 130))
        self.surface.blit(self.floor, (0, 203))
        self.surface.blit(self.title, (self.surface.get_width() / 2 - self.title.get_width() / 2, self.surface.get_height() / 2 - self.title.get_width() / 2))
        
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
