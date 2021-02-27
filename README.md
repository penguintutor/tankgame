# Tank Game
This is a Tank game. An artillary style pass and play game. It is created as a demonstration of creating vector graphics in Pygame Zero and of porting / creating a game on the Raspberry Pi Pico with the Pimoroni Display Pack.

# Pygame Zero Game 

The initial version was created in Python Pygame Zero as part of the book Beginning Game Programming with Pygame Zero.

More details of the original game are in the book:
http://www.penguintutor.com/projects/book-pygamezero 

## Installing / Running the Pygame Zero game

The Pygame zero version is in the folder pygamezero. All the files need to be in a single folder and the game launched from that folder.

You need either the Mu Editor installed https://codewith.mu/ or Python with Pygame Zero installed https://pygame-zero.readthedocs.io/en/stable/ . This is included as standard on the Raspberry Pi. 

If you have the Mu editor installed then you can load the file tankgame.py into the Mu editor, ensure you are in Pygame Zero mode and then choose run. 

To run using the command line and pygame zero change to the game's pygame zero directory and then run

pgzrun tankgame.py 


## Playing the Pygame Zero Version

Play starts with player 1. The angle of the current tank is adjusted using the up and down arrow. The power is adjusted using the left and right buttons and then press the space bar to fire a shell towards the enemy.

If you score a hit then you win, otherwise the game passes to the next player.

# Raspberry Pi Pico 

This is designed to play on a Raspberry Pi Pico with the Pimoroni Display Pack. 

## Installing / Running the Pico Display version

Before you can run the game you need the Pimoroni version of MicroPython. For details on how to install that see: https://learn.pimoroni.com/tutorial/hel/getting-started-with-pico 

The Raspberry Pi Pico program is in the directory picodisplay. You need to copy all of the files onto the Pico. The easiest way to do this is using the Thonny editor. Copy and paste each file into a new page in the editor and save that as the same file on the Pico.

# Playing the Raspberry Pi Pico version

The game is a pass and play game starting with player 1. Press the B button to select between Angle and Power adjustment. The appropriate mode will be displayed on the screen. Press the X and Y buttons to adjust the angle or power as appropriate. Press the A button to fire a shell.

If you score a hit then you win, otherwise the game passes to the next player.

# More Details

For more details about the game see: 
http://www.penguintutor.com/projects/pico-tankgame