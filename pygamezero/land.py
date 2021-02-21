import pygame
import math
import random

# Creates the land for the tanks to go on.
# Also positions the tanks - which can be retrieved using get_tank_position method

# How big a chunk to split up x axis
LAND_CHUNK_SIZE = 20
# Max that land can go up or down within chunk size
LAND_MAX_CHG = 20
# Max height of ground
LAND_MIN_Y = 200

class Land:

    def __init__ (self, ground_color, screen_size):
        self.ground_color = ground_color
        self.screen_size = screen_size

        # Setup landscape (these positions represent left side of platform)
        # Choose a random position (temp values - to be stored in tank object)
        # The complete x,y co-ordinates will be saved in a tuple in left_tank_rect and right_tank_rect
        left_tank_x_position = random.randint (10,300)
        right_tank_x_position = random.randint (500,750)

        # Sub divide screen into chunks for the landscape
        # store as list of x positions (0 is first position)
        current_land_x = 0
        current_land_y = random.randint (300,400)
        self.land_positions = [(current_land_x,current_land_y)]
        while (current_land_x < self.screen_size[0]):
            if (current_land_x == left_tank_x_position):
                # handle tank platform
                self.tank1_position = (current_land_x, current_land_y)
                # Add another 50 pixels further along at same y position (level ground for tank to sit on)
                current_land_x += 60
                self.land_positions.append((current_land_x, current_land_y))
                continue
            elif (current_land_x == right_tank_x_position):
                # handle tank platform
                self.tank2_position = (current_land_x, current_land_y)
                # Add another 50 pixels further along at same y position (level ground for tank to sit on)
                current_land_x += 60
                self.land_positions.append((current_land_x, current_land_y))
                continue
            # Checks to see if next position will be where the tanks are
            if (current_land_x < left_tank_x_position and current_land_x + LAND_CHUNK_SIZE >= left_tank_x_position):
                # set x position to tank position
                current_land_x = left_tank_x_position
            elif (current_land_x < right_tank_x_position and current_land_x + LAND_CHUNK_SIZE >= right_tank_x_position):
                # set x position to tank position
                current_land_x = right_tank_x_position
            elif (current_land_x + LAND_CHUNK_SIZE > self.screen_size[0]):
                current_land_x = self.screen_size[0]
            else:
                current_land_x += LAND_CHUNK_SIZE
            # Set the y height
            current_land_y += random.randint(0-LAND_MAX_CHG,LAND_MAX_CHG)
            # check not too high or too lower (note the reverse logic as high y is bottom of screen)
            if (current_land_y > self.screen_size[1]):   # Bottom of screen
                current_land_y = self.screen_size[1]
            if (current_land_y < LAND_MIN_Y):
                current_land_y = LAND_MIN_Y
            # Add to list
            self.land_positions.append((current_land_x, current_land_y))
        # Add end corners
        self.land_positions.append((self.screen_size[0],self.screen_size[1]))
        self.land_positions.append((0,self.screen_size[1]))

    def get_tank1_position(self):
        return self.tank1_position

    def get_tank2_position(self):
        return self.tank2_position



    def draw (self, screen):
        pygame.draw.polygon(screen.surface, self.ground_color, self.land_positions)


