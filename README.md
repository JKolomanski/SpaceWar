# ![Alt text](Assets/GUI/spacewar_icon.png?raw=true "Title") SpaceWar!


## Overview
SpaceWar! is a simple asteroids-inspired game made in python.
This project was started by me to learn some basic python and programming in general

External libraries used: Pygame, Pillow, Pyinstaller


## Installation
The simplest way to run the game is to run the included .exe file

Please note: The .exe file may not always be up-to-date with the rest of the project

Alternatively you can just run main.py


## Controls

### In main menu:
Use 'W' and 'S' to move the cursor and SPACE to select

### During gameplay:
Use 'A' and 'D' to turn, 'W' to power the engine and SPACE to shoot


## Gameplay

### Arcade mode:
Shoot lasers to destroy meteorites to get points,
small meteorites add 1 point after being shot, bigger
meteorites require two hits to break, they add 3 points
and release 3 small meteorites when destroyed. 
Control your spaceship to avoid getting hit. Each hit takes
1 life, you have 3 lives before you lose the game.

### Campaign mode:
Not implemented yet


## ToDo list:

### Short-term:

- Highscore, display highscore on game-over screen
- Settings menu with the ability to change window size and reset highscore
- Add different player spaceship colors unlockable by achieving specific highscores

### Medium-term:

- Add the ability to change player color in setting menu
- PowerUps
- Weapon pickups
- Alien enemies

### Long-term (if ever):

- Campaign mode
- Fullscreen mode
- Ability to resize the game window freely in windowed mode
- AI which would play the game in arcade mode (so you don't have to)