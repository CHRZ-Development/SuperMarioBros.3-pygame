from pygame.sprite import Sprite

from ..inputs.ressources import Ressources
from ..tile import Tile


class Player(Sprite):
    def __init__(self, group, vector):
        super().__init__(group)
        self.image = Ressources()["images"]["mario"].subsurface(
            (Tile.WIDTH, Tile.HEIGHT), (Tile.WIDTH, Tile.HEIGHT)
        )
        self.rect = self.image.get_rect(topleft=vector)
        self.rect.update(
            self.rect.left, self.rect.top, self.rect.width - 1, self.rect.height - 1
        )
        self.vector = vector

    def update(self, dt):
        self.rect.update(self.vector.x, self.vector.y, Tile.WIDTH - 1, Tile.HEIGHT - 1)
