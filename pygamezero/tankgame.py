import math
import random
import pygame
from tank import Tank

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

# How big a chunk to split up x axis
LAND_CHUNK_SIZE = 20
# Max that land can go up or down within chunk size
LAND_MAX_CHG = 20
# Max height of ground
LAND_MIN_Y = 200

# Timer used to create delays before action (prevent accidental button press)
game_timer = 0

# Angle that the gun is pointing (degrees relative to horizontal)
left_gun_angle = 20
right_gun_angle = 50
# Amount of power to fire with - is divided by 40 to give scale 10 to 100
left_gun_power = 25
right_gun_power = 25
# These are shared between left and right as we only fire one shell at a time
shell_power = 1
shell_angle = 0
shell_time = 0

# Position of shell when fired (create as a global - but update before use)
shell_start_position = (0,0)
shell_current_position = (0,0)

# Position of the two tanks - set to zero, update before use
left_tank_position = (0,0)
right_tank_position = (0,0)

# Tank 1 = Left
tank1 = Tank("left")
# Tank 2 = Right
tank2 = Tank("right")

def draw_shell (position):
    (xpos, ypos) = position
    # Create rectangle of the shell
    shell_rect = Rect((math.floor(xpos),math.floor(ypos)),(5,5))
    pygame.draw.ellipse(screen.surface, SHELL_COLOR, shell_rect)



def draw():
    global game_state, left_tank_position, right_tank_position, left_gun_angle, right_gun_angle, shell_start_position
    screen.fill(SKY_COLOR)
    pygame.draw.polygon(screen.surface, GROUND_COLOR, land_positions)
    tank1.draw_tank (screen, left_tank_position, left_gun_angle)
    tank2.draw_tank (screen, right_tank_position, right_gun_angle)
    if (game_state == "player1" or game_state == "player1fire"):
        screen.draw.text("Player 1\nPower "+str(left_gun_power)+"%", fontsize=30, topleft=(50,50), color=(TEXT_COLOR))
    if (game_state == "player2" or game_state == "player2fire"):
        screen.draw.text("Player 2\nPower "+str(right_gun_power)+"%", fontsize=30, topright=(WIDTH-50,50), color=(TEXT_COLOR))
    if (game_state == "player1fire" or game_state == "player2fire"):
        draw_shell(shell_current_position)
    if (game_state == "game_over_1"):
        screen.draw.text("Game Over\nPlayer 1 wins!", fontsize=60, center=(WIDTH/2,200), color=(TEXT_COLOR))
    if (game_state == "game_over_2"):
        screen.draw.text("Game Over\nPlayer 2 wins!", fontsize=60, center=(WIDTH/2,200), color=(TEXT_COLOR))

def update():
    global game_state, left_gun_angle, left_tank_position, shell_start_position, shell_current_position, shell_angle, shell_time, left_gun_power, right_gun_power, shell_power, game_timer
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
            gun_positions = tank1.calc_gun_positions (left_tank_position, left_gun_angle)
            shell_start_position = gun_positions[3]
            shell_current_position = gun_positions[3]
            game_state = 'player1fire'
            shell_angle = math.radians (left_gun_angle)
            shell_power = left_gun_power / 40
            shell_time = 0
    if (game_state == 'player1fire'):
        update_shell_position ("left")
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
            gun_positions = tank2.calc_gun_positions (right_tank_position, right_gun_angle)
            shell_start_position = gun_positions[3]
            shell_current_position = gun_positions[3]
            game_state = 'player2fire'
            shell_angle = math.radians (right_gun_angle)
            shell_power = right_gun_power / 40
            shell_time = 0
    if (game_state == 'player2fire'):
        update_shell_position ("right")
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


def update_shell_position (left_right):
    global shell_power, shell_angle, shell_start_position, shell_current_position, shell_time

    init_velocity_y = shell_power * math.sin(shell_angle)

    # Direction - multiply by -1 for left to right
    if (left_right == 'left'):
        init_velocity_x = shell_power * math.cos(shell_angle)
    else:
        init_velocity_x = shell_power * math.cos(math.pi - shell_angle)

    # Gravity constant is 9.8 m/s^2 but this is in terms of screen so instead use a sensible constant
    GRAVITY_CONSTANT = 0.004
    # Constant to give a sensible distance on x axis
    DISTANCE_CONSTANT = 1.5
    # Wind is not included in this version, to implement then decreasing wind value is when the wind is against the fire direction
    # wind > 1 is where wind is against the direction of fire. Wind must never be 0 or negative (which would make it impossible to fire forwards)
    wind_value = 1

    # time is calculated in update cycles
    shell_x = shell_start_position[0] + init_velocity_x * shell_time * DISTANCE_CONSTANT
    shell_y = shell_start_position[1] + -1 * ((init_velocity_y * shell_time) - (0.5 * GRAVITY_CONSTANT * shell_time * shell_time * wind_value))

    shell_current_position = (shell_x, shell_y)

    shell_time += 1

