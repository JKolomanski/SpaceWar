import pygame
# import time
from random import randint
from sys import exit

from player import Player, PlayerCursor, LaserPlayer
from graphics import GuiObject, get_resolution

pygame.init()


# screen, icon, display caption
get_resolution()
resolution = [get_resolution()[0], get_resolution()[1]]

screen = pygame.display.set_mode(resolution)
pygame.display.set_caption('SpaceWar!')
pygame.display.set_icon(pygame.image.load('Assets/Player/player1_01.png'))

# randomise background
background_index = randint(1, 3)
if background_index == 1:
    menu_background = pygame.image.load('Assets/Backgrounds/background_earth.png').convert()
elif background_index == 2:
    menu_background = pygame.image.load('Assets/Backgrounds/background_moon.png').convert()
else:
    menu_background = pygame.image.load('Assets/Backgrounds/background_mars.png').convert()

# sounds
choose_sound = pygame.mixer.Sound('Assets/Sounds/menu_choose.wav')
choose_sound.set_volume(0.5)

cursor_sound = pygame.mixer.Sound('Assets/Sounds/cursor_sound.wav')
cursor_sound.set_volume(0.2)

# Variables
clock = pygame.time.Clock()
cursor_index = 0
gamemode = 0
# gamemode 0 = start menu
# gamemode 1 = main menu
# gamemode 2 = settings
# gamemode 3 = arcade mode
# gamemode 4 = campaign mode
font = pygame.font.Font('Assets/Spacewarfont/spacewarfont.ttf', 25)
deadzone = 5

# Groups
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

hint = pygame.sprite.Group()
hint.add(GuiObject(type_of_object='hint'))

energy_frame = pygame.sprite.Group()
energy_frame.add(GuiObject(type_of_object='energy_frame'))

cursor = pygame.sprite.Group()
cursor.add(PlayerCursor())

player = pygame.sprite.GroupSingle()
player.add(Player())

laser_player_group = pygame.sprite.Group()
laser_player_group.add(LaserPlayer(-50, -50, 0))

# Main loop
while True:
    if deadzone > 0:
        deadzone -= 1
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # start menu
        if gamemode == 0:
            if event.type == pygame.KEYDOWN and not deadzone:
                choose_sound.play()
                gamemode = 1
                deadzone = 5

        # main menu
        if gamemode == 1:
            if event.type == pygame.KEYDOWN and not deadzone:
                if event.key == pygame.K_w and cursor_index > 0 or event.key == pygame.K_UP and cursor_index > 0:
                    cursor_index -= 1
                    cursor_sound.play()
                if event.key == pygame.K_s and cursor_index < 2 or event.key == pygame.K_DOWN and cursor_index < 2:
                    cursor_index += 1
                    cursor_sound.play()
                if cursor_index == 0 and event.key == pygame.K_SPACE:
                    gamemode = 3
                    choose_sound.play()
                deadzone = 5

    # start menu
    if gamemode == 0:
        screen.blit(menu_background, (0, 0))
        logo.draw(screen)
        press_any_key_button.draw(screen)
        press_any_key_button.update(type_of_object='press_any_key')

    # main menu
    elif gamemode == 1:
        screen.blit(menu_background, (0, 0))
        logo.draw(screen)
        hint.draw(screen)

        arcade.draw(screen)
        arcade.update(type_of_object='menu_button', type_of_button='arcade', index=cursor_index)
        campaign.draw(screen)
        campaign.update(type_of_object='menu_button', type_of_button='campaign', index=cursor_index)
        settings.draw(screen)
        settings.update(type_of_object='menu_button', type_of_button='settings', index=cursor_index)

        cursor.draw(screen)
        cursor.update(index=cursor_index)

    # arcade mode
    elif gamemode == 3:

        # player shooting
        if player.sprite.shooting:
            player_x = player.sprite.x
            player_y = player.sprite.y
            player_angle = player.sprite.player_angle
            laser_player_group.add(LaserPlayer(x=player_x, y=player_y, angle=player_angle))

        screen.blit(menu_background, (0, 0))

        energy = player.sprite.energy / 2
        if energy < 0:
            energy = 0
        energy_frame.draw(screen)
        energy_bar = pygame.Surface((energy, 20))
        energy_bar.fill('White')
        screen.blit(energy_bar, (12, 12))

        laser_player_group.update()
        laser_player_group.draw(screen)

        player.draw(screen)
        player.update()

    # refresh screen
    pygame.display.update()
    clock.tick(60)
