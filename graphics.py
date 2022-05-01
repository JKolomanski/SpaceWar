import pygame
import json
global resolution


def get_resolution():
    global resolution
    with open("options.json", "r") as f:
        data = json.load(f)

    resolution = ['', '']
    resolution[0] = int(data['res_x'])
    resolution[1] = int(data['res_y'])
    return resolution


class GuiObject(pygame.sprite.Sprite):
    def __init__(self, type_of_object, type_of_button=None):
        super().__init__()

        if type_of_object == 'press_any_key':
            self.animation_index = 0
            press_any_key_0 = pygame.transform.scale(pygame.image.load('Graphics/press_any_key_0.png'), (200, 36))\
                .convert()
            press_any_key_1 = pygame.transform.scale(pygame.image.load('Graphics/press_any_key_1.png'), (200, 36))\
                .convert()
            self.animation_frames = [press_any_key_0, press_any_key_1]
            self.image = self.animation_frames[self.animation_index]
            self.rect = self.image.get_rect(midtop=(resolution[0] / 2, resolution[1] / 1.5))

        if type_of_object == 'logo':
            logo = pygame.transform.scale(pygame.image.load('Graphics/spacewar_logo.png'), (420, 300))\
                .convert()
            self.image = logo
            self.rect = self.image.get_rect(midtop=(resolution[0] / 2, resolution[1] / 24))

        if type_of_object == 'menu_button':
            if type_of_button == 'arcade':
                self.image = pygame.transform.scale(pygame.image.load('Graphics/arcade.png'), (196, 44))
                self.rect = self.image.get_rect(center=(resolution[0] / 2, resolution[1] / 1.6))

            if type_of_button == 'campaign':
                self.image = pygame.transform.scale(pygame.image.load('Graphics/campaign.png'), (236, 44))
                self.rect = self.image.get_rect(center=(resolution[0] / 2, resolution[1] / 1.6 + 53))

            if type_of_button == 'settings':
                self.image = pygame.transform.scale(pygame.image.load('Graphics/settings.png'), (148, 44))
                self.rect = self.image.get_rect(center=(resolution[0] / 2, resolution[1] / 1.6 + 106))

    def animate(self):
        self.animation_index += 0.03
        if self.animation_index >= len(self.animation_frames):
            self.animation_index = 0
        self.image = self.animation_frames[int(self.animation_index)]

    def update(self, type_of_object):
        if type_of_object == 'press_any_key':
            self.animate()
