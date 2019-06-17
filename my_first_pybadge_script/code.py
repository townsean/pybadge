# Write your code here :-)
import board
import digitalio
import time
import neopixel

PIXEL_PIN = board.D8
ORDER = neopixel.RGB
COLOR = (232, 63, 12)
VIOLET = (148, 0, 211)
INDIGO = (75, 0, 130)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 127, 0)
RED = (255, 0, 0)
RAINBOW_COLORS = [VIOLET, INDIGO, BLUE, GREEN, YELLOW, ORANGE, RED]
CLEAR = (0, 0, 0)
DELAY = 0.5

pixel = neopixel.NeoPixel(PIXEL_PIN, 1, brightness=0.05, pixel_order=ORDER)
index = 0
while True:
    pixel[0] = RAINBOW_COLORS[index]
    time.sleep(DELAY)

    if(index + 1 == len(RAINBOW_COLORS)):
        index = 0
    else:
        index += 1

    if index % 2 == 0:
        print("*" * 10)
    else:
        print("-" * 10)
    print("Current color is {}.".format(RAINBOW_COLORS[index]))