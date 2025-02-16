import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (50, 205, 50)
BLACK = (0, 0, 0)

hp_font = pygame.font.Font(None, 36)
font = pygame.font.Font(None, 36)

MENU = 0
GAME = 1


# Инициализация окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sprite Animation with Jump and Attack")
clock = pygame.time.Clock()

background = pygame.image.load("backgroundC.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

class Button:
    def __init__(self, text, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = ORANGE
        self.text_color = WHITE

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


# Класс для анимации
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.hp = 100

        self.animation_speeds = {
            'idle': 0.1,
            'walk_right': 0.15,
            'walk_left': 0.15,
            'jump_right': 0.75,
            'jump_left': 0.75,
            'attack_right': 0.85,
            'attack_left': 0.85
        }
        # Загружаем спрайты для анимаций
        self.spritesheets = {
            'idle': self.load_spritesheet('Idle.png', 6),
            'walk_right': self.load_spritesheet('Walk.png', 8),
            'walk_left': self.load_spritesheet('Walk.png', 8, flip=True),
            'jump_right': self.load_spritesheet('Jump.png', 10),  # Анимация прыжка вправо
            'jump_left': self.load_spritesheet('Jump.png', 10, flip=True),  # Анимация прыжка влево
            'attack_right': self.load_spritesheet('Attack_1.png', 4),  # Анимация атаки вправо
            'attack_left': self.load_spritesheet('Attack_1.png', 4, flip=True),  # Анимация атаки влево
        }
        self.current_animation = 'idle'
        self.sprites = self.spritesheets[self.current_animation]
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft=position)
        self.animation_speed = self.animation_speeds[self.current_animation]
        self.last_update = pygame.time.get_ticks()

        # Физика прыжка
        self.jump_speed = -15  # Начальная скорость прыжка
        self.gravity = 0.8  # Гравитация
        self.velocity_y = 0  # Текущая вертикальная скорость
        self.on_ground = True  # Находится ли персонаж на земле
        self.jump_height = self.rect.height * 1.5  # Высота прыжка (1.5x от роста)

        # Атака
        self.is_attacking = False  # Флаг атаки
        self.attack_cooldown = 100  # Время перезарядки атаки (в миллисекундах)
        self.last_attack_time = 0  # Время последней атаки

    def load_spritesheet(self, filename, frames, flip=False):
        spritesheet = pygame.image.load(filename).convert_alpha()
        frame_width = spritesheet.get_width() // frames
        frame_height = spritesheet.get_height()
        sprites = []
        for i in range(frames):
            frame = spritesheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            if flip:  # Если нужно отразить спрайт
                frame = pygame.transform.flip(frame, True, False)
            sprites.append(frame)
        return sprites

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:  # Обновление кадра каждые 100 мс
            self.last_update = now
            self.current_sprite += self.animation_speed
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                if self.is_attacking:  # Если атака завершена
                    self.is_attacking = False
                    self.change_animation('idle')  # Возвращаемся к idle после атаки
            self.image = self.sprites[int(self.current_sprite)]

        # Применяем гравитацию
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Ограничение на падение (земля)
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity_y = 0
            self.on_ground = True

    def jump(self, direction):
        if self.on_ground:  # Прыжок возможен только с земли
            self.velocity_y = self.jump_speed
            self.on_ground = False
            # Выбор анимации прыжка в зависимости от направления
            if direction == 'right':
                self.change_animation('jump_right')
            elif direction == 'left':
                self.change_animation('jump_left')

    def attack(self):
        now = pygame.time.get_ticks()
        if now - self.last_attack_time > self.attack_cooldown:  # Проверка перезарядки
            self.last_attack_time = now
            self.is_attacking = True
            # Выбор анимации атаки в зависимости от направления
            if self.current_animation == 'walk_right' or self.current_animation == 'idle':
                self.change_animation('attack_right')
            elif self.current_animation == 'walk_left':
                self.change_animation('attack_left')

    def change_animation(self, animation):
        if self.current_animation != animation:
            self.current_animation = animation
            self.sprites = self.spritesheets[self.current_animation]
            self.current_sprite = 0
            self.animation_speed = self.animation_speeds[animation]

def main_menu():
    play_button = Button("ИГРАТЬ", WIDTH//2 - 100, HEIGHT//2 - 60, 200, 50)
    level_button = Button("УРОВНИ", WIDTH//2 - 100, HEIGHT//2 + 10, 200, 50)  #WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 50
    exit_button = Button("ВЫЙТИ", WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 50) # WIDTH//2 - 100, HEIGHT//2 + 10, 200, 50

    while True:
        screen.fill(BLACK)
        play_button.draw(screen)
        level_button.draw(screen)
        exit_button.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.rect.collidepoint(event.pos):
                    return GAME
                elif exit_button.rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEMOTION:
                if play_button.rect.collidepoint(event.pos):
                    play_button.color = (255, 140, 0)
                else:
                    play_button.color = ORANGE

                if exit_button.rect.collidepoint(event.pos):
                    exit_button.color = (255, 140, 0)
                else:
                    exit_button.color = ORANGE

                    if level_button.rect.collidepoint(event.pos):
                        level_button.color = (255, 140, 0)
                    else:
                        level_button.color = ORANGE
        clock.tick(FPS)

# Создание персонажа
player = AnimatedSprite((100, HEIGHT - 150))  # Стартовая позиция на "земле"
all_sprites = pygame.sprite.Group(player)

# Основной цикл игры
current_state = MENU
running = True

while running:
    if current_state == MENU:
        current_state = main_menu()

    elif current_state == GAME:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Прыжок по нажатию пробела
                    if player.current_animation == 'walk_right' or player.current_animation == 'idle':
                        player.jump('right')
                    elif player.current_animation == 'walk_left':
                        player.jump('left')
                if event.key == pygame.K_f:  # Атака по нажатию клавиши 'F'
                    player.attack()

    # Управление персонажем
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        if not player.is_attacking:  # Если не атакуем, можно двигаться
            player.change_animation('walk_right')
            player.rect.x += 5
    elif keys[pygame.K_a]:
        if not player.is_attacking:  # Если не атакуем, можно двигаться
            player.change_animation('walk_left')
            player.rect.x -= 5
    else:
        if player.on_ground and not player.is_attacking:  # Если на земле и не атакуем, то idle
            player.change_animation('idle')

    # Ограничение перемещения по горизонтали
    if player.rect.left < 0:
        player.rect.left = 0
    if player.rect.right > WIDTH:
        player.rect.right = WIDTH

    # Обновление и отрисовка,
    screen.blit(background, (0, 0))
    all_sprites.update()
    all_sprites.draw(screen)


    hp_text = hp_font.render(f"HP: {player.hp}%", True, RED)
    screen.blit(hp_text, (WIDTH-250, 10))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
