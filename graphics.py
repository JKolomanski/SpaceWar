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
            press_any_key_0 = pygame.transform.scale(pygame.image.load('Graphics/GUI/press_any_key_0.png'), (200, 36))\
                .convert()
            press_any_key_1 = pygame.transform.scale(pygame.image.load('Graphics/GUI/press_any_key_1.png'), (200, 36))\
                .convert()
            self.animation_frames = [press_any_key_0, press_any_key_1]
            self.image = self.animation_frames[self.animation_index]
            self.rect = self.image.get_rect(midtop=(resolution[0] / 2, resolution[1] / 1.5))

        if type_of_object == 'logo':
            logo = pygame.transform.scale(pygame.image.load('Graphics/GUI/spacewar_logo.png'), (420, 300))\
                .convert()
            self.image = logo
            self.rect = self.image.get_rect(midtop=(resolution[0] / 2, resolution[1] / 24))

        if type_of_object == 'menu_button':
            self.animation_index = 0

            if type_of_button == 'arcade':
                arcade_1 = pygame.transform.scale(pygame.image.load('Graphics/GUI/arcade.png').convert(), (196, 44))
                arcade_2 = pygame.transform.scale(pygame.image.load('Graphics/GUI/arcade_02.png').convert(), (196, 44))

                self.animation_frames = [arcade_1, arcade_2]
                self.image = self.animation_frames[self.animation_index]
                self.rect = self.image.get_rect(center=(resolution[0] / 2, resolution[1] / 1.6))

            if type_of_button == 'campaign':
                campaign_1 = pygame.transform.scale(pygame.image.load('Graphics/GUI/campaign.png')
                                                    .convert(), (236, 44))
                campaign_2 = pygame.transform.scale(pygame.image.load('Graphics/GUI/campaign_02.png')
                                                    .convert(), (236, 44))

                self.animation_frames = [campaign_1, campaign_2]
                self.image = self.animation_frames[self.animation_index]
                self.rect = self.image.get_rect(center=(resolution[0] / 2, resolution[1] / 1.6 + 53))

            if type_of_button == 'settings':
                settings_1 = pygame.transform.scale(pygame.image.load('Graphics/GUI/settings.png')
                                                    .convert(), (148, 44))
                settings_2 = pygame.transform.scale(pygame.image.load('Graphics/GUI/settings_02.png')
                                                    .convert(), (148, 44))

                self.animation_frames = [settings_1, settings_2]
                self.image = self.animation_frames[self.animation_index]
                self.rect = self.image.get_rect(center=(resolution[0] / 2, resolution[1] / 1.6 + 106))

        if type_of_object == 'hint':
            self.image = pygame.transform.scale(pygame.image.load('Graphics/GUI/hint.png'), (423, 33))
            self.rect = self.image.get_rect(bottomleft=(0, resolution[1]))

    def animate(self):
        self.animation_index += 0.03
        if self.animation_index >= len(self.animation_frames):
            self.animation_index = 0
        self.image = self.animation_frames[int(self.animation_index)]

    def update(self, type_of_object, type_of_button=None, index=None):
        if type_of_object == 'press_any_key':
            self.animate()

        if type_of_button == 'arcade' and index == 0 or type_of_button == 'campaign' and index == 1 \
                or type_of_button == 'settings' and index == 2:
            self.animation_index = 0
            self.image = self.animation_frames[self.animation_index]
        elif type_of_object == 'menu_button':
            self.animation_index = 1
            self.image = self.animation_frames[self.animation_index]