# Detects if the shell has hit something.
# Simple detection looks at colour of the screen at the position
# uses an offset to not detect the actual shell
# Return 0 for in-flight,
# 1 for offscreen temp (too high),
# 10 for offscreen permanent (too far),
# 11 for hit ground,
# 20 for hit other tank
def detect_hit (left_right):
    global shell_current_position
    (shell_x, shell_y) = shell_current_position
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
    global shell_start_position, left_gun_angle, right_gun_angle, left_gun_power, right_gun_power

    # get current angle
    if (left_right == 'left'):
        this_gun_angle = left_gun_angle
        this_gun_power = left_gun_power
    else:
        this_gun_angle = right_gun_angle
        this_gun_power = right_gun_power

    # Allow space key or left-shift (picade) to fire
    if (keyboard.space or keyboard.lshift):
        return True
    # Up moves firing angle upwards, down moves it down
    if (keyboard.up):
        this_gun_angle += 1
        if (this_gun_angle > 85):
            this_gun_angle = 85
    if (keyboard.down):
        this_gun_angle -= 1
        if (this_gun_angle < 0):
            this_gun_angle = 0
    # left reduces power, right increases power
    if (keyboard.right):
        this_gun_power += 1
        if (this_gun_power > 100):
            this_gun_power = 100
    if (keyboard.left):
        this_gun_power -= 1
        if (this_gun_power < 10):
            this_gun_power = 10

    # Update the appropriate global (left / right)
    if (left_right == 'left'):
        left_gun_angle = this_gun_angle
        left_gun_power = this_gun_power
    else:
        right_gun_angle = this_gun_angle
        right_gun_power = this_gun_power

    return False

# Setup game - allows create new game
def setup():
    global left_tank_position, right_tank_position, land_positions
    # Setup landscape (these positions represent left side of platform)
    # Choose a random position
    # The complete x,y co-ordinates will be saved in a tuple in left_tank_rect and right_tank_rect
    left_tank_x_position = random.randint (10,300)
    right_tank_x_position = random.randint (500,750)

    # Sub divide screen into chunks for the landscape
    # store as list of x positions (0 is first position)
    current_land_x = 0
    current_land_y = random.randint (300,400)
    land_positions = [(current_land_x,current_land_y)]
    while (current_land_x < WIDTH):
        if (current_land_x == left_tank_x_position):
            # handle tank platform
            left_tank_position = (current_land_x, current_land_y)
            # Add another 50 pixels further along at same y position (level ground for tank to sit on)
            current_land_x += 60
            land_positions.append((current_land_x, current_land_y))
            continue
        elif (current_land_x == right_tank_x_position):
            # handle tank platform
            right_tank_position = (current_land_x, current_land_y)
            # Add another 50 pixels further along at same y position (level ground for tank to sit on)
            current_land_x += 60
            land_positions.append((current_land_x, current_land_y))
            continue
        # Checks to see if next position will be where the tanks are
        if (current_land_x < left_tank_x_position and current_land_x + LAND_CHUNK_SIZE >= left_tank_x_position):
            # set x position to tank position
            current_land_x = left_tank_x_position
        elif (current_land_x < right_tank_x_position and current_land_x + LAND_CHUNK_SIZE >= right_tank_x_position):
            # set x position to tank position
            current_land_x = right_tank_x_position
        elif (current_land_x + LAND_CHUNK_SIZE > WIDTH):
            current_land_x = WIDTH
        else:
            current_land_x += LAND_CHUNK_SIZE
        # Set the y height
        current_land_y += random.randint(0-LAND_MAX_CHG,LAND_MAX_CHG)
        # check not too high or too lower (note the reverse logic as high y is bottom of screen)
        if (current_land_y > HEIGHT):   # Bottom of screen
            current_land_y = HEIGHT
        if (current_land_y < LAND_MIN_Y):
            current_land_y = LAND_MIN_Y
        # Add to list
        land_positions.append((current_land_x, current_land_y))
    # Add end corners
    land_positions.append((WIDTH,HEIGHT))
    land_positions.append((0,HEIGHT))

# Setup the game (at end so that it can see the other functions)
setup()