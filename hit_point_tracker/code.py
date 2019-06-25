# https://learn.adafruit.com/circuitpython-display-support-using-displayio/sprite-sheet
import time
import board
import displayio
import digitalio
import adafruit_imageload
from gamepadshift import GamePadShift
from adafruit_display_shapes.rect import Rect
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font

# Color constants
WHITE = 0xFFFFFF
RED = 0xFF0000
CYAN = 0x00FFFF
BLUE = 0x0000FF
BLACK = 0x000000
GREEN = 0x00FF00

# Button constants
BUTTON_LEFT = const(128)
BUTTON_UP = const(64)
BUTTON_DOWN = const(32)
BUTTON_RIGHT = const(16)
BUTTON_SEL = const(8)
BUTTON_START = const(4)
BUTTON_A = const(2)
BUTTON_B = const(1)

# Other constants
FONTNAME = "/fonts/Arial-12.bdf"
MAX_HIT_POINT_BAR_WIDTH = 34

display = board.DISPLAY

# Define game pad objects
pad = GamePadShift(digitalio.DigitalInOut(board.BUTTON_CLOCK),
                   digitalio.DigitalInOut(board.BUTTON_OUT),
                   digitalio.DigitalInOut(board.BUTTON_LATCH))

# load the sprite sheet
sprite_sheet, palette = adafruit_imageload.load("/spritesheet.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)

sprite = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width = 1,
                            height = 1,
                            tile_width = 32,
                            tile_height = 32,
                            x = 4)

# fill the background
color_bitmap = displayio.Bitmap(160, 128, 1)
color_palette = displayio.Palette(1)
color_palette[0] = CYAN

bg_sprite = displayio.TileGrid(color_bitmap,
                               pixel_shader=color_palette,
                               x=0, y=0)

group = displayio.Group(scale = 4)
group.append(bg_sprite)
group.append(sprite)

# draw health bar
# Rect(x, y, width, height)
health_bar = Rect(2, 26, 36, 5, fill=RED, outline=BLACK)
group.append(health_bar)

# draw hit point bar
hit_point_bar = Rect(3, 27, MAX_HIT_POINT_BAR_WIDTH, 3, fill=GREEN)
group.append(hit_point_bar)

# initialize hit point text
font_name = bitmap_font.load_font(FONTNAME)
font_name.load_glyphs("TEST".encode('utf-8'))
hit_point_label = Label(font_name, text="ELF", line_spacing=0.75)
(x, y, w, h) = hit_point_label.bounding_box
hit_point_label.y = 25
# display.show(hit_point_label)
# group.append(hit_point_label)

display.show(group)

current_buttons = pad.get_pressed()
last_read = 0
max_hit_points = 25
current_hit_points = max_hit_points
source_index = 0
hit_point_level = 1
while True:
    index = source_index % (hit_point_level * 6)
    if (hit_point_level - 1) * 6 <= index < hit_point_level * 6:
        sprite[0] = index
        time.sleep(0.05)
    source_index += 1

    # reading buttons too fast returns 0
    if (last_read + 0.1) < time.monotonic():
        buttons = pad.get_pressed()
        last_read = pad.get_pressed();
    if current_buttons != buttons:
        # respond to buttons
        if (buttons & BUTTON_RIGHT) > 0 and current_hit_points < max_hit_points:
            current_hit_points += 1
        elif (buttons & BUTTON_LEFT) > 0 and current_hit_points > 0:
            current_hit_points -= 1

        health_percentage = current_hit_points / max_hit_points

        if health_percentage > 0.75:
            hit_point_level = 1
        elif 0.50 < health_percentage <= 0.75:
            hit_point_level = 2
        elif 0.25 < health_percentage <= 0.50:
            hit_point_level = 3
        elif 0 <= health_percentage:
            hit_point_level = 4

        # not the ideal update to the hitpoint bar but it's a workaround
        group.pop()
        hit_point_bar = Rect(3, 27, int(MAX_HIT_POINT_BAR_WIDTH * health_percentage), 3, fill=GREEN)
        group.append(hit_point_bar)
        #hit_point_bar.width = int(MAX_HIT_POINT_BAR_WIDTH * health_percentage
        current_buttons = buttons