import random
import pygame
from sys import exit

from player import Player, PlayerCursor, LaserPlayer
from graphics import GuiObject, get_resolution
from meteorites import Meteorite


def fade(object_list, object_list2, switch_to, start_menu=None):
    global lives
    global fading
    global gamemode
    global gamemode_transition
    if start_menu:
        speed_of_transition = 10
    else:
        speed_of_transition = 40

    def do_fade(list_of_objects):
        if gamemode_transition < 256:
            for i in list_of_objects:
                i.update(type_of_object=str(i), do_fadeout=True, transparency=gamemode_transition)
        return list_of_objects

    if gamemode_transition < 256 and fading == 0:
        fading = 0
        gamemode_transition += speed_of_transition
        object_list = do_fade(list_of_objects=object_list)

    elif gamemode_transition >= 256:
        fading = 1
        gamemode_transition = 256

    elif gamemode_transition < 256 and fading == 1:
        if switch_to == 5:
            lives -= 1
        gamemode_transition -= 40
        object_list2 = do_fade(list_of_objects=object_list2)

    if gamemode_transition <= 0:
        fading = 0
        gamemode = switch_to
    return [object_list, object_list2]


def breakout(temp_meteorite_group, x, y, angle, speed, color):
    explosion_sound.play()
    temp_meteorite_index = len(temp_meteorite_group)
    temp_meteorite_group.append(str(temp_meteorite_index))
    temp_meteorite_group[temp_meteorite_index] = pygame.sprite.GroupSingle()
    temp_meteorite_group[temp_meteorite_index].add(Meteorite(1, True, x, y, angle - 180, speed, color))

    temp_meteorite_index = len(temp_meteorite_group)
    temp_meteorite_group.append(str(temp_meteorite_index))
    temp_meteorite_group[temp_meteorite_index] = pygame.sprite.GroupSingle()
    temp_meteorite_group[temp_meteorite_index].add(Meteorite(1, True, x, y, angle - 60, speed, color))

    temp_meteorite_index = len(temp_meteorite_group)
    temp_meteorite_group.append(str(temp_meteorite_index))
    temp_meteorite_group[temp_meteorite_index] = pygame.sprite.GroupSingle()
    temp_meteorite_group[temp_meteorite_index].add(Meteorite(1, True, x, y, angle - 300, speed, color))


pygame.init()

# Screen, icon, display caption
get_resolution()
resolution = [get_resolution()[0], get_resolution()[1]]

screen = pygame.display.set_mode(resolution)
pygame.display.set_caption('SpaceWar!')
pygame.display.set_icon(pygame.image.load('Assets/GUI/spacewar_icon.png'))

# Randomise background
background_index = random.randint(1, 4)
if background_index == 1:
    menu_background = pygame.image.load('Assets/Backgrounds/background_earth.png').convert()
elif background_index == 2:
    menu_background = pygame.image.load('Assets/Backgrounds/background_moon.png').convert()
elif background_index == 3:
    menu_background = pygame.image.load('Assets/Backgrounds/background_mars.png').convert()
else:
    menu_background = pygame.image.load('Assets/Backgrounds/background_nebula.png').convert()


# Sound effects
choose_sound = pygame.mixer.Sound('Assets/Sounds/menu_choose.wav')
choose_sound.set_volume(0.5)

cursor_sound = pygame.mixer.Sound('Assets/Sounds/cursor_sound.wav')
cursor_sound.set_volume(0.1)

player_hit_sound = pygame.mixer.Sound('Assets/Sounds/player_hit.wav')
player_hit_sound.set_volume(0.5)

player_explosion_sound = pygame.mixer.Sound('Assets/Sounds/player_explosion.wav')
player_explosion_sound.set_volume(0.5)

hit_sound = pygame.mixer.Sound('Assets/Sounds/hit.wav')
hit_sound.set_volume(0.2)

explosion_sound = pygame.mixer.Sound('Assets/Sounds/explosion.wav')
explosion_sound.set_volume(0.2)

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
gamemode_transition = 1
fading = 0
# 0 = Fading in
# 1 = Fading out
game_played = False
deadzone = 32
meteorite_index = 0
score = 0
lives = 3
invincibility_cooldown = 60

# Text and font
font = pygame.font.Font('Assets/Spacewarfont/spacewarfont.ttf', 20)
score_surf = font.render(str(score), False, 'White')
score_rect = score_surf.get_rect(topleft=(488, 12))

# Groups and classes
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

score_frame2 = pygame.sprite.Group()
score_frame2.add(GuiObject(type_of_object='score_frame2'))

energy_frame = pygame.sprite.Group()
energy_frame.add(GuiObject(type_of_object='energy_frame'))

lives_bar = pygame.sprite.Group()
lives_bar.add(GuiObject(type_of_object='lives'))

score_frame = pygame.sprite.Group()
score_frame.add(GuiObject(type_of_object='score_frame'))

cursor = pygame.sprite.GroupSingle()
cursor.add(PlayerCursor())

player = pygame.sprite.GroupSingle()
player.add(Player())

laser_player_group = pygame.sprite.Group()
laser_player_group.add(LaserPlayer(-50, -50, 0))

initial_meteorite = pygame.sprite.GroupSingle()
initial_meteorite.add(Meteorite(0, x=resolution[0] / 2, y=resolution[1] + 30, angle=180))
meteorite_group = [initial_meteorite]

GuiObject_list = [press_any_key_button, arcade, campaign, settings, hint]

GuiObject_list2 = [logo, press_any_key_button, arcade, campaign, settings, hint, cursor]

GuiObject_list3 = [press_any_key_button, arcade, campaign, settings, hint, cursor]

