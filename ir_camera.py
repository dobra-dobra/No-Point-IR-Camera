import board
import busio
import adafruit_amg88xx
import neopixel

# Initialize IR sensor
i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)

# Initialize NEOPIXEL matrix
pixel_pin = board.D5
num_pixels = 72 # 64 LEDs on 8x8 matrix and 8 LEDs on temperature scale display
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False, pixel_order=ORDER)

# Define pixel numbers map for RGB matrix
screen_map = []
for row in range(8):
    row_table = []
    for col in range(8):
        row_table.append(8 * row + col)
    screen_map.append(row_table)

# Define pixel numbers map for temperature scale display
temp_scale_map = [i for i in range(64, 73)]

# Define maximal temperature
temp_max = 30

# Change maximal temperature when encoder is rotated
def update_temp_max(change):
    global temp_max
    temp_max = temp_max + 10 * change
    if temp_max > 80:
        temp_max = 80
    elif temp_max < 10:
        temp_max = 10

def get_temp():
    """
    Reads temperatures from AMG8833
    Returns table of 8 tables representing
    rows of data from sensor
    """
    temperature = amg.pixels
    return temperature

# Calculate colour change step for 1 deg. C
def colour_step(temp_max):
    return (255 / temp_max) * 2

# Check if value of parameter is between 0 and 255
def normalize(value):
    if value > 255:
        return 255
    elif value < 0:
        return 0
    else:
        return value

# There is a bug in adafruit_AMG88xx library
# which cause that negative temperatures are read
# as values above 500 deg. C
# https://forums.adafruit.com/viewtopic.php?f=8&t=127137
def normalize_temp(temp):
    if temp > 450:
        return 0.0
    else:
        return temp

# Calculate colour for given temperature
def convert_temp(temp, temp_max, step):
    temp = normalize_temp(temp)
    red = normalize(int(255 - (temp_max - temp) * step))
    blue = normalize(int(255 - temp * step))
    if red:
        green = 255 - red
    else:
        green = 255 - blue
    return (red,green,blue)

def colours_map(temp):
    step = colour_step(temp_max)
    colours = []
    for row in temp:
        row_colours = []
        for temp in row:
            row_colours.append(convert_temp(temp, temp_max, step))
        colours.append(row_colours)
    return colours

def set_scale():
    step = colour_step(temp_max)
    for i in range(temp_max // 10):
        pixels[temp_scale_map[i]] = convert_temp(i * 10 + 10, temp_max, step) # 1st pixel: 10 deg. C, 2nd: 20 deg. C, etc.
    for i in range(temp_max // 10, 8):
        pixels[temp_scale_map[i]] = convert_temp(temp_max, temp_max, step)
    pixels.show()

def set_matrix():
    temperatures = get_temp()
    colours = colours_map(temperatures)
    for i in range(8): # get consecutive rows
        for j in range(8): # get consecutive pixels
            pixels[screen_map[i][j]] = colours[i][j]
    pixels.show()

def send_temperatures():
    temperatures = get_temp()
    print(temperatures)
