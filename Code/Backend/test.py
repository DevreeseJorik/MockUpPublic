from repositories.ShiftRepo import ShiftRegister
import time
from RPi import GPIO

try: 
    
    shift = ShiftRegister()
    shift.setup()
    while True:
        shift.change_state_pump(0,1)
        time.sleep(1)
        shift.change_state_pump(3,1)
        time.sleep(1)
        shift.set_all_pumps(0)
        time.sleep(1)

        # for i in range(6):
        #     print(f"Enabling {i}")
        #     shift.write_byte((1<<i)^0xFF)
        #     time.sleep(1)
        #     print("Writing 1")
        # time.sleep(1)
except Exception:
    shift.set_all_pumps(0)
except KeyboardInterrupt:
    shift.set_all_pumps(0)
