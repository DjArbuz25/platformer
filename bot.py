import pygame
from pygame.math import Vector2

class BaseCharacter(pygame.sprite.Sprite):

    def __init__(self, position, animation_config, animation_speeds):
        super().__init__()
        self.animations = {}
        self.animation_speeds = animation_speeds
        self.load_animations(animation_config)


        self.current_animation = 'idle'
        self.animaton_frame = 0
        self.last_update = pygame.time.get_ticks()


        self.image = self.animations[self.current_animation]['frames'][0]
        self.rect = self.image.get_rect(topleft=position)
        self.velocity = Vector2(0, 0)
        self.facing_right = True
        self.on_ground = True
        self.is_attacking = False

        def load_animations(self, config):
            for anim_name, params in config.items():
                frames = self.load_spritesheet(
                    params['path'],
                    params['frames'],
                    params.get('flip', False)
                )

                self.animations[anim_name] = {
                    'frames': frames,
                    'speed': self.animations_speeds.get(anim_name, 100)
                }

        def load_spritesheet(self, filename, frames, flip=False):
            spritesheet = pygame.image.load(filename).convert_alpha()
            frame_width = spritesheet.get_width() // frames
            frame_height = spritesheet.get_height()

            sprites = []
            for i in range(frames):
                frame = spritesheet.subsurface(pygame.Rect(
                    i * frame_width, 0, frame_width, frame_height
                ))
                if flip:
                    frame = pygame.transform.flip(frame, True, False)
                sprites.append(frame)
            return sprites

        def change_animation(self,new_animation):
            if self.current_animation != new_animation:
                self.current_animation = new_animation
                self.animation_frame = 0
                self.last_update = pygame.time.get_ticks()

        def update_animation(self):
            now = pygame.time.get_ticks()
            anim_data = self.animations[self.current_animation]

            if now - self.last_update > anim_data['speed']:
                self.last_update = now
                self.animation_frame = (self.animation_frame + 1) % len(anim_data['frames'])
                self.image = anim_data['frames'][self.animation_frame]

                if not self.facing_right:
                    self.image = pygame.transform.flip(self.image, True, False)

        def apply_physics(self, gravity=0.8, ground_level=600):
            self.velocity.y += gravity
            self.rect.y += self.velocity.y

            if self.rect.bottom >= ground_level:
                self.rect.bottom = ground_level
                self.velocity.y = 0
                self.on_ground = True

        def update(self):
            self.update_animation()
            self.apply_physics()
