#from pgzero import Rect
import math
import pygame

TANK_COLOR_P1 = (216, 216, 153)
TANK_COLOR_P2 = (219, 163, 82)
SHELL_COLOR = (255,255,255)

class Tank:

    def __init__(self, left_right, tank_color):
        self.left_right = left_right
        self.tank_color = tank_color

    # Draws tank (including gun - which depends upon direction and aim)
    # self.left_right can be "left" or "right" to depict which position the tank is in
    # tank_start_pos requires x, y co-ordinates as a tuple
    # angle is relative to horizontal - in degrees
    def draw_tank (self, screen, tank_start_pos, gun_angle):
        (xpos, ypos) = tank_start_pos

        # The shape of the tank track is a polygon
        # (uses list of tuples for the x and y co-ords)
        track_positions = [
            (xpos+5, ypos-5),
            (xpos+10, ypos-10),
            (xpos+50, ypos-10),
            (xpos+55, ypos-5),
            (xpos+50, ypos),
            (xpos+10, ypos)
        ]
        # Polygon for tracks (pygame not pygame zero)
        pygame.draw.polygon(screen.surface, self.tank_color, track_positions)

        # hull uses a rectangle which uses top right co-ords and dimensions
        hull_rect = pygame.Rect((xpos+15,ypos-20),(30,10))
        # Rectangle for tank body "hull" (pygame zero)
        screen.draw.filled_rect(hull_rect, self.tank_color)

        # Despite being an ellipse pygame requires this as a rect
        turret_rect = pygame.Rect((xpos+20,ypos-25),(20,10))
        # Ellipse for turret (pygame not pygame zero)
        pygame.draw.ellipse(screen.surface, self.tank_color, turret_rect)

        # Gun position involves more complex calculations so in a separate function
        gun_positions = self.calc_gun_positions (tank_start_pos, gun_angle)
        # Polygon for gun barrel (pygame not pygame zero)
        pygame.draw.polygon(screen.surface, self.tank_color, gun_positions)

    # Calculate the polygon positions for the gun barrel
    def calc_gun_positions (self, tank_start_pos, gun_angle):
        (xpos, ypos) = tank_start_pos
        # Set the start of the gun (top of barrel at point it joins the tank)
        if (self.left_right == "right"):
            gun_start_pos_top = (xpos+20, ypos-20)
        else:
            gun_start_pos_top = (xpos+40, ypos-20)

        # Convert angle to radians (for right subtract from 180 deg first)
        relative_angle = gun_angle
        if (self.left_right == "right"):
            relative_angle = 180 - gun_angle
        angle_rads = relative_angle * (math.pi / 180)
        # Create vector based on the direction of the barrel
        # Y direction *-1 (due to reverse y of screen)
        gun_vector =  (math.cos(angle_rads), math.sin(angle_rads) * -1)

        # Determine position bottom of barrel
        # Create temporary vector 90deg to existing vector
        if (self.left_right == "right"):
            temp_angle_rads = math.radians(relative_angle - 90)
        else:
            temp_angle_rads = math.radians(relative_angle + 90)
        temp_vector =  (math.cos(temp_angle_rads), math.sin(temp_angle_rads) * -1)

        # Add constants for gun size
        GUN_LENGTH = 20
        GUN_DIAMETER = 3
        gun_start_pos_bottom = (gun_start_pos_top[0] + temp_vector[0] * GUN_DIAMETER, gun_start_pos_top[1] + temp_vector[1] * GUN_DIAMETER)

        # Calculate barrel positions based on vector from start position
        gun_positions = [
            gun_start_pos_bottom,
            gun_start_pos_top,
            (gun_start_pos_top[0] + gun_vector[0] * GUN_LENGTH, gun_start_pos_top[1] + gun_vector[1] * GUN_LENGTH),
            (gun_start_pos_bottom[0] + gun_vector[0] * GUN_LENGTH, gun_start_pos_bottom[1] + gun_vector[1] * GUN_LENGTH),
        ]

        return gun_positions