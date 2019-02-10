from ir_camera import *

set_scale()
get_temp()
sleep(0.25)

try:
    while True:
        if not scale_btn.value: # when button pin value goes low
            update_temp_max()
            set_scale()
            sleep(0.1)
        set_matrix()
except KeyboardInterrupt:
    pass
