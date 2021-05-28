import time
from RPi import GPIO

# # default pin numbers (BCM) - pas aan indien nodig
# DS = 17  # serial data
# OE = 27  # output enable (active low)
# STCP = 22  # storage register clock pulse
# SHCP = 6  # shift register clock pulse
# MR = 5  # master reset (active low)


delay = 0.001


class ShiftRegister:
    def __init__(self, ds_pin= 17, shcp_pin=5, stcp_pin= 22 , mr_pin=6, oe_pin=27):

        self.ds_pin = ds_pin
        self.shcp_pin = shcp_pin
        self.stcp_pin = stcp_pin
        self.mr_pin = mr_pin
        self.oe_pin = oe_pin
        self.value_pumps = 0x0
        self.amount_pumps = 6

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([self.ds_pin, self.oe_pin, self.shcp_pin,
                    self.stcp_pin, self.mr_pin], GPIO.OUT, initial=GPIO.LOW)
        GPIO.output(self.mr_pin, GPIO.HIGH)
        self.write_byte(0x0)

    def write_one_bit(self, value):
        GPIO.output(self.ds_pin, value)
        time.sleep(delay)
        GPIO.output(self.shcp_pin, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(self.shcp_pin, GPIO.LOW)

    def copy_to_storage_register(self):
        GPIO.output(self.stcp_pin, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(self.stcp_pin, GPIO.LOW)
        time.sleep(delay)

    def write_byte(self, value):
        mask = 0x80
        for i in range(0, 8):
            if (value & (mask >> i)) == 0:
                bit = 0
            else:
                bit = 1
            self.write_one_bit(bit)
        time.sleep(0.001)
        self.copy_to_storage_register()

    @property
    def output_enabled(self):
        return not GPIO.input(self.oe_pin)

    @output_enabled.setter
    def output_enabled(self, value):
        GPIO.output(self.oe_pin, not value)

    def reset_shift_register(self):
        GPIO.output(self.mr_pin, GPIO.LOW)
        time.sleep(delay)
        GPIO.output(self.mr_pin, GPIO.HIGH)
        time.sleep(delay)

    def reset_storage_register(self):
        self.reset_shift_register()
        self.copy_to_storage_register()

    def change_state_pump(self,id,state):
        mask = 0
        for i in range(8):
            if i == id:
                mask = mask | 0 << i
            else:
                mask = mask | 1 << i

        value = state<<id
        # print(bin(value))
        # print("Mask", mask)
        self.value_pumps = (self.value_pumps & mask) | value
        # print(bin(self.value_pumps))
        self.write_byte(self.value_pumps)

    def set_all_pumps(self,state=1):
        value = 0
        if state in [0,1]:
            for i in range(self.amount_pumps):
                value | state << i
            self.value_pumps = value
            self.write_byte(self.value_pumps)
            print(self.vale)
        else: 
            return "state must be 0 or 1"

