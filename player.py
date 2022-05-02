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

        # if self.player_level == 1:
        self.player_off = pygame.transform.scale(pygame.image.load('Graphics/player1_00.png'), (64, 64)).convert_alpha()
        player_on1 = pygame.transform.scale(pygame.image.load('Graphics/player1_01.png'), (64, 64)).convert_alpha()
        player_on2 = pygame.transform.scale(pygame.image.load('Graphics/player1_02.png'), (64, 64)).convert_alpha()
        player_on3 = pygame.transform.scale(pygame.image.load('Graphics/player1_03.png'), (64, 64)).convert_alpha()

        self.animation_frames = [player_on1, player_on2, player_on3]
        self.image = self.animation_frames[self.player_animation_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))

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

        elif not keys[pygame.K_w]:
            self.image = self.player_off

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

        # fun fact: this game is played on a torus (a.k.a a donut)!
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

    def update(self):
        self.going_forward()
        self.turning()
        self.calculating_position()


class PlayerCursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        global resolution

        self.x = resolution[0] / 2 - 160
        self.y = resolution[1] / 1.6

        player_on1 = pygame.transform.scale(pygame.image.load('Graphics/player1_01.png'), (64, 64)).convert_alpha()
        player_on2 = pygame.transform.scale(pygame.image.load('Graphics/player1_02.png'), (64, 64)).convert_alpha()
        player_on3 = pygame.transform.scale(pygame.image.load('Graphics/player1_03.png'), (64, 64)).convert_alpha()
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


class LaserPlayer(pygame.sprite.Sprite):
    def __int__(self):
        super().__init__()
