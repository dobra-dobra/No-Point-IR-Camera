import board
import digitalio
import rotaryio
from ir_camera import *
from time import sleep

# Initialize button used take a photo when connected to PC
photo_btn = digitalio.DigitalInOut(board.D10)
photo_btn.direction = digitalio.Direction.INPUT
photo_btn.pull = digitalio.Pull.UP

# Initialize rotary encoder used for temperature scale change
encoder = rotaryio.IncrementalEncoder(board.A2, board.A3)

set_scale()
get_temp()
sleep(0.25)

enc_last_pos = encoder.position

try:
    while True:
        if not photo_btn.value: # when button pin value goes low
            pixels.fill((0, 0, 0))
            pixels.show()
            sleep(0.1)
            send_temperatures()
            sleep(0.1)
            set_scale()
        enc_pos = encoder.position
        if enc_pos != enc_last_pos:
            update_temp_max(enc_last_pos - enc_pos)
            set_scale()
            enc_last_pos = enc_pos
        set_matrix()
except KeyboardInterrupt:
    pass
