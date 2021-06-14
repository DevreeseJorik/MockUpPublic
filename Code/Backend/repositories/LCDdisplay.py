from RPi import GPIO
import time
from .DataRepository import DataRepository
from subprocess import check_output

GPIO.setwarnings(False)

class Display:
    def __init__(self, bit_amount=8, pins={"RS": 24, "E": 23}, DB_pins=[17, 27, 22, 5, 6, 13, 19, 26]):
        self.bit_amount = bit_amount
        self.pins = pins
        self.DB_pins = DB_pins
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pins["RS"], GPIO.OUT)
        GPIO.setup(self.pins["E"], GPIO.OUT)
        for pin in self.DB_pins:
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.output(self.pins["E"], GPIO.HIGH)

        self.init_lcd()
        self.display_drink_with_row_number(0)

    def init_lcd(self):
        self.send_instruction(0x38)
        self.send_instruction(0x0C)
        self.send_instruction(0x01)

    def clear_lcd(self):
        self.send_instruction(0x01)

    def set_data_bits(self, byte):
        mask = 0x1
        for i in range(0, 8):
            if (byte & mask) == 0:
                bit = 0
            else:
                bit = 1
            GPIO.output(self.DB_pins[i], bit)
            mask = mask << 1

    def send_instruction(self, value):
        GPIO.output(self.pins["RS"], GPIO.LOW)
        self.set_data_bits(value)
        time.sleep(0.002)

        GPIO.output(self.pins["E"], GPIO.LOW)
        time.sleep(0.002)
        GPIO.output(self.pins["E"], GPIO.HIGH)
        time.sleep(0.01)

    def send_character(self, value):
        if type(value) == str:
            value = ord(value)
        GPIO.output(self.pins["RS"], GPIO.HIGH)
        self.set_data_bits(value)
        time.sleep(0.002)

        GPIO.output(self.pins["E"], GPIO.LOW)
        time.sleep(0.002)
        GPIO.output(self.pins["E"], GPIO.HIGH)
        time.sleep(0.01)

    def display_string(self,text):
        for chr in text:
            self.send_character(chr)

    def go_to_address(self, row, position):
        if row == 1:
            byte = 0x0 | position
        else:
            byte = 0x40 | position
        instruction = byte | 0x80
        # print(f"position is at: {byte}")
        # print(f"Instruction is: {instruction}")
        self.send_instruction(instruction)

    def display_drink_with_row_number(self,cocktail_id):
        self.clear_lcd()
        cocktail = DataRepository.get_cocktail_by_id(cocktail_id)
        cocktail_name = cocktail["name"]
        self.go_to_address(1,0)
        self.display_string(cocktail_name)
        self.go_to_address(2,0)
        self.display_string(str(cocktail_id))
        
    def display_extra_screen(self,id):
        print(id)
        self.clear_lcd()
        requested_ip = check_output(['hostname', '--all-ip-addresses']).decode('utf-8').strip()
        status_message_l1 = "E" + requested_ip.split(" ")[0]
        status_message_l2 = "W" + requested_ip.split(" ")[1]
        print(status_message_l1, status_message_l2)
        self.go_to_address(1,0)
        self.display_string(status_message_l1)
        self.go_to_address(2,0)
        self.display_string(status_message_l2)
        self.go_to_address(2,0)
        

    def scroll_text(self, line_choice, cursor_position, input_string, delay):
        stop = ""
        counter = 0
        while stop == "":
            time.sleep(delay)
            self.go_to_address(line_choice, cursor_position)
            if len(input_string) - counter > 16:
                temp_string = input_string[counter:counter+16]
            else:
                temp_string = input_string[counter:]
            if len(temp_string) == 16:
                for char in temp_string:
                    # time.sleep(0.02)
                    self.send_character(ord(char))
                counter = (counter + 1) % (len(input_string))
            else:
                counter = 0




if __name__ == '__main__':
    GPIO.setwarnings(False)
    display = Display()
    display.setup()
    display.init_lcd()
    try:
        while True:
            display.go_to_address(1,0)
            display.display_string("Test")
            print("test")
            time.sleep(6)
    except Exception as e:
        print(e)