import pygame
from dataclasses import dataclass

@dataclass
class KeyBinding:
    left: int
    right: int 

PLAYER_TO_KEYS = {
    1: KeyBinding(pygame.K_LEFT, pygame.K_RIGHT),
    2: KeyBinding(pygame.K_a, pygame.K_d),
}

PLAYER_TO_COLOR = {
    1: pygame.Color("#ffae00"),
    2: pygame.Color("#00a2ff"),
}

def get_key_binding(player_number: int) -> KeyBinding:
    """
    Returns the input map for the given player number
    """
    return PLAYER_TO_KEYS[player_number]

def get_player_color(player_number: int) -> pygame.Color:
    return PLAYER_TO_COLOR[player_number]