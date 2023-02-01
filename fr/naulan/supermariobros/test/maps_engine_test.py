import os

from unittest import TestCase

from fr.naulan.supermariobros.src.entities.player import Player
from fr.naulan.supermariobros.src.maps.maps_generator import MapsGenerator


class MapsEngineTest(TestCase):
    def test_empty_map(self):
        """
            Test with full empty tiles
        """
        maps_generator = MapsGenerator()

        with open(os.getcwd() + "test/res/matrices/empty.txt", "r") as f:
            maps_generator.new(f.readlines(), f.name, False)
        self.assertTrue(len(maps_generator.data) == 1, "Have a map generated")

        empty_map = maps_generator.data[0]
        self.assertTrue(len(empty_map.data) == 0, "Is really empty")

    def test_player(self):
        """
            Test with only player on the map
        """
        maps_generator = MapsGenerator()

        with open(os.getcwd() + "test/res/matrices/player.txt", "r") as f:
            maps_generator.new(f.readlines(), f.name, False)
        self.assertTrue(len(maps_generator.data) == 1, "Have a map generated")

        player_map = maps_generator.data[0]
        self.assertTrue(len(player_map.data) == 1, "Have player into the list of entities")
        self.assertTrue(isinstance(player_map.player, Player), "Is really a player ?")

        player = player_map.player
        self.assertTrue(player.x == 4*16, "Generated at a good position on x axis")
        self.assertTrue(player.y == 16, "Generated at a good position on y axis")
