# https://learn.adafruit.com/circuitpython-display-support-using-displayio/sprite-sheet
import time
import board
import displayio
import adafruit_imageload

WHITE = 0xFFFFFF
display = board.DISPLAY

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
color_palette[0] = WHITE

bg_sprite = displayio.TileGrid(color_bitmap,
                               pixel_shader=color_palette,
                               x=0, y=0)

group = displayio.Group(scale = 4)
group.append(bg_sprite)
group.append(sprite)

display.show(group)

source_index = 0
while True:
    sprite[0] = source_index % 12
    source_index += 1
    time.sleep(0.05)