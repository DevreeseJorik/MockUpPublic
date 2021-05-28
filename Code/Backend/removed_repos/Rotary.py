#pylint: skip-file
from RPi import GPIO
import time
from .SerialRepository import SerialRepository
from .LCDdisplay import Display
from .DataRepository import DataRepository
from .Cocktail import Cocktail

display = Display()

class Rotary(Cocktail):
    def __init__(self, queue=[],waiting=False, clk=21, dt=20, sw=16,rotary_id=0):
        super().__init__(queue,waiting)
        self.clk = clk
        self.dt = dt
        self.sw = sw

        self.counter = 0
        self.clk_last_state = 0
        self.setup_pins()
        self.rotary_id = rotary_id



    def setup_pins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.clk, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.dt, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.sw, GPIO.IN, GPIO.PUD_UP)
        GPIO.add_event_detect(self.clk, GPIO.BOTH, self.callback_clk, bouncetime=1)
        GPIO.add_event_detect(self.sw, GPIO.FALLING, self.callback_sw, bouncetime=250)
    
    def callback_clk(self, pin):
        clk_state = GPIO.input(self.clk)
        dt_state = GPIO.input(self.dt)
        if clk_state != self.clk_last_state and clk_state == False:
            if dt_state != clk_state:
                self.counter -= 1
                if self.counter < -2:
                    max_cocktails = DataRepository.get_total_cocktails()["count"]
                    self.rotary_id = (self.rotary_id  - 1) % max_cocktails
                    if self.rotary_id < 0:
                        self.rotary_id = max_cocktails - 1
                    display.display_drink_with_row_number(self.rotary_id)
            else:
                self.counter += 1
                if self.counter > 2:
                    self.counter = 0
                    max_cocktails = DataRepository.get_total_cocktails()["count"]
                    self.rotary_id = (self.rotary_id  + 1) % max_cocktails
                    display.display_drink_with_row_number(self.rotary_id)
        self.clk_last_state = clk_state
            
    def callback_sw(self, pin):
        print(pin)
        print(self.__waiting)
        if pin == 16:
            if self.rotary_id == 0:
                print("\nUser chose random drink!")
                self.make_random_recipe()
                return

            print(f"Received request to make cocktail: {self.rotary_id}")
            recipe = DataRepository.get_recipe_by_cocktail_id(self.rotary_id)
            self.make_cocktail(recipe,self.rotary_id)

if __name__ == '__main__':
    r = Rotary()
    try:
        while True:
            time.sleep(1)
    except Exception as e:
        print(e)