import pygame
import math
from graphics import get_resolution

get_resolution()
resolution = [get_resolution()[0], get_resolution()[1]]


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global resolution

        self.x = resolution[0] / 2
        self.y = resolution[1] / 2
        self.dx = 0
        self.dy = 0

        self.player_angle = 180
        self.engine_angle = self.player_angle
        self.player_animation_index = 0
        self.max_speed = 6

        self.cooldown = 30
        self.shooting = False

        self.player_off = pygame.transform.scale(pygame.image.load('Assets/Player/player1_00.png'), (64, 64))\
            .convert_alpha()
        player_on1 = pygame.transform.scale(pygame.image.load('Assets/Player/player1_01.png'), (64, 64))\
            .convert_alpha()
        player_on2 = pygame.transform.scale(pygame.image.load('Assets/Player/player1_02.png'), (64, 64))\
            .convert_alpha()
        player_on3 = pygame.transform.scale(pygame.image.load('Assets/Player/player1_03.png'), (64, 64))\
            .convert_alpha()

        self.animation_frames = [player_on1, player_on2, player_on3]
        self.image = self.animation_frames[self.player_animation_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.shoot_sound = pygame.mixer.Sound('Assets/Sounds/shoot.wav')
        self.shoot_sound.set_volume(0.2)

        self.engine_sound = pygame.mixer.Sound('Assets/Sounds/engine_sound.wav')
        self.engine_sound.set_volume(0.2)
        self.engine_sound_delay = 0

    def going_forward(self):
        keys = pygame.key.get_pressed()

        # going forward
        if keys[pygame.K_w]:

            self.player_animation_index += 0.3
            if self.player_animation_index >= len(self.animation_frames):
                self.player_animation_index = 0
            self.image = self.animation_frames[int(self.player_animation_index)]
            self.engine_angle = self.player_angle

            ax = math.cos(math.radians(self.engine_angle - 90))
            ay = -math.sin(math.radians(self.engine_angle - 90))

            self.dx += ax * 0.1
            self.dy += ay * 0.1

            if not self.engine_sound_delay:
                self.engine_sound.play()
                self.engine_sound_delay = 292
            self.engine_sound_delay -= 1

        elif not keys[pygame.K_w]:
            self.image = self.player_off
            self.engine_sound.fadeout(400)
            self.engine_sound_delay = 0

    def turning(self):
        keys = pygame.key.get_pressed()

        # turning left (counter-clockwise)
        if keys[pygame.K_a]:
            self.player_angle += 5

        # turning right (clockwise)
        if keys[pygame.K_d]:
            self.player_angle -= 5

    def calculating_position(self):
        global resolution

        # for x axis
        if -self.max_speed < self.dx < self.max_speed or self.dx >= self.max_speed and (self.x + self.dx) < self.x or \
                self.dx <= -self.max_speed and (self.x + self.dx) > self.x:
            self.x += self.dx

        elif self.dx >= self.max_speed:
            self.x += self.max_speed
            self.dx = self.max_speed

        elif self.dx <= -self.max_speed:
            self.x += -self.max_speed
            self.dx = -self.max_speed

        # for y axis
        if -self.max_speed < self.dy < self.max_speed or self.dy >= self.max_speed and (self.y + self.dy) < self.y or \
                self.dy <= -self.max_speed and (self.y + self.dy) > self.y:
            self.y += self.dy

        elif self.dy >= self.max_speed:
            self.y += self.max_speed
            self.dy = self.max_speed

        elif self.dy <= -self.max_speed:
            self.y += -self.max_speed
            self.dy = -self.max_speed

        # looping the screen
        if self.x > resolution[0] + 20:
            self.x = -20
        if self.x < -20:
            self.x = resolution[0] + 20
        if self.y > resolution[1] + 20:
            self.y = -20
        if self.y < -20:
            self.y = resolution[1] + 20

        # rotate the player image
        self.image = pygame.transform.rotate(self.image, self.player_angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def shoot(self):
        keys = pygame.key.get_pressed()

        if self.cooldown:
            self.cooldown -= 1

        if keys[pygame.K_SPACE] and not self.cooldown:
            self.cooldown = 30
            self.shooting = True
            self.shoot_sound.play()
        else:
            self.shooting = False

    def update(self):
        self.going_forward()
        self.turning()
        self.calculating_position()
        self.shoot()


class LaserPlayer(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()

        self.x = x
        self.y = y
        self.angle = angle

        self.ax = math.cos(math.radians(self.angle - 90))
        self.ay = -math.sin(math.radians(self.angle - 90))

        self.dx = self.ax * 10
        self.dy = self.ay * 10

        self.x += self.dx
        self.y += self.dy

    def calculating_position(self):

        self.dx += self.ax * 0.8
        self.dy += self.ay * 0.8

        self.x += self.dx
        self.y += self.dy

        if self.x < -20 or self.x > resolution[0] + 20 or self.y < -20 or self.y > resolution[1] + 20:
            self.kill()

    def update(self):
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load
                                                                    ('Assets/Player/laser_player.png'), (12, 28))
                                             .convert_alpha(), self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.calculating_position()


class PlayerCursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        global resolution

        self.x = resolution[0] / 2 - 160
        self.y = resolution[1] / 1.6

        player_on1 = pygame.transform.scale(pygame.image.load('Assets/Player/player1_01.png'), (64, 64))\
            .convert_alpha()
        player_on2 = pygame.transform.scale(pygame.image.load('Assets/Player/player1_02.png'), (64, 64))\
            .convert_alpha()
        player_on3 = pygame.transform.scale(pygame.image.load('Assets/Player/player1_03.png'), (64, 64))\
            .convert_alpha()
        self.player_animation_index = 0
        self.animation_frames = [player_on1, player_on2, player_on3]

        self.image = pygame.transform.rotate(self.animation_frames[self.player_animation_index], 0.3)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, index):

        self.player_animation_index += 0.3
        if self.player_animation_index >= len(self.animation_frames):
            self.player_animation_index = 0
        self.image = self.animation_frames[int(self.player_animation_index)]

        if index == 0:
            self.y = resolution[1] / 1.6
        if index == 1:
            self.y = resolution[1] / 1.6 + 53
        if index == 2:
            self.y = resolution[1] / 1.6 + 106

        self.image = pygame.transform.rotate(self.animation_frames[int(self.player_animation_index)], 90)
        self.rect = self.image.get_rect(center=(self.x, self.y))
