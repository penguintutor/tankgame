import math

class Shell:
    
    def __init__ (self, display, shell_color):
        self.display = display
        self.shell_color = shell_color
        self.start_position = (0,0)
        self.current_position = (0,0)
        self.power = 1
        self.angle = 0
        self.time = 0
        
    def set_start_position(self, position):
        self.start_position = position
 
    def get_start_position(self):
        return self.start_position
        
    def set_current_position(self, position):
        self.current_position = position
        
    def get_current_position(self):
        return self.current_position
        
    def set_angle(self, angle):
        self.angle = angle
        
    def set_power(self, power):
        self.power = power
    
    def set_time(self, time):
        self.time = time
        
    def draw (self):
        (xpos, ypos) = self.current_position
        # Create rectangle of the shell
        self.display.set_pen(*self.shell_color)
        self.display.rectangle(int(xpos), int(ypos), 2, 2)
        
    def update_shell_position (self, left_right):
        
        init_velocity_y = self.power * math.sin(self.angle)
        
        # Direction - multiply by -1 for left to right
        if (left_right == 'left'):
            init_velocity_x = self.power * math.cos(self.angle)
        else:
            init_velocity_x = self.power * math.cos(math.pi - self.angle)
            
        # Gravity constant is 9.8 m/s^2 but this is in terms of screen so instead use a sensible constant (0.004)
        GRAVITY_CONSTANT = 0.008
        # Constant to give a sensible distance on x axis (1.5 on pygame zero)
        DISTANCE_CONSTANT = 1.5
        # Wind is not included in this version, to implement then decreasing wind value is when the wind is against the fire direction
        # wind > 1 is where wind is against the direction of fire. Wind must never be 0 or negative (which would make it impossible to fire forwards)
        wind_value = 1
        
        # time is calculated in update cycles
        shell_x = self.start_position[0] + init_velocity_x * self.time * DISTANCE_CONSTANT
        shell_y = self.start_position[1] + -1 * ((init_velocity_y * self.time) - (0.5 * GRAVITY_CONSTANT * self.time * self.time * wind_value))
        
        self.current_position = (shell_x, shell_y)
           
        self.time += 4
