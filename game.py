import pygame
from player import Player

class Game:
    def __init__(self):

        # Legg til 2 spillere by default
        self.players: list[Player] = []
        self.players.append(Player(player_id=1))
        self.players.append(Player(player_id=2))


        # Spawn spillere fra start (midlertidig for testing)
        self.players[0].spawn(position=pygame.Vector2(100, 100))
        self.players[1].spawn(position=pygame.Vector2(300, 300))


    def handle_events(self, events: list[pygame.Event]):

        for player in self.players:
            player.handle_events(events)

    def update(self, dt):

        for player in self.players:
            player.update(dt)

    def draw(self, canvas: pygame.Surface):

        for player in self.players:
            player.draw(canvas)

    def resize(self, new_size: tuple[int, int]):
        """Kalles når skjermstørrelsen er endret"""
        
        for player in self.players:
            player.resize(new_size)