import smbus
import time
 
LED1 = 0x01
bus = smbus.SMBus(1)

try:
    while True:
        for i in range(6):
            state = 1 << i
            print(state)
            bus.write_byte(0x38,state^0xFF)
            time.sleep(1)
except KeyboardInterrupt:
    bus.write_byte(0x38,0x0^0xFF)


# from repositories.pcfRepo import Pcf8574

# SDA = 21
# SCL = 6    
# Pcf8574 = Pcf8574(SDA,SCL,0x20)
# my_address = Pcf8574.search_addresses(SDA,SCL)    
# print()    
# print("volgende adressen gevonden :")    
# print(my_address)    
# print("test om alles op 1 te zetten")    
# mypcf = Pcf8574(SDA,SCL,my_address[0])    
# mypcf.write_outputs(255) 
