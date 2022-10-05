import math
import random
import utime
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY
from pimoroni import Button
from tank import Tank
from shell import Shell
from land import Land

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, rotate=0)
display.set_backlight(1.0)

width, height = display.get_bounds()

# Colour constants
sky_color = display.create_pen(165,182,255)
gnd_color = display.create_pen(9,84,5)     
# Different tank colors for player 1 and player 2
# These colors must be unique as well as the GROUND_COLOR
tank_color_p1 = display.create_pen(216, 216, 153)     
tank_color_p2 = display.create_pen(219, 163, 82)      
shell_color = display.create_pen(255,255,255)
text_color = display.create_pen(255,255,255)
text_color_active = display.create_pen(0,0,0)

# States are:
# start - timed delay before start
# player1 - waiting for player to set position
# player1fire - player 1 fired
# player2 - player 2 set position
# player2fire - player 2 fired
# game_over_1 / game_over_2 - show who won 1 = player 1 won etc.
game_state = "player1"

# switch button mode from angle to power
key_mode = "angle"

# Tank 1 = Left
tank1 = Tank(display, "left", tank_color_p1)
# Tank 2 = Right
tank2 = Tank(display, "right", tank_color_p2)

# Only fire one shell at a time, a single shell object can be used for both player 1 and player 2    
shell = Shell(display, shell_color)
    
ground = Land(display, gnd_color)

def run_game():
    global key_mode, game_state

    while True:
        ## Draw methods
        display.set_pen(sky_color)
        display.clear()
        
        display.set_pen(tank_color_p1)
        
        ground.draw()
        tank1.draw ()
        tank2.draw ()
        
        # debug tank rect
        #display.set_pen(display.create_pen(255,0,0))
        #positions = tank2.get_rect()
        #display.rectangle(positions[0], positions[1], positions[2]-positions[0], positions[3]-positions[1])
        
        display.update()
        
        if (game_state == "player1fire" or game_state == "player2fire"):
            shell.draw()

        display.set_pen(text_color)
        if (game_state == "player1" or game_state == "player1fire"):
            display.text("Player 1", 10, 10, 240, 1)
            if (key_mode == "power"):
                display.set_pen(text_color_active)
            display.text("Power "+str(tank1.get_gun_power())+"%", 10, 20, 240, 1)#
            if (key_mode == "angle"):
                display.set_pen(text_color_active)
            else:
                display.set_pen(text_color)
            display.text("Angle "+str(tank1.get_gun_angle()), 10, 30, 240, 1)
        if (game_state == "player2" or game_state == "player2fire"):
            display.text("Player 2", 180, 10, 240, 1)
            if (key_mode == "power"):
                display.set_pen(text_color_active)
            display.text("Power "+str(tank2.get_gun_power())+"%", 180, 20, 240, 1)
            if (key_mode == "angle"):
                display.set_pen(text_color_active)
            else:
                display.set_pen(text_color)
            display.text("Angle "+str(tank2.get_gun_angle()), 180, 30, 240, 1)
        if (game_state == "game_over_1"):
            display.text("Game Over", 50, 20, 240, 3)
            display.text("Player 1 wins!", 30, 40, 240, 3)
        if (game_state == "game_over_2"):
            display.text("Game Over", 50, 20, 240, 3)
            display.text("Player 2 wins!", 30, 40, 240, 3)
        display.update()


        ## Update methods
        # Only read keyboard in certain states
        if (game_state == 'player1'):
            player1_fired = player_keyboard("left")
            if (player1_fired == True):
                # Set shell position to end of gun
                # Use gun_positions so we can get start position 
                gun_positions = tank1.calc_gun_positions ()
                start_shell_pos = (gun_positions[3][0],gun_positions[3][1]+2)
                shell.set_start_position(start_shell_pos)
                shell.set_current_position(start_shell_pos)
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
                # reset key mode to angle
                key_mode = "angle"
                game_state = 'player2'
        if (game_state == 'player2'):
            player2_fired = player_keyboard("right")
            if (player2_fired == True):
                # Set shell position to end of gun
                # Use gun_positions so we can get start position 
                gun_positions = tank2.calc_gun_positions ()
                start_shell_pos = (gun_positions[3][0],gun_positions[3][1]+2)
                shell.set_start_position(start_shell_pos)
                shell.set_current_position(start_shell_pos)
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
                # reset key mode to angle
                key_mode = "angle"
        if (game_state == 'game_over_1' or game_state == 'game_over_2'):
            # Allow space key or left-shift (picade) to continue
            if (button_b.read()) :
                # Reset position of tanks and terrain
                setup()


