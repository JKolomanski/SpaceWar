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
def define_image(color, size):
    # brown
    if color == 0:
        r_offset = 4
        g_offset = -2
        b_offset = -2
    # gray
    elif color == 1:
        r_offset = 0
        g_offset = 0
        b_offset = 0
    # blue
    else:
        r_offset = -4
        g_offset = -4
        b_offset = 4

    shape = random.randint(0, 100)
    if size == 0:
        if shape < 40:
            image_file = 'Assets/Meteorites/meteorite_large_1.png'
        elif shape < 80:
            image_file = 'Assets/Meteorites/meteorite_large_2.png'
        else:
            image_file = 'Assets/Meteorites/meteorite_large_3.png'
    else:
        if shape < 40:
            image_file = 'Assets/Meteorites/meteorite_small_1.png'
        elif shape < 80:
            image_file = 'Assets/Meteorites/meteorite_small_2.png'
        else:
            image_file = 'Assets/Meteorites/meteorite_small_3.png'

    image = pygame.image.load(image_file).convert_alpha()
    image = pygame_to_pillow(image)
    image.convert('RGBA')

    pixel = image.load()
    for row in range(image.size[0]):
        for column in range(image.size[1]):
            if pixel[row, column] != (0, 0, 0, 0):
                pixel[row, column] = (pixel[row, column][0] + r_offset, pixel[row, column][1] + g_offset,
                                      pixel[row, column][2] + b_offset, 256)
    return pillow_to_pygame(image)


# noinspection PyUnresolvedReferences
class Meteorite(pygame.sprite.Sprite):
    def __init__(self, size, child=None, x=None, y=None, angle=None, speed=None, color=None):
        super().__init__()

        self.rotation_speed = random.randint(-100, 100) / 100
        self.cracked = False

        # If the meteorite is not a child
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
            # color 0 = brown
            # color 1 = gray
            # color 2 = blue

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
            # brown
            if self.color == 0:
                self.original_image = define_image(0, 0)
            # gray
            if self.color == 1:
                self.original_image = define_image(1, 0)
            # blue
            if self.color == 2:
                self.original_image = define_image(2, 0)

        # Small meteorites
        if self.size == 1:
            # brown
            if self.color == 0:
                self.original_image = define_image(0, 1)
            # gray
            if self.color == 1:
                self.original_image = define_image(1, 1)
            # blue
            if self.color == 2:
                self.original_image = define_image(2, 1)

        self.image = self.original_image
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

    def update_image(self):
        # Large meteorites
        if self.size == 0:
            self.image = pygame.transform.rotate(pygame.transform.scale(self.original_image, (128, 128)), self.angle) \
                .convert_alpha()

        # Small meteorites
        elif self.size == 1:
            self.image = pygame.transform.rotate(pygame.transform.scale(self.original_image, (64, 64)), self.angle) \
                .convert_alpha()

    def update(self, do_fadeout=None, transparency=None, type_of_object=None):
        self.update_image()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.angle += self.rotation_speed
        self.calculate_position()