GuiObject_list4 = [player, lives_bar, score_frame, energy_frame] + meteorite_group

GuiObject_list5 = [game_over, press_any_key_button, score_frame2]

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
                gamemode_transition = 255
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
                    gamemode_transition = 255
                    choose_sound.play()
                deadzone = 5

        # Game over screen
        if gamemode == 5:
            if event.type == pygame.KEYDOWN and not deadzone:
                choose_sound.play()
                gamemode_transition = 255
                deadzone = 5

    # Main loop

    # Start menu
    if gamemode == 0:
        Object_list_temp = fade(object_list=GuiObject_list2, object_list2=GuiObject_list, switch_to=1, start_menu=True)
        GuiObject_list = Object_list_temp[1]
        GuiObject_list2 = Object_list_temp[0]

        screen.blit(menu_background, (0, 0))
        logo.draw(screen)
        press_any_key_button.draw(screen)
        press_any_key_button.update('press_any_key')

    # Main menu
    elif gamemode == 1:
        if not game_played:
            Object_list_temp = fade(object_list=GuiObject_list3, object_list2=GuiObject_list2, switch_to=3)
            GuiObject_list3 = Object_list_temp[0]
            GuiObject_list2 = Object_list_temp[1]
        else:
            Object_list_temp = fade(object_list=GuiObject_list2, object_list2=GuiObject_list2, switch_to=3)
            GuiObject_list = Object_list_temp[1]
            GuiObject_list2 = Object_list_temp[0]

        score = 0
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
        GuiObject_list4 = fade(object_list=GuiObject_list4, object_list2=GuiObject_list4, switch_to=5)[1]

        screen.blit(menu_background, (0, 0))

        # Player shooting
        if player.sprite.shooting:
            laser_player_group.add(LaserPlayer(x=player.sprite.x, y=player.sprite.y, angle=player.sprite.player_angle))

        laser_player_group.update()
        laser_player_group.draw(screen)

        # Displaying energy bar
        energy = player.sprite.energy / 2
        if energy < 0:
            energy = 0
        energy_frame.draw(screen)
        energy_bar = pygame.Surface((energy, 20))
        energy_bar.fill('#7FC9FF')
        if lives > 0:
            screen.blit(energy_bar, (12, 12))

        # Displaying lives
        lives_bar.update(type_of_object='lives', index=lives)
        lives_bar.draw(screen)

        # Displaying score
        score_frame.draw(screen)
        score_surf = font.render(f'{score}', False, 'White')
        if lives > 0:
            screen.blit(score_surf, score_rect)

        # Meteorites
        for meteorite in meteorite_group:
            meteorite.update()
            # Collide with player
            if pygame.sprite.spritecollide(player.sprite, meteorite, False):
                if not invincibility_cooldown:
                    lives -= 1
                    if lives > 0:
                        player_hit_sound.play()
                    else:
                        player_explosion_sound.play()
                    invincibility_cooldown = 60
                # Knockback
                player.sprite.dx += (player.sprite.x - meteorite.sprite.x) * 0.009
                player.sprite.dy += (player.sprite.y - meteorite.sprite.y) * 0.009

            # Collide with player_laser
            elif pygame.sprite.groupcollide(laser_player_group, meteorite, True, False):
                # Small meteorites
                if meteorite.sprite.size == 1:
                    hit_sound.play()
                    score += 1
                    meteorite.sprite.broken = True

                    if len(meteorite_group) < 5:
                        meteorite_index = len(meteorite_group)
                        meteorite_group.append(str(meteorite_index))
                        meteorite_group[meteorite_index] = pygame.sprite.GroupSingle()
                        meteorite_group[meteorite_index].add(Meteorite(random.randint(0, 1)))

                # Large meteorites
                elif meteorite.sprite.size == 0:
                    if meteorite.sprite.cracked:
                        breakout(meteorite_group, meteorite.sprite.x, meteorite.sprite.y,
                                 meteorite.sprite.starting_angle, meteorite.sprite.speed, meteorite.sprite.color)
                        score += 3
                        meteorite.sprite.broken = True

                    elif not meteorite.sprite.cracked:
                        hit_sound.play()
                        meteorite.sprite.cracked = True

            # Kill meteorites
            if meteorite.sprite.dead:
                meteorite.sprite.kill()
                del meteorite_group[meteorite_group.index(meteorite)]

        # Separate for loop to prevent meteorites from flickering
        for meteorite in meteorite_group:
            meteorite.draw(screen)

        if invincibility_cooldown > 0:
            invincibility_cooldown -= 1

        if lives == 0:
            gamemode_transition = 255

        player.draw(screen)
        player.update()

    # Game over screen
    elif gamemode == 5:
        GuiObject_list5 = fade(object_list=GuiObject_list5, object_list2=GuiObject_list5, switch_to=1)[1]

        game_played = True
        lives = 3
        initial_meteorite = pygame.sprite.GroupSingle()
        initial_meteorite.add(Meteorite(0, x=resolution[0] / 2, y=resolution[1] + 30, angle=180))
        meteorite_group = [initial_meteorite]
        cursor.sprite.__init__()
        player.sprite.__init__()
        laser_player_group.empty()
        screen.blit(menu_background, (0, 0))

        game_over.draw(screen)
        press_any_key_button.draw(screen)
        press_any_key_button.update(type_of_object='press_any_key')

        score_frame2.draw(screen)
        score_surf = font.render(f'{score}', False, 'White')
        if gamemode_transition == 256:
            screen.blit(score_surf, score_surf.get_rect(topleft=(resolution[0] / 2 + 8, resolution[1] / 1.85 + 12)))

    # Refresh screen
    pygame.display.update()
    clock.tick(60)
