import pygame
import json
from PIL import Image

global resolution


def get_resolution():
    global resolution
    with open("options.json", "r") as f:
        data = json.load(f)

    resolution = ['', '']
    resolution[0] = int(data['res_x'])
    resolution[1] = int(data['res_y'])
    return resolution


def pillow_to_pygame(pillow_image):
    return pygame.image.fromstring(
        pillow_image.tobytes(), pillow_image.size, pillow_image.mode).convert_alpha()


def pygame_to_pillow(pygame_surface):
    raw_str = pygame.image.tostring(pygame_surface, 'RGBA', False)
    return Image.frombytes('RGBA', pygame_surface.get_size(), raw_str)


# noinspection PyUnresolvedReferences,PyTypeChecker
class GuiObject(pygame.sprite.Sprite):
    def __init__(self, type_of_object, type_of_button=None):
        super().__init__()

        self.transparency = 0

        if type_of_object == 'press_any_key':
            self.size_x = 200
            self.size_y = 36
            self.image_file_0 = 'Assets/GUI/press_any_key_0.png'
            self.image_file_1 = 'Assets/GUI/press_any_key_1.png'
            self.animation_index = 0
            press_any_key_0 = pygame.transform.scale(pygame.image.load(self.image_file_0), (200, 36)).convert()
            press_any_key_1 = pygame.transform.scale(pygame.image.load(self.image_file_1), (200, 36)).convert()
            self.animation_frames = [press_any_key_0, press_any_key_1]
            self.image = self.animation_frames[self.animation_index]
            self.rect = self.image.get_rect(midtop=(resolution[0] / 2, resolution[1] / 1.5))

        if type_of_object == 'logo':
            self.size_x = 420
            self.size_y = 300
            self.image_file_0 = 'Assets/GUI/spacewar_logo.png'
            logo = pygame.transform.scale(pygame.image.load(self.image_file_0), (420, 300))\
                .convert_alpha()
            self.image = logo
            self.rect = self.image.get_rect(midtop=(resolution[0] / 2, resolution[1] / 24))

        if type_of_object == 'menu_button':
            self.animation_index = 0

            if type_of_button == 'arcade':
                self.size_x = 196
                self.size_y = 44
                self.image_file_0 = 'Assets/GUI/arcade.png'
                self.image_file_1 = 'Assets/GUI/arcade_02.png'
                arcade_1 = pygame.transform.scale(pygame.image.load(self.image_file_0).convert(), (196, 44))
                arcade_2 = pygame.transform.scale(pygame.image.load(self.image_file_1).convert(), (196, 44))

                self.animation_frames = [arcade_1, arcade_2]
                self.image = self.animation_frames[self.animation_index]
                self.rect = self.image.get_rect(center=(resolution[0] / 2, resolution[1] / 1.6))

            if type_of_button == 'campaign':
                self.size_x = 236
                self.size_y = 44
                self.image_file_0 = 'Assets/GUI/campaign.png'
                self.image_file_1 = 'Assets/GUI/campaign_02.png'
                campaign_1 = pygame.transform.scale(pygame.image.load(self.image_file_0).convert(), (236, 44))
                campaign_2 = pygame.transform.scale(pygame.image.load(self.image_file_1).convert(), (236, 44))

                self.animation_frames = [campaign_1, campaign_2]
                self.image = self.animation_frames[self.animation_index]
                self.rect = self.image.get_rect(center=(resolution[0] / 2, resolution[1] / 1.6 + 53))

            if type_of_button == 'settings':
                self.size_x = 148
                self.size_y = 44
                self.image_file_0 = 'Assets/GUI/settings.png'
                self.image_file_1 = 'Assets/GUI/settings_02.png'
                settings_1 = pygame.transform.scale(pygame.image.load(self.image_file_0)
                                                    .convert(), (148, 44))
                settings_2 = pygame.transform.scale(pygame.image.load(self.image_file_1)
                                                    .convert(), (148, 44))

                self.animation_frames = [settings_1, settings_2]
                self.image = self.animation_frames[self.animation_index]
                self.rect = self.image.get_rect(center=(resolution[0] / 2, resolution[1] / 1.6 + 106))

        if type_of_object == 'hint':
            self.size_x = 423
            self.size_y = 33
            self.image_file_0 = 'Assets/GUI/hint.png'
            self.image = pygame.transform.scale(pygame.image.load(self.image_file_0), (423, 33))
            self.rect = self.image.get_rect(bottomleft=(0, resolution[1]))

        if type_of_object == 'energy_frame':
            self.size_x = 264
            self.size_y = 44
            self.image_file_0 = 'Assets/GUI/energy_frame.png'
            self.image = pygame.transform.scale(pygame.image.load(self.image_file_0), (264, 44))
            self.rect = self.image.get_rect(topleft=(0, 0))

        if type_of_object == 'lives':

            self.size_x = 124
            self.size_y = 44
            self.image_file_0 = 'Assets/GUI/lives_3.png'
            self.animation_index = 3
            self.image = pygame.transform.scale(pygame.image.load(self.image_file_0), (124, 44))
            self.rect = self.image.get_rect(topleft=(264, 0))

        if type_of_object == 'score_frame':
            self.size_x = 184
            self.size_y = 44
            self.image_file_0 = 'Assets/GUI/score_frame.png'
            self.image = pygame.transform.scale(pygame.image.load(self.image_file_0), (184, 44))
            self.rect = self.image.get_rect(topleft=(388, 0))

        if type_of_object == 'game_over':
            self.size_x = 380
            self.size_y = 300
            self.image_file_0 = 'Assets/GUI/game_over.png'
            self.image = pygame.transform.scale(pygame.image.load(self.image_file_0), (380, 300))
            self.rect = self.image.get_rect(midtop=(resolution[0] / 2, resolution[1] / 24))

        if type_of_object == 'score_frame2':
            self.size_x = 184
            self.size_y = 44
            self.image_file_0 = 'Assets/GUI/score_frame.png'
            self.image = pygame.transform.scale(pygame.image.load(self.image_file_0), (184, 44))
            self.rect = self.image.get_rect(midtop=(resolution[0] / 2, resolution[1] / 1.85))

    def animate(self):
        self.animation_index += 0.03
        if self.animation_index >= len(self.animation_frames):
            self.animation_index = 0
        self.image = self.animation_frames[int(self.animation_index)]

    def update(self, type_of_object, type_of_button=None, index=None, do_fadeout=None, transparency=None):
        if type_of_object == 'press_any_key':
            self.animate()

        if type_of_button == 'arcade' and index == 0 or type_of_button == 'campaign' and index == 1 \
                or type_of_button == 'settings' and index == 2:
            self.animation_index = 0
            self.image = self.animation_frames[self.animation_index]

        elif type_of_object == 'menu_button':
            self.animation_index = 1
            self.image = self.animation_frames[self.animation_index]

        elif type_of_object == 'lives':
            if index == 3:
                self.image = pygame.transform.scale(pygame.image.load('Assets/GUI/lives_3.png'), (124, 44))

            if index == 2:
                self.image = pygame.transform.scale(pygame.image.load('Assets/GUI/lives_2.png'), (124, 44))

            if index == 1:
                self.image = pygame.transform.scale(pygame.image.load('Assets/GUI/lives_1.png'), (124, 44))

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
                                                (self.size_x, self.size_y)).convert_alpha()
