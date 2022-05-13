import random

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

        self.max_energy = 480
        self.energy = self.max_energy
        self.energy_regen = 5
        self.max_energy_regen = self.energy_regen

        self.cooldown = 30
        self.shooting = False

        self.engine = False

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

    def going_forward(self):
        keys = pygame.key.get_pressed()

        # Going forward
        if keys[pygame.K_w] and self.energy > 0 and self.engine:
            self.engine = True
            self.player_animation_index += 0.3
            if self.player_animation_index >= len(self.animation_frames):
                self.player_animation_index = 0
            self.image = self.animation_frames[int(self.player_animation_index)]
            self.engine_angle = self.player_angle

            ax = math.cos(math.radians(self.engine_angle - 90))
            ay = -math.sin(math.radians(self.engine_angle - 90))

            self.dx += ax * 0.1
            self.dy += ay * 0.1

            self.energy -= 1

        elif not keys[pygame.K_w]:
            self.engine = True
            if self.energy < 480:
                self.energy += self.energy_regen
            self.image = self.player_off

        elif keys[pygame.K_w] and self.energy == 0 or keys[pygame.K_w] and not self.engine:
            self.engine = False
            self.energy += self.energy_regen
            self.image = self.player_off

        if self.energy > 480:
            self.energy = 480

    def turning(self):
        keys = pygame.key.get_pressed()

        # Turning left (counter-clockwise)
        if keys[pygame.K_a]:
            self.player_angle += 5

        # Turning right (clockwise)
        if keys[pygame.K_d]:
            self.player_angle -= 5

    def calculating_position(self):
        global resolution

        # For x axis
        if -self.max_speed < self.dx < self.max_speed or self.dx >= self.max_speed and (self.x + self.dx) < self.x or \
                self.dx <= -self.max_speed and (self.x + self.dx) > self.x:
            self.x += self.dx

        elif self.dx >= self.max_speed:
            self.x += self.max_speed
            self.dx = self.max_speed

        elif self.dx <= -self.max_speed:
            self.x += -self.max_speed
            self.dx = -self.max_speed

        # For y axis
        if -self.max_speed < self.dy < self.max_speed or self.dy >= self.max_speed and (self.y + self.dy) < self.y or \
                self.dy <= -self.max_speed and (self.y + self.dy) > self.y:
            self.y += self.dy

        elif self.dy >= self.max_speed:
            self.y += self.max_speed
            self.dy = self.max_speed

        elif self.dy <= -self.max_speed:
            self.y += -self.max_speed
            self.dy = -self.max_speed

        # Looping the screen
        if self.x > resolution[0] + 20:
            self.x = -20
        if self.x < -20:
            self.x = resolution[0] + 20
        if self.y > resolution[1] + 20:
            self.y = -20
        if self.y < -20:
            self.y = resolution[1] + 20

        # Rotate the player image
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
            if self.energy > 5:
                self.energy -= 5
            else:
                self.energy = 0
        else:
            self.shooting = False

        if self.cooldown == 0:
            self.energy_regen = self.max_energy_regen
        else:
            self.energy_regen = 0

    def update(self):
        self.shoot()
        self.going_forward()
        self.turning()
        self.calculating_position()


class LaserPlayer(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()

        self.x = x
        self.y = y
        self.angle = angle + random.randint(-5, 5)

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
                                                                    ('Assets/Player/laser_player_green.png'), (12, 28))
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
