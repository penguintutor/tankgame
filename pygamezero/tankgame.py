import math
import random
import pygame
from tank import Tank
from shell import Shell
from land import Land

WIDTH=800
HEIGHT=600

# States are:
# start - timed delay before start
# player1 - waiting for player to set position
# player1fire - player 1 fired
# player2 - player 2 set position
# player2fire - player 2 fired
# game_over_1 / game_over_2 - show who won 1 = player 1 won etc.
game_state = "player1"

# Colour constants
SKY_COLOR = (165, 182, 209)
SKY_COLOR = (165, 182, 209)
GROUND_COLOR = (9,84,5)
# Different tank colors for player 1 and player 2
# These colors must be unique as well as the GROUND_COLOR
TANK_COLOR_P1 = (216, 216, 153)
TANK_COLOR_P2 = (219, 163, 82)
SHELL_COLOR = (255,255,255)
TEXT_COLOR = (255,255,255)

# Timer used to create delays before action (prevent accidental button press)
game_timer = 0

# Tank 1 = Left
tank1 = Tank("left", TANK_COLOR_P1)
# Tank 2 = Right
tank2 = Tank("right", TANK_COLOR_P2)

# Only fire one shell at a time, a single shell object can be used for both player 1 and player 2
shell = Shell(SHELL_COLOR)

ground = Land(GROUND_COLOR, (WIDTH, HEIGHT))


tank1.set_position(ground.get_tank1_position())
tank2.set_position(ground.get_tank2_position())


def draw():
    global game_state
    screen.fill(SKY_COLOR)
    ground.draw(screen)
    tank1.draw (screen)
    tank2.draw (screen)
    if (game_state == "player1" or game_state == "player1fire"):
        screen.draw.text("Player 1\nPower "+str(tank1.get_gun_power())+"%", fontsize=30, topleft=(50,50), color=(TEXT_COLOR))
    if (game_state == "player2" or game_state == "player2fire"):
        screen.draw.text("Player 2\nPower "+str(tank2.get_gun_power())+"%", fontsize=30, topright=(WIDTH-50,50), color=(TEXT_COLOR))
    if (game_state == "player1fire" or game_state == "player2fire"):
        shell.draw(screen)
    if (game_state == "game_over_1"):
        screen.draw.text("Game Over\nPlayer 1 wins!", fontsize=60, center=(WIDTH/2,200), color=(TEXT_COLOR))
    if (game_state == "game_over_2"):
        screen.draw.text("Game Over\nPlayer 2 wins!", fontsize=60, center=(WIDTH/2,200), color=(TEXT_COLOR))

def update():
    global game_state, game_timer
    # Delayed start (prevent accidental firing by holding start button down)
    if (game_state == 'start'):
        game_timer += 1
        if (game_timer == 30):
            game_timer = 0
            game_state = 'player1'
    # Only read keyboard in certain states
    if (game_state == 'player1'):
        player1_fired = player_keyboard("left")
        if (player1_fired == True):
            # Set shell position to end of gun
            # Use gun_positions so we can get start position
            gun_positions = tank1.calc_gun_positions ()
            shell.set_start_position(gun_positions[3])
            shell.set_current_position(gun_positions[3])
            game_state = 'player1fire'
            shell.set_angle(math.radians (tank1.get_gun_angle()))
            shell.set_power(tank1.get_gun_power() / 40)
            shell.set_time(0)
    if (game_state == 'player1fire'):
        shell.update_shell_position ("left")
        # shell value is whether the shell is inflight, hit or missed
        shell_value = detect_hit("left")
        # shell_value 20 is if other tank hit
        if (shell_value >= 20):
            game_state = 'game_over_1'
        # 10 is offscreen and 11 is hit ground, both indicate missed
        elif (shell_value >= 10):
            game_state = 'player2'
    if (game_state == 'player2'):
        player2_fired = player_keyboard("right")
        if (player2_fired == True):
            # Set shell position to end of gun
            # Use gun_positions so we can get start position
            gun_positions = tank2.calc_gun_positions ()
            shell.set_start_position(gun_positions[3])
            shell.set_current_position(gun_positions[3])
            game_state = 'player2fire'
            shell.set_angle(math.radians (tank2.get_gun_angle()))
            shell.set_power(tank2.get_gun_power() / 40)
            shell.set_time(0)
    if (game_state == 'player2fire'):
        shell.update_shell_position ("right")
        # shell value is whether the shell is inflight, hit or missed
        shell_value = detect_hit("right")
        # shell_value 20 is if other tank hit
        if (shell_value >= 20):
            game_state = 'game_over_2'
        # 10 is offscreen and 11 is hit ground, both indicate missed
        elif (shell_value >= 10):
            game_state = 'player1'
    if (game_state == 'game_over_1' or game_state == 'game_over_2'):
        # Allow space key or left-shift (picade) to continue
        if (keyboard.space or keyboard.lshift):
            game_state = 'start'
            # Reset position of tanks and terrain
            setup()




# Detects if the shell has hit something.
# Simple detection looks at colour of the screen at the position
# uses an offset to not detect the actual shell
# Return 0 for in-flight,
# 1 for offscreen temp (too high),
# 10 for offscreen permanent (too far),
# 11 for hit ground,
# 20 for hit other tank
def detect_hit (left_right):
    (shell_x, shell_y) = shell.get_current_position()
    # Add offset (3 pixels)
    # offset left/right depending upon direction of fire
    if (left_right == "left"):
        shell_x += 3
    else:
        shell_x -= 3
    shell_y += 3
    offset_position = (math.floor(shell_x), math.floor(shell_y))

    # Check whether it's off the screen
    # temporary if just y axis, permanent if x
    if (shell_x > WIDTH or shell_x <= 0 or shell_y >= HEIGHT):
        return 10
    if (shell_y < 1):
        return 1

    # Get colour at position
    color_pixel = screen.surface.get_at(offset_position)
    if (color_pixel == GROUND_COLOR):
        return 11
    if (left_right == 'left' and color_pixel == TANK_COLOR_P2):
        return 20
    if (left_right == 'right' and color_pixel == TANK_COLOR_P1):
        return 20

    return 0

# Handles keyboard for players
# If player has hit fire key (space) then returns True
# Otherwise changes angle of gun if applicable and returns False
def player_keyboard(left_right):
    global shell_start_position

    # get current angle
    if (left_right == 'left'):
        this_gun_angle = tank1.get_gun_angle()
        this_gun_power = tank1.get_gun_power()
    else:
        this_gun_angle = tank2.get_gun_angle()
        this_gun_power = tank2.get_gun_power()

    # Allow space key or left-shift (picade) to fire
    if (keyboard.space or keyboard.lshift):
        return True
    # Up moves firing angle upwards, down moves it down
    if (keyboard.up):
        if (left_right == 'left'):
            tank1.change_gun_angle(1)
        else:
            tank2.change_gun_angle(1)
    if (keyboard.down):
        if (left_right == 'left'):
            tank1.change_gun_angle(-1)
        else:
            tank2.change_gun_angle(-1)
    # left reduces power, right increases power
    if (keyboard.right):
        if (left_right == 'left'):
            tank1.change_gun_power(1)
        else:
            tank2.change_gun_power(1)
    if (keyboard.left):
        if (left_right == 'left'):
            tank1.change_gun_power(-1)
        else:
            tank2.change_gun_power(-1)

    return False