# Reset
def setup():
    global game_state, key_mode
    # reset key mode to angle
    key_mode = "angle"
    ground.setup()
    # Get positions of tanks from ground generator
    tank1.set_position(ground.get_tank1_position())
    tank2.set_position(ground.get_tank2_position())
    game_state = "player1"
    
    
    
# Detects if the shell has hit something. 

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
        shell_x += 2
    else:
        shell_x -= 2
    shell_y += 2
    offset_position = (math.floor(shell_x), math.floor(shell_y))
    
    # Check whether it's off the screen 
    # may be temporary if just y axis, permanent if x
    if (shell_x > width or shell_x <= 0 or shell_y >= height):
        return 10
    if (shell_y < 1):
        # special case if gone beyond size of screen then that's too far
        if (shell_y < 0-height):
            return 10
        return 1
        
    # check to see if it's hit a tank
    
    # get x and y for rect covering tank
    tank1_rect = tank1.get_rect()
    tank2_rect = tank2.get_rect()
    
    # If gone below bottom of screen - hit ground
    if (shell_y >= height):
        return 11
    
    # If hit tank 1
    if (left_right == 'right' and
        shell_x >= tank1_rect[0] and
        shell_x <= tank1_rect[2] and
        shell_y >= tank1_rect[1] and
        shell_y <= tank1_rect[3]):
        print ("Hit Tank 1")
        return 20

    # If hit tank 2
    if (left_right == 'left' and
            shell_x >= tank2_rect[0] and
            shell_x <= tank2_rect[2] and
            shell_y >= tank2_rect[1] and
            shell_y <= tank2_rect[3]):
        print ("Hit Tank 2")
        return 20

    if (ground.is_ground(int(shell_x), int(shell_y))):
        return 11
    
    return 0
    
# Handles keyboard for players
# Although named keyboard (consistancy with pygame zero version) - for the pico this refers to buttons
# If player has hit fire key (space) then returns True
# Otherwise changes angle of gun if applicable and returns False
def player_keyboard(left_right):
    global key_mode
    
    # change key_mode between angle and power using B button
    if (button_b.read()) :
        if key_mode == "angle":
            key_mode = "power"
        else:
            key_mode = "angle"
        # add delay to prevent accidental double press
        utime.sleep(0.5)
    
    # A button is fire
    if (button_a.read()) :
        return True
    # Up moves firing angle upwards or increase power
    if (button_x.read()) :
        if (key_mode == "angle" and left_right == 'left'):
            tank1.change_gun_angle(5)
        elif (key_mode == "angle" and left_right == 'right'):
            tank2.change_gun_angle(5)
        elif (key_mode == "power" and left_right == 'left'):
            tank1.change_gun_power(5)
        elif (key_mode == "power" and left_right == 'right'):
            tank2.change_gun_power(5)
    # Down moves firing angle downwards or decrease power
    if (button_y.read()) :
        if (key_mode == "angle" and left_right == 'left'):
            tank1.change_gun_angle(-5)
        elif (key_mode == "angle" and left_right == 'right'):
            tank2.change_gun_angle(-5)
        elif (key_mode == "power" and left_right == 'left'):
            tank1.change_gun_power(-5)
        elif (key_mode == "power" and left_right == 'right'):
            tank2.change_gun_power(-5)

    return False

# Returns as list
def get_display_bytes (x, y):
    buffer_pos = (x*2) + (y*width*2)
    byte_list = [display_buffer[buffer_pos], display_buffer[buffer_pos+1]]
    return (byte_list)

def color_to_bytes (color):
    r, g, b = color
    bytes = [0,0]
    bytes[0] = r & 0xF8
    bytes[0] += (g & 0xE0) >> 5
    bytes[1] = (g & 0x1C) << 3
    bytes[1] += (b & 0xF8) >> 3
    
    return bytes
    
setup()
run_game()

