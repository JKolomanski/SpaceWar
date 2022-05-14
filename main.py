import random
import pygame
from sys import exit

from player import Player, PlayerCursor, LaserPlayer
from graphics import GuiObject, get_resolution
from meteorites import Meteorite

pygame.init()

# Screen, icon, display caption
get_resolution()
resolution = [get_resolution()[0], get_resolution()[1]]

screen = pygame.display.set_mode(resolution)
pygame.display.set_caption('SpaceWar!')
pygame.display.set_icon(pygame.image.load('Assets/Player/player1_01.png'))

# Randomise background
background_index = random.randint(1, 3)
if background_index == 1:
    menu_background = pygame.image.load('Assets/Backgrounds/background_earth.png').convert()
elif background_index == 2:
    menu_background = pygame.image.load('Assets/Backgrounds/background_moon.png').convert()
else:
    menu_background = pygame.image.load('Assets/Backgrounds/background_mars.png').convert()

# Sounds
choose_sound = pygame.mixer.Sound('Assets/Sounds/menu_choose.wav')
choose_sound.set_volume(0.5)

cursor_sound = pygame.mixer.Sound('Assets/Sounds/cursor_sound.wav')
cursor_sound.set_volume(0.1)

player_hit_sound = pygame.mixer.Sound('Assets/Sounds/player_hit.wav')
player_hit_sound.set_volume(0.8)

hit_sound = pygame.mixer.Sound('Assets/Sounds/hit.wav')
hit_sound.set_volume(0.2)

explosion_sound = pygame.mixer.Sound('Assets/Sounds/explosion.wav')
explosion_sound.set_volume(0.3)

# Variables
clock = pygame.time.Clock()
cursor_index = 0
gamemode = 0
# gamemode 0 = start menu
# gamemode 1 = main menu
# gamemode 2 = settings
# gamemode 3 = arcade mode
# gamemode 4 = campaign mode
# gamemode 5 = game over screen
deadzone = 5
meteorite_index = 0
score = 0
life = 3
invincibility_cooldown = 60

# Text
font = pygame.font.Font('Assets/Spacewarfont/spacewarfont.ttf', 20)
score_surf = font.render(str(score), False, 'White')
score_rect = score_surf.get_rect(topleft=(488, 12))

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

game_over = pygame.sprite.Group()
game_over.add(GuiObject(type_of_object='game_over'))

score_frame_2 = pygame.sprite.Group()
score_frame_2.add(GuiObject(type_of_object='score_frame2'))

energy_frame = pygame.sprite.Group()
energy_frame.add(GuiObject(type_of_object='energy_frame'))

lives = pygame.sprite.Group()
lives.add(GuiObject(type_of_object='lives'))

score_frame = pygame.sprite.Group()
score_frame.add(GuiObject(type_of_object='score_frame'))

cursor = pygame.sprite.Group()
cursor.add(PlayerCursor())

player = pygame.sprite.GroupSingle()
player.add(Player())

laser_player_group = pygame.sprite.Group()
laser_player_group.add(LaserPlayer(-50, -50, 0))

initial_meteorite = pygame.sprite.GroupSingle()
initial_meteorite.add(Meteorite(0))
meteorite_group = [initial_meteorite]

