import pygame
from tools import draw_polyline_aa

class Trail:

    def __init__(self, color: pygame.Color):

        self.color = color
        self.points: list[pygame.Vector2] = []

        # Trail is drawn on its own canvas. Copy the line to the main canvas
        self._canvas = pygame.Surface((2000, 2000), pygame.SRCALPHA)

    def add_point(self, point: pygame.Vector2, min_dist: float = 5):
        # Add if first
        if not self.points:
            self.points.append(point)
            return
        # Add only if the distance is large enough
        last_placed_point = self.points[-1]
        if point.distance_to(last_placed_point) >= min_dist:
            self.points.append(point)


    def draw(self, canvas: pygame.Surface, player_position: pygame.Vector2, width: int = 6):
        if not self.points:
            return

        # Draw only the last n points
        n = 4
        pts = self.points[-n:] + [player_position]
        draw_polyline_aa(self._canvas, self.color, pts, width)

        # Copy the short line segment to the main canvas
        canvas.blit(self._canvas, (0, 0))


    def resize(self, new_size: tuple[int, int]):
        new_canvas = pygame.Surface(new_size, pygame.SRCALPHA)
        new_canvas.blit(self._canvas, (0, 0))
        self._canvas = new_canvas




