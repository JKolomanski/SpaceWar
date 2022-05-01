import pygame
# import time
from random import randint
from sys import exit

from player import Player, PlayerCursor
from graphics import GuiObject, get_resolution

pygame.init()

# Variables
get_resolution()
resolution = [get_resolution()[0], get_resolution()[1]]
clock = pygame.time.Clock()
cursor_index = 0
gamemode = 0
# gamemode 0 = start menu
# gamemode 1 = main menu
# gamemode 2 = arcade mode
# gamemode 3 = campaign mode

# screen, icon, display caption
screen = pygame.display.set_mode(resolution)
pygame.display.set_caption('SpaceWar! 0.1')
pygame.display.set_icon(pygame.image.load('Graphics/player1_01.png'))


# randomise background
background_index = randint(1, 3)
if background_index == 1:
    menu_background = pygame.image.load('Graphics/background_earth.png').convert()
elif background_index == 2:
    menu_background = pygame.image.load('Graphics/background_moon.png').convert()
else:
    menu_background = pygame.image.load('Graphics/background_mars.png').convert()

# assign classes
logo = pygame.sprite.Group()
logo.add(GuiObject(type_of_object='logo'))

press_any_key_button = pygame.sprite.Group()
press_any_key_button.add(GuiObject(type_of_object='press_any_key'))

arcade = pygame.sprite.Group()
arcade.add(GuiObject(type_of_object='menu_button', type_of_button='arcade'))

campaign = pygame.sprite.Group()
campaign.add(GuiObject(type_of_object='menu_button', type_of_button='campaign'))

settings = pygame.sprite.Group()
settings.add(GuiObject(type_of_object='menu_button', type_of_button='settings'))

player = pygame.sprite.GroupSingle()
player.add(Player())

cursor = pygame.sprite.Group()
cursor.add(PlayerCursor())

# Main loop
while True:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # start menu
        if gamemode == 0:
            if event.type == pygame.KEYDOWN:
                gamemode = 1

        # main menu
        if gamemode == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP and cursor_index > 0:
                    cursor_index -= 1
                if event.key == pygame.K_s or event.key == pygame.K_DOWN and cursor_index < 2:
                    cursor_index += 1
                if cursor_index == 0 and event.key == pygame.K_SPACE:
                    gamemode = 2

    # start menu
    if gamemode == 0:
        screen.blit(menu_background, (0, 0))
        logo.draw(screen)
        press_any_key_button.draw(screen)
        press_any_key_button.update('press_any_key')

    # main menu
    elif gamemode == 1:
        screen.blit(menu_background, (0, 0))
        logo.draw(screen)
        arcade.draw(screen)
        campaign.draw(screen)
        settings.draw(screen)
        cursor.draw(screen)
        cursor.update(index=cursor_index)

    # arcade mode
    elif gamemode == 2:
        screen.blit(menu_background, (0, 0))
        player.draw(screen)
        player.update()

    # refresh screen
    pygame.display.update()
    clock.tick(60)
