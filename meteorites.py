import pygame
import random
import math
from PIL import Image
from graphics import get_resolution

get_resolution()
resolution = [get_resolution()[0], get_resolution()[1]]


def pillow_to_pygame(pillow_image):
    return pygame.image.fromstring(
        pillow_image.tobytes(), pillow_image.size, pillow_image.mode).convert_alpha()


def pygame_to_pillow(pygame_surface):
    raw_str = pygame.image.tostring(pygame_surface, 'RGBA', False)
    return Image.frombytes('RGBA', pygame_surface.get_size(), raw_str)


# noinspection PyUnresolvedReferences
class Meteorite(pygame.sprite.Sprite):
    def __init__(self, size, child=None, x=None, y=None, angle=None, speed=None, color=None):
        super().__init__()

        self.transparency = 0
        self.rotation_speed = random.randint(-100, 100) / 100

        if not child:
            # Initial meteorite
            if angle:
                self.angle = angle
                self.x = x
                self.y = y
                self.speed = 1.5
            # All other meteorites
            else:
                self.speed = round(random.uniform(1, 3.5), 1)
                self.angle = random.randint(-360, 360)
                self.x = random.randint(-70, resolution[0] + 70)
                if resolution[0] + 50 > self.x > -50:
                    self.y = random.choice([
                        random.randint(-70, -50), random.randint(resolution[1] + 50, resolution[1] + 70)])
                else:
                    self.y = random.randint(-70, resolution[1] + 70)

            self.starting_angle = self.angle
            self.color = random.randint(0, 2)

        # If the meteorite is a child
        else:
            self.angle = angle
            self.starting_angle = angle
            self.x = x
            self.y = y
            self.speed = speed
            self.color = color

        self.dx = 0
        self.dy = 0

        self.size = size

        # Large meteorites
        if self.size == 0:
            self.cracked = False
            if self.color == 0:
                self.image = pygame.transform.scale(pygame.transform.rotate(
                    pygame.image.load('Assets/Meteorites/meteorite_large_brown.png'), self.angle), (128, 128))
            if self.color == 1:
                self.image = pygame.transform.scale(pygame.transform.rotate(
                    pygame.image.load('Assets/Meteorites/meteorite_large_gray.png'), self.angle), (128, 128))
            if self.color == 2:
                self.image = pygame.transform.scale(pygame.transform.rotate(
                    pygame.image.load('Assets/Meteorites/meteorite_large_blue.png'), self.angle), (128, 128))

        # Small meteorites
        if self.size == 1:
            if self.color == 0:
                self.image = pygame.transform.scale(pygame.transform.rotate(
                    pygame.image.load('Assets/Meteorites/meteorite_small_brown.png'), self.angle), (64, 64))
            if self.color == 1:
                self.image = pygame.transform.scale(pygame.transform.rotate(
                    pygame.image.load('Assets/Meteorites/meteorite_small_gray.png'), self.angle), (64, 64))
            if self.color == 2:
                self.image = pygame.transform.scale(pygame.transform.rotate(
                    pygame.image.load('Assets/Meteorites/meteorite_small_blue.png'), self.angle), (64, 64))

        self.rect = self.image.get_rect(center=(self.x, self.y))

    def calculate_position(self):
        ax = math.cos(math.radians(self.starting_angle - 90))
        ay = -math.sin(math.radians(self.starting_angle - 90))

        self.dx = ax * self.speed
        self.dy = ay * self.speed

        self.x += self.dx
        self.y += self.dy

        # Looping the screen
        if self.x > resolution[0] + 70 or self.x < -70 or self.y > resolution[1] + 70 or self.y < -70:
            self.starting_angle = random.randint(0, 360)
            self.x = random.randint(-70, resolution[0] + 70)
            if resolution[0] + 60 > self.x > -60:
                self.y = random.choice([
                    random.randint(-70, -60), random.randint(resolution[1] + 60, resolution[1] + 70)])
            else:
                self.y = random.randint(-70, resolution[1] + 70)

    def update(self, do_fadeout=None, transparency=None, type_of_object=None):
        self.angle += self.rotation_speed

        # Large meteorites
        if self.size == 0:
            if self.color == 0:
                if not self.cracked:
                    self.image = pygame.transform.rotate(pygame.transform.scale
                                                         (pygame.image.load('Assets/Meteorites/meteorite_large_brown'
                                                                            '.png'),
                                                          (128, 128)).convert_alpha(), self.angle)
                if self.cracked:
                    self.image = pygame.transform.rotate(pygame.transform.scale
                                                         (pygame.image.load('Assets/Meteorites'
                                                                            '/meteorite_large_brown_cracked.png'),
                                                          (128, 128)).convert_alpha(), self.angle)

            if self.color == 1:
                if not self.cracked:
                    self.image = pygame.transform.rotate(pygame.transform.scale
                                                         (pygame.image.load('Assets/Meteorites/meteorite_large_gray'
                                                                            '.png'),
                                                          (128, 128)).convert_alpha(), self.angle)
                if self.cracked:
                    self.image = pygame.transform.rotate(pygame.transform.scale
                                                         (pygame.image.load('Assets/Meteorites'
                                                                            '/meteorite_large_gray_cracked.png'),
                                                          (128, 128)).convert_alpha(), self.angle)

            if self.color == 2:
                if not self.cracked:
                    self.image = pygame.transform.rotate(pygame.transform.scale
                                                         (pygame.image.load('Assets/Meteorites/meteorite_large_blue'
                                                                            '.png'),
                                                          (128, 128)).convert_alpha(), self.angle)
                if self.cracked:
                    self.image = pygame.transform.rotate(pygame.transform.scale
                                                         (pygame.image.load('Assets/Meteorites'
                                                                            '/meteorite_large_blue_cracked.png'),
                                                          (128, 128)).convert_alpha(), self.angle)

        # Small meteorites
        if self.size == 1:
            if self.color == 0:
                self.image = pygame.transform.rotate(pygame.transform.scale
                                                     (pygame.image.load('Assets/Meteorites/meteorite_small_brown.png'),
                                                      (64, 64)).convert_alpha(), self.angle)
            if self.color == 1:
                self.image = pygame.transform.rotate(pygame.transform.scale
                                                     (pygame.image.load('Assets/Meteorites/meteorite_small_gray.png'),
                                                      (64, 64)).convert_alpha(), self.angle)
            if self.color == 2:
                self.image = pygame.transform.rotate(pygame.transform.scale
                                                     (pygame.image.load('Assets/Meteorites/meteorite_small_blue.png'),
                                                      (64, 64)).convert_alpha(), self.angle)

        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.calculate_position()

        if do_fadeout:
            self.transparency = transparency
            image = pygame_to_pillow(self.image)

            pixel = image.load()
            for row in range(image.size[0]):
                for column in range(image.size[1]):
                    if pixel[row, column] != (0, 0, 0, 0):
                        pixel[row, column] = (pixel[row, column][0], pixel[row, column][1],
                                              pixel[row, column][2], self.transparency)

            self.image = pygame.transform.scale(pillow_to_pygame(image),
                                                (64, 64)).convert_alpha()
