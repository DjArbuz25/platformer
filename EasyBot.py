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

        super().__init__(position, animations_config, animation_speeds)
        self.speed = 2
        self.direction = 1
        self.attack_range = 50
        self.attack_cooldown = 1000
        self.last_attack_time = 0

    def ai_update(self, player):
        self.rect.x += self.direction * self.speed
        if self.rect.right > 700 or self.rect.left < 100:
            self.direction *= -1
            self.facing_right = not self.facing_right

        now = pygame.time.get_ticks()
        if abs(self.rect.centerx - player.rect.centerx) < self.attack_range:
            if now - self.last_attack_time > self.attack_cooldown:
                self.change_animation('attack')
                self.last_attack_time = now

update(self, player)
super().update()
self.ai_update(player)