import random
from RPi import GPIO

from .SerialRepository import SerialRepository
from .DataRepository import DataRepository
from .LCDdisplay import Display

display = Display()

GPIO.setwarnings(False)


class Cocktail:
    def __init__(self,queue=[],waiting=True, clk=21, dt=20, sw=16,rotary_id=0):
        self.queue = queue
        self.waiting = waiting

        self.clk = clk
        self.dt = dt
        self.sw = sw

        self.counter = 0
        self.clk_last_state = 0
        self.rotary_id = rotary_id

        self.beveragevolumes = []
        self.extra_screens = 1

        self.setup_pins()
        self.get_volumes()

    def setup_pins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.clk, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.dt, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.sw, GPIO.IN, GPIO.PUD_UP)
        GPIO.add_event_detect(self.clk, GPIO.BOTH, self.callback_clk, bouncetime=1)
        GPIO.add_event_detect(self.sw, GPIO.FALLING, self.callback_sw, bouncetime=250)
    
    def get_volumes(self):
        beverages = DataRepository.get_all_beverages()
        for beverage in beverages:
            self.beveragevolumes.append(beverage["currentVolume"])
        # print(self.beveragevolumes)


    def callback_clk(self, pin):
        clk_state = GPIO.input(self.clk)
        dt_state = GPIO.input(self.dt)

        max_cocktails = DataRepository.get_total_cocktails()["count"]

        if clk_state != self.clk_last_state and clk_state == False:
            if dt_state != clk_state:
                # self.counter -= 1
                # if self.counter < -1:
                # self.counter = 0
                # print("Turning left")
                self.rotary_id = (self.rotary_id  - 1)
                if self.rotary_id < 0:
                    self.rotary_id = max_cocktails + self.extra_screens - 1
 
            else:
                # self.counter += 1
                # if self.counter > 1:
                # self.counter = 0
                # print("Turning right")
                self.rotary_id = (self.rotary_id  + 1) % (max_cocktails + self.extra_screens)


            if self.rotary_id < max_cocktails:
                display.display_drink_with_row_number(self.rotary_id)
            else:
                display.display_extra_screen(self.rotary_id-max_cocktails)
        self.clk_last_state = clk_state
            
    def callback_sw(self, pin):
        if pin == 16:
            if self.rotary_id == 0:
                # print("\nUser chose random drink!")
                self.make_random_recipe()
                return
            elif self.rotary_id < DataRepository.get_total_cocktails()["count"]:
                # print(f"Received request to make cocktail: {self.rotary_id}")
                recipe = DataRepository.get_recipe_by_cocktail_id(self.rotary_id)
                self.make_cocktail(recipe,self.rotary_id)
                DataRepository.put_device_history(14,action_id=2)

    def add_cocktail_to_queue(self,recipe,cocktail_id):
        self.queue.append([recipe,cocktail_id])
        cocktail = DataRepository.get_cocktail_by_id(cocktail_id)
        cocktail_name = cocktail["name"]
        # print(f"\nAdded {cocktail_name} to queue.")

    def make_next_cocktail_from_queue(self):
        self.waiting = False
        if len(self.queue) != 0:
            # print(f"\nMaking next cocktail in queue. {len(self.queue)-1} cocktails left in queue.")
            recipe = self.queue[0][0]
            cocktail_id = self.queue[0][1]
            self.make_cocktail(recipe,cocktail_id)
            self.remove_first_from_queue()
            return
        # print("\nQueue is now empty.")

    def remove_first_from_queue(self):
        if (len(self.queue) != 0):
            self.queue.pop(0)
    
    def clear_queue(self):
        self.queue = []

    def make_random_recipe(self):
        beverage_data = DataRepository.get_all_beverages()
        count_data = len(beverage_data)
        amount_of_ingredients = random.randint(2,4)
        ingredients = random.sample(range(1, count_data), amount_of_ingredients)
        volume = random.sample(range(40,80),amount_of_ingredients)
        recipe = [{'beverageId':ingredients[i],'volume':(volume[i])/1000} for i in range(amount_of_ingredients)]

        self.make_cocktail(recipe,0)

    def make_cocktail(self,recipe,cocktail_id):
        # print(recipe)
        if self.waiting == True:
            self.add_cocktail_to_queue(recipe,cocktail_id)
            return

        cocktail = DataRepository.get_cocktail_by_id(cocktail_id)
        cocktail_name = cocktail["name"]

        # print(f"\nMaking: {cocktail_name}")
        # print("The recipe is as follows:")
        SerialRepository.send_ser("Act:Start")
        for beverage in recipe:
            beverage_id = beverage["beverageId"]
            volume = beverage["volume"]*10**3
            beverage = DataRepository.get_beverage_by_id(beverage_id)
            beverage_name = beverage["beverageName"]
            # print(f"\t{volume} ml {beverage_name}")
            SerialRepository.send_ser(f"Act:{beverage_id}:{volume}")
            DataRepository.put_device_history(device_id=beverage_id+1,action_id=1,value=volume,comment=str(cocktail_name))
        
        SerialRepository.send_ser("Act:Fin")
        self.waiting = True
        DataRepository.put_cocktail_history(cocktail_id,str(cocktail_name))
 