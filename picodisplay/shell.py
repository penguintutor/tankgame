import math
import random

# Creates the land for the tanks to go on.
# Also positions the tanks - which can be retrieved using get_tank_position method

# How big a chunk to split up x axis
LAND_CHUNK_SIZE = 20
# Max that land can go up or down within chunk size
LAND_MAX_CHG = 20
# Max height of ground
LAND_MIN_Y = 50
# Ssize of land for tank
LAND_TANK_SIZE = 20

class Land:
    
    def __init__ (self, display, ground_color):
        self.display = display
        self.ground_color = ground_color
        self.screen_size = (display.get_width(), display.get_height())
        self.setup()
        
    def setup(self):
        
        # Create an array of land y values - gravity means that all blocks below are solid (no caves)
        # Initially all set to 0
        self.land_y_positions = [0] * self.display.get_width()
        
        # Setup landscape (these positions represent left side of platform)
        # Choose a random position (temp values - to be stored in tank object)
        # The complete x,y co-ordinates will be saved in a tuple in left_tank_rect and right_tank_rect
        # includes a DMZ of 40 pixels
        left_tank_x_position = random.randint (10,int(self.screen_size[0]/2)-30)
        right_tank_x_position = random.randint (int(self.screen_size[0]/2)+30,self.screen_size[0]-40)
        
        self.tank1_position = (left_tank_x_position,0)
        self.tank2_position = (right_tank_x_position,0)
        
        # Sub divide screen into chunks for the landscape
        current_land_x = 0
        next_land_x = 0 + LAND_CHUNK_SIZE
        # start y position at least 50 from top 20 from bottom
        current_land_y = random.randint (50,self.display.get_height()-20)
        self.land_y_positions[current_land_x] = current_land_y
        while (current_land_x < self.screen_size[0]):
            # If where tank is then we create a flat area for tank to sit on
            if (current_land_x == left_tank_x_position):
                # handle tank platform
                self.tank1_position = (current_land_x, int(current_land_y))
                # Add another 60 pixels further along at same y position (level ground for tank to sit on)
                for i in range (0, LAND_TANK_SIZE):
                    self.land_y_positions[current_land_x] = int(current_land_y)
                    current_land_x += 1
                continue
            elif (current_land_x == right_tank_x_position):
                # handle tank platform
                self.tank2_position = (current_land_x, int(current_land_y))
                # Add another 60 pixels further along at same y position (level ground for tank to sit on)
                for i in range (0, LAND_TANK_SIZE):
                    self.land_y_positions[current_land_x] = int(current_land_y)
                    current_land_x += 1
                continue
            
            # Checks to see if next position will be where the tanks are
            if (current_land_x < left_tank_x_position and current_land_x + LAND_CHUNK_SIZE >= left_tank_x_position):
                # set x position to tank position
                next_land_x = left_tank_x_position
            elif (current_land_x < right_tank_x_position and current_land_x + LAND_CHUNK_SIZE >= right_tank_x_position):
                # set x position to tank position
                next_land_x = right_tank_x_position
            elif (current_land_x + LAND_CHUNK_SIZE > self.screen_size[0]):
                next_land_x = self.screen_size[0] 
            else:
                next_land_x = current_land_x + LAND_CHUNK_SIZE
            # Set the y height
            next_land_y = current_land_y + random.randint(0-LAND_MAX_CHG,LAND_MAX_CHG)
            # check not too high or too lower (note the reverse logic as high y is bottom of screen)
            if (next_land_y > self.screen_size[1]):   # Bottom of screen
                next_land_y = self.screen_size[1]
            if (next_land_y < LAND_MIN_Y):
                next_land_y = LAND_MIN_Y
            # Add to list
            # Work through until current_land_x = next_land_x
            # delta is how much the y value changes per increment
            # Check not flat first
            if (next_land_y == current_land_y or next_land_x == current_land_x):
                y_delta = 0
            else:
                y_delta = (next_land_y - current_land_y) / (next_land_x - current_land_x)
            for i in range (current_land_x, next_land_x):
                current_land_y += y_delta
                self.land_y_positions[current_land_x] = int(current_land_y)
                current_land_x += 1
            

    def get_tank1_position(self):
        return self.tank1_position
        
    def get_tank2_position(self):
        return self.tank2_position
        

    def draw (self):
        self.display.set_pen(*self.ground_color)
        current_land_x = 0
        for this_pos in self.land_y_positions:
            for this_y in range (self.land_y_positions[current_land_x], self.screen_size[1]):
                self.display.pixel(current_land_x, int(this_y))
            current_land_x += 1
        
        
        