# Main loop
while True:
    if deadzone > 0:
        deadzone -= 1
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Start menu
        if gamemode == 0:
            if event.type == pygame.KEYDOWN and not deadzone:
                choose_sound.play()
                gamemode = 1
                deadzone = 5

        # Main menu
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

        # Game over screen
        if gamemode == 5:
            if event.type == pygame.KEYDOWN and not deadzone:
                choose_sound.play()
                gamemode = 1
                deadzone = 5

    # Start menu
    if gamemode == 0:
        screen.blit(menu_background, (0, 0))
        logo.draw(screen)
        press_any_key_button.draw(screen)
        press_any_key_button.update(type_of_object='press_any_key')

    # Main menu
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

    # Arcade mode
    elif gamemode == 3:
        screen.blit(menu_background, (0, 0))

        # Player shooting
        if player.sprite.shooting:
            player_x = player.sprite.x
            player_y = player.sprite.y
            player_angle = player.sprite.player_angle
            laser_player_group.add(LaserPlayer(x=player_x, y=player_y, angle=player_angle))

        laser_player_group.update()
        laser_player_group.draw(screen)

        # Displaying energy bar
        energy = player.sprite.energy / 2
        if energy < 0:
            energy = 0
        energy_frame.draw(screen)
        energy_bar = pygame.Surface((energy, 20))
        energy_bar.fill('#7FC9FF')
        screen.blit(energy_bar, (12, 12))

        # Displaying lives
        lives.update(type_of_object='lives', index=life)
        lives.draw(screen)

        # Displaying score
        score_frame.draw(screen)
        score_surf = font.render(f'{score}', False, 'White')
        screen.blit(score_surf, score_rect)

        # Meteorites
        for meteorite in meteorite_group:
            meteorite.update()
            if pygame.sprite.spritecollide(player.sprite, meteorite, False):
                if not invincibility_cooldown:
                    life -= 1
                    player_hit_sound.play()
                    invincibility_cooldown = 60

            elif pygame.sprite.groupcollide(laser_player_group, meteorite, True, False):

                # Small meteorites
                if meteorite.sprite.size == 1:
                    hit_sound.play()
                    score += 1
                    if len(meteorite_group) < 5:
                        meteorite_index = len(meteorite_group)
                        meteorite_group.append(str(meteorite_index))
                        meteorite_group[meteorite_index] = pygame.sprite.GroupSingle()
                        meteorite_group[meteorite_index].add(Meteorite(random.randint(0, 1)))

                    meteorite.sprite.kill()
                    del meteorite_group[meteorite_group.index(meteorite)]

                # Large meteorites
                elif meteorite.sprite.size == 0:
                    if meteorite.sprite.cracked:
                        explosion_sound.play()
                        meteorite_index = len(meteorite_group)
                        meteorite_group.append(str(meteorite_index))
                        meteorite_group[meteorite_index] = pygame.sprite.GroupSingle()
                        meteorite_group[meteorite_index]\
                            .add(Meteorite(1, True, meteorite.sprite.x, meteorite.sprite.y,
                                           meteorite.sprite.starting_angle - 180, meteorite.sprite.speed,
                                           meteorite.sprite.color))

                        meteorite_index = len(meteorite_group)
                        meteorite_group.append(str(meteorite_index))
                        meteorite_group[meteorite_index] = pygame.sprite.GroupSingle()
                        meteorite_group[meteorite_index]\
                            .add(Meteorite(1, True, meteorite.sprite.x, meteorite.sprite.y,
                                           meteorite.sprite.starting_angle - 60, meteorite.sprite.speed,
                                           meteorite.sprite.color))

                        meteorite_index = len(meteorite_group)
                        meteorite_group.append(str(meteorite_index))
                        meteorite_group[meteorite_index] = pygame.sprite.GroupSingle()
                        meteorite_group[meteorite_index]\
                            .add(Meteorite(1, True, meteorite.sprite.x, meteorite.sprite.y,
                                           meteorite.sprite.starting_angle - 300, meteorite.sprite.speed,
                                           meteorite.sprite.color))

                        score += 3
                        meteorite.sprite.kill()
                        del meteorite_group[meteorite_group.index(meteorite)]

                    elif not meteorite.sprite.cracked:
                        hit_sound.play()
                        meteorite.sprite.cracked = True

        # Separate for loop to prevent meteorites from flickering
        for meteorite in meteorite_group:
            meteorite.draw(screen)

        if invincibility_cooldown > 0:
            invincibility_cooldown -= 1

        if life < 1:
            gamemode = 5

        player.draw(screen)
        player.update()

    elif gamemode == 5:
        screen.blit(menu_background, (0, 0))

        game_over.draw(screen)

        press_any_key_button.draw(screen)
        press_any_key_button.update(type_of_object='press_any_key')

        score_frame_2.draw(screen)

        score_surf = font.render(f'{score}', False, 'White')
        screen.blit(score_surf, score_surf.get_rect(topleft=(resolution[0] / 2 + 8, resolution[1] / 1.85 + 12)))

    # Refresh screen
    pygame.display.update()
    clock.tick(60)
