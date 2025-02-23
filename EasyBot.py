from .bot import BaseCharacter
import pygame

class EasyBot(BaseCharacter):
    def __init__(self, position):
        animations_config = {
            'idle': {'path': 'assets/Idle.png', 'frames': 6},
            'walk': {'path': 'assets/Walk.png', 'frames': 8},
            'attack': {'path': 'assets/Attack_1.png', 'frames': 6}
        }

        animation_speeds = {
            'idle': 150,
            'walk': 100,
            'attack': 80
        }

        