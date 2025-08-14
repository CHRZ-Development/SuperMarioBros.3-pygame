"""
    "Fan Game" created by CHRZASZCZ Naulan.
        * Created the 26/09/2020 at 8:35am.
"""
import pygame as pg
import json
import yaml
import os

from pygame.locals import *

from src.scenes.animation_levels_scene import AnimationLevelsScene
from src.scenes.main_menu_scene import MainMenuScene
from src.scene_manager import SceneManager
from src.scenes.animation_main_menu_scene import AnimationMainMenuScene
from src.scenes.intro_scene import IntroScene
from src.scenes.scene_3 import Scene3
from src.maps_engine import Maps
from src.font import Font


class Main(object):
    def __init__(self):
        with open("config.yaml") as config_file:
            self.config = yaml.safe_load(config_file)

        pg.mixer.init(
            self.config["mixer"]["frequency"],
            self.config["mixer"]["size"],
            self.config["mixer"]["channels"],
            self.config["mixer"]["buffer"]
        )
        pg.init()
        pg.joystick.init()
        pg.font.init()

        self.window_size = (
            self.config["screen"]["width"],
            self.config["screen"]["height"]
        )
        self.screen = pg.display.set_mode(
            self.window_size,
            self.config["screen"]["flags"],
            self.config["screen"]["depth"]
        )
        self.display = pg.Surface((
            self.config["display"]["width"],
            self.config["display"]["height"]
        ))
        pg.mouse.set_visible(self.config["mouse"]["visible"])

        # Stock all Maps (Stages) in memory
        self.stage_list = {}
        self.t = 0

        # load all resources.
        print("-" * 3 + "= Loading resources =" + "-" * 11)
        with open(os.path.join("res", "pathIndex.json")) as f:
            pathIndex = json.load(f)
        self.res = {}
        for i in pathIndex:
            self.res[i] = {}
            for index in pathIndex[i]:
                if index != ":type":
                    directory = pathIndex[i][index][0]
                    file = pathIndex[i][index][1]
                    if pathIndex[i][":type"] == "image":
                        self.res[i][index] = self.load_img(os.path.join(directory, file))
                    elif pathIndex[i][":type"] == "music":
                        self.res[i][index] = pg.mixer.Sound(os.path.join(directory, file))
                    elif pathIndex[i][":type"] == "map":
                        with open(os.path.join(directory, file)) as f:
                            self.res[i][index] = json.load(f)
                    print(f"{pathIndex[i][index][1]} loaded !")
        print("-" * 3 + "= all resources loaded =" + "-" * 11 + "\n")

        with open("save.yaml") as save_file:
            self.save = yaml.safe_load(save_file)

        self.scene_manager = SceneManager()
        self.scene_manager.register("intro", IntroScene(self.display, self.res))
        self.scene_manager.register("animation_main_menu", AnimationMainMenuScene(self.display, self.res))
        self.scene_manager.register("main_menu", MainMenuScene(self.display, self.res))
        self.scene_manager.register("animation_levels", AnimationLevelsScene(self.display, self.res))
        self.scene_manager.register("enter_world", Scene3())
        
        if self.config["skipIntro"]:
            self.scene_manager.set_default_scene("animation_main_menu")
        else:
            self.scene_manager.set_default_scene("intro")

        self.font_custom = Font()
        self.maps = Maps()

    @staticmethod
    def load_img(directory, color_key=(255, 174, 201)):
        img = pg.image.load(directory).convert()
        img.set_colorkey(color_key)
        return img

    def run(self):
        clock = pg.time.Clock()
        while True:
            dt = clock.tick(self.config["framerateLimit"]) / 1000.
            
            self.scene_manager.handle_events(pg.event.get())
            self.screen.fill((0, 0, 0))
            self.scene_manager.draw()
            self.screen.blit(pg.transform.scale(self.display, self.window_size), (0, 0))
            
            self.scene_manager.update(dt)
            pg.display.update()


main = Main()
main.run()
