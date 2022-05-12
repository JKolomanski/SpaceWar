import pygame
import random
import math
from graphics import get_resolution

get_resolution()
resolution = [get_resolution()[0], get_resolution()[1]]


class Meteorite(pygame.sprite.Sprite):
    def __init__(self, size, child=None, x=None, y=None, angle=None):
        super().__init__()

        self.rotation_speed = random.randint(-100, 100) / 100

        if not child:
            self.angle = random.randint(-360, 360)
            self.starting_angle = self.angle

            self.x = random.randint(-70, resolution[0] + 70)
            if resolution[0] + 50 > self.x > -50:
                self.y = random.choice([
                    random.randint(-70, -50), random.randint(resolution[1] + 50, resolution[1] + 70)])
            else:
                self.y = random.randint(-70, resolution[1] + 70)

        else:
            self.angle = angle
            self.starting_angle = angle
            self.x = x
            self.y = y

        self.dx = 0
        self.dy = 0

        self.size = size

        # large meteorites
        if self.size == 0:
            self.image = pygame.transform.scale(pygame.transform.rotate(
                pygame.image.load('Assets/Meteorites/meteorite_large.png'), self.angle), (128, 128))

        # small meteorites
        if self.size == 1:
            self.image = pygame.transform.scale(pygame.transform.rotate(
                pygame.image.load('Assets/Meteorites/meteorite_small.png'), self.angle), (64, 64))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def calculate_position(self):
        ax = math.cos(math.radians(self.starting_angle - 90))
        ay = -math.sin(math.radians(self.starting_angle - 90))

        self.dx = ax * 3
        self.dy = ay * 3

        self.x += self.dx
        self.y += self.dy

        # looping the screen
        if self.x > resolution[0] + 70 or self.x < -70 or self.y > resolution[1] + 70 or self.y < -70:
            self.starting_angle = random.randint(0, 360)
            self.x = random.randint(-70, resolution[0] + 70)
            if resolution[0] + 60 > self.x > -60:
                self.y = random.choice([
                    random.randint(-70, -60), random.randint(resolution[1] + 60, resolution[1] + 70)])
            else:
                self.y = random.randint(-70, resolution[1] + 70)

    def update(self):
        self.angle += self.rotation_speed
        if self.size == 0:
            self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load
                                                                        ('Assets/Meteorites/meteorite_large.png'),
                                                                        (128, 128)).convert_alpha(), self.angle)

        if self.size == 1:
            self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load
                                                                        ('Assets/Meteorites/meteorite_small.png'),
                                                                        (64, 64)).convert_alpha(), self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.calculate_position()
