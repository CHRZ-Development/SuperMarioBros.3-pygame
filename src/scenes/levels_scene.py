from enum import Enum, auto

import pygame

from ..entities.player import Player
from ..tile import Tile
from ..hud import HUD
from ..map_manager import MapManager
from ..inputs.ressources import Ressources
from .scene import Scene


class AnimationState(Enum):
    ENTER_WORLD = auto()
    DONE = auto()


class LevelsScene(Scene):
    duration = {
        AnimationState.ENTER_WORLD: 2
    }
    state = None

    def __init__(self):
        super().__init__()
        self.map_manager = MapManager()
        self.hud = HUD()

        self.sheet = Ressources()["images"]["levels"]
        self.hud_pos = pygame.Vector2(
            self.surface.get_width() / 2 - self.hud.get_width() / 2,
            self.surface.get_height() - self.hud.get_height(),
        )

    def on_enter(self):
        self.levels = pygame.Surface(
            (self.map_manager.current.width, self.map_manager.current.height)
        )
        self.levels_pos = pygame.Vector2(
            0, self.surface.get_height() / 2 - self.levels.get_height() / 2
        )

        self.enter_world_rect = pygame.Rect(0, 0, self.levels.width, self.levels.height)
        self.enter_world_rect_start_width = pygame.Vector2(0, 0)
        self.enter_world_rect_end_width = pygame.Vector2((self.levels.height / 2) / 16, 0)
        self.enter_world_rect_current_width = self.enter_world_rect_start_width.copy()

        for sprite in self.map_manager.current.sprites:
            # TODO: dirty code to find the start tile and level 1 tile
            if sprite.vector.x == Tile.WIDTH * 3 and sprite.vector.y == Tile.HEIGHT * 5:
                self.player_start_pos = sprite.vector
            if sprite.vector.x == Tile.WIDTH * 8 and sprite.vector.y == Tile.HEIGHT * 5:
                self.level_1_pos = sprite.vector
        self.player = Player(
            self.map_manager.current.sprites, self.player_start_pos.copy()
        )
        # TODO: dirty, move this code to player ?
        self.player_start_move_pos = self.player.vector.copy()
        self.player_end_move_pos = self.player.vector.copy()
        self.t = 1.0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # TODO: dirty, move this code to player ?
            if self.t == 1.0:
                self.timer = 0
                self.player_start_move_pos = self.player.vector.copy()
                if event.key == pygame.K_z:
                    self.player_end_move_pos = pygame.Vector2(
                        self.player.vector.x, self.player.vector.y - 16
                    )
                if event.key == pygame.K_q:
                    self.player_end_move_pos = pygame.Vector2(
                        self.player.vector.x - 16, self.player.vector.y
                    )
                if event.key == pygame.K_s:
                    self.player_end_move_pos = pygame.Vector2(
                        self.player.vector.x, self.player.vector.y + 16
                    )
                if event.key == pygame.K_d:
                    self.player_end_move_pos = pygame.Vector2(
                        self.player.vector.x + 16, self.player.vector.y
                    )
                if event.key == pygame.K_a:
                    if self.player.vector == self.level_1_pos:
                        self.state = AnimationState.ENTER_WORLD

    def update(self, dt):
        self.timer += dt

        match self.state:
            case None:
                self.map_manager.update(dt)
                # TODO: dirty, move this code to player ?
                collision = any(
                    self.player.rect.colliderect(tile.rect) and tile.collidable
                    for tile in self.map_manager.current.sprites
                    if tile != self.player
                )
                if collision:
                    self.player_end_move_pos = self.player_start_move_pos.copy()

                # TODO: dirty, move this code to player ?
                player_move_speed = 0.1
                self.t = min(self.timer / player_move_speed, 1.0)
                self.player.vector = self.player_start_move_pos.lerp(
                    self.player_end_move_pos, self.t
                )
            # TODO: Improve animation
            case AnimationState.ENTER_WORLD:
                t = min(self.timer / self.duration[self.state], 1.0)
                self.enter_world_rect_current_width = self.enter_world_rect_start_width.lerp(
                    self.enter_world_rect_end_width, t
                )
                if self.timer >= self.duration[self.state]:
                    self.timer = 0
                    self.state = AnimationState.DONE
            case AnimationState.DONE:
                if self.player.vector == self.level_1_pos:
                    self.manager.change_scene("level_1")

    def draw(self):
        self.surface.fill((0, 0, 0))
        self.map_manager.draw(self.levels)

        if self.state == AnimationState.ENTER_WORLD:
            pygame.draw.rect(self.levels, (0, 0, 0), self.enter_world_rect, int(self.enter_world_rect_current_width.x) * 16)
        self.surface.blit(self.levels, self.levels_pos)

        self.surface.blit(self.hud, self.hud_pos)
