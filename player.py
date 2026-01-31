import pygame
from trail import Trail
from player_config import get_key_binding, get_player_color
import random

class Player:
    def __init__(self, player_id: int):

        self.player_id: int = player_id

        self.position = pygame.Vector2(0, 0)
        self.direction = pygame.Vector2(1, 0)
        self.speed = 100
        self.rotation_speed = 200
        self.color = get_player_color(player_id)
        self.trail = Trail(self.color)
        self.size = 5

        self._dt = 0.0
        self._has_spawned = False


    def handle_events(self, events: list[pygame.Event]):

        if self._has_spawned:
            self._handle_input()


    def update(self, dt):
        self._dt = dt

        self.position += self.direction * self.speed * dt

        self.trail.add_point(self.position.copy())

    def draw(self, canvas: pygame.Surface):

        if not self._has_spawned:
            return

        self.trail.draw(canvas, self.position)
        self._draw_player_head(canvas)
        
    def resize(self, new_size: tuple[int, int]):
        self.trail.resize(new_size)

    def spawn(self, position: pygame.Vector2):
        self.position = position

        # roter til en tilfeldig vinkel
        angle = random.uniform(0, 360)
        self.direction.rotate_ip(angle)

        self._has_spawned = True


    def _handle_input(self):

        keys = pygame.key.get_pressed()

        if keys[get_key_binding(self.player_id).left]:
            self._rotate_left()

        if keys[get_key_binding(self.player_id).right]:
            self._rotate_right()


    def _draw_player_head(self, canvas: pygame.Surface):

        pygame.draw.circle(canvas, self.color, (self.position.x, self.position.y), self.size)

        # Draw the player's direction
        end_x = self.position.x + self.direction[0] * self.size * 2
        end_y = self.position.y + self.direction[1] * self.size * 2
        pygame.draw.line(canvas, self.color, (self.position.x, self.position.y), (end_x, end_y), 2)


    def _rotate_right(self):
        self.direction.rotate_ip(self.rotation_speed * self._dt)
        self.direction = self.direction.normalize()
    
    def _rotate_left(self):
        self.direction.rotate_ip(-self.rotation_speed * self._dt)
        self.direction = self.direction.normalize()
