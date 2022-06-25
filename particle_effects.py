import pygame
from PIL import Image
import random

from graphics import pillow_to_pygame


# noinspection PyUnresolvedReferences
class Sparks(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y
        self.lifetime = 256
        self.angle = 0
        self.rotation_speed = random.randint(1, 10)

        self.pillow_image = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
        self.image = pillow_to_pygame(self.pillow_image)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def spark(self):
        pixel = self.pillow_image.load()
        if self.lifetime <= 256:
            for row in range(self.pillow_image.size[0]):
                for column in range(self.pillow_image.size[1]):
                    if pixel[row, column] != (0, 0, 0, 0):
                        pixel[row, column] = (0, 0, 0, 0)
                    swap = random.randint(0, self.lifetime)
                    if swap == 0:
                        pixel[row, column] = (random.randint(190, 255), random.randint(100, 220), random.randint(0, 100), 256)
                        self.lifetime += 10

    def pygame_image(self):
        initial_image = pillow_to_pygame(self.pillow_image)
        self.image = pygame.transform.\
            rotate(pygame.transform.scale(initial_image, (64, 64)), self.angle + self.rotation_speed).convert_alpha()

        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.spark()
        self.pygame_image()
        if self.lifetime >= 256:
            self.image = pillow_to_pygame(Image.new('RGBA', (16, 16), (0, 0, 0, 0)))
