#pylint:skip-file
from RPi import GPIO

class Pcf8574:    
    def __init__(self,SDA,SCL,address=0x3F):
        self.SDA = SDA        
        self.SCL = SCL        
        self.address = address & 0x7F        
        self.setup()    
        
    @property    
    def address(self):        
        return self.__address    
    
    @address.setter    
    def address(self, value):        
        self.__address = value    


    # __ double underscore => private method, enkel zichtbaar in de klasse zelf    
    def setup(self):        
        GPIO.setmode(GPIO.BCM)        
        for pin in [self.SDA, self.SCL]:            
            GPIO.setup(pin, GPIO.OUT)    
    
    def start_conditie(self):        
        print("start")        
        GPIO.output(self.SDA, GPIO.HIGH)        
        GPIO.output(self.SCL, GPIO.HIGH)        
        GPIO.output(self.SDA, GPIO.LOW)        
        GPIO.output(self.SCL, GPIO.LOW)    

    def stop_conditie(self):        
        print("stop")        
        GPIO.output(self.SDA, GPIO.LOW)
        GPIO.output(self.SCL, GPIO.HIGH)        
        GPIO.output(self.SDA, GPIO.HIGH)    
        
    def write_bit(self,bit):        
        GPIO.output(self.SDA, bit)        
        GPIO.output(self.SCL, GPIO.HIGH)        
        GPIO.output(self.SCL, GPIO.LOW)        
        GPIO.output(self.SDA, GPIO.LOW)   
    
    def ack(self):        
        GPIO.setup(self.SDA, GPIO.IN, GPIO.PUD_UP)        
        GPIO.output(self.SCL, GPIO.HIGH)        
        ackbit = GPIO.input(self.SDA)        
        GPIO.output(self.SCL, GPIO.LOW)        
        GPIO.setup(self.SDA, GPIO.OUT)        
        print("ack {0}".format(ackbit))        
        if ackbit:            
            print("verkeerd adres!")            
            return False        
        else : return True    
        
    def write_byte(self,byte):        
        print(f"write_byte : {byte}")        
        mask = 0x80        
        for i in range(0, 8):            
            if byte & mask == 0:                
                self.write_bit(False)            
            else:                
                self.write_bit(True)            
            mask >>= 1    
    
    def write_outputs(self,data: int):        
        address_write = self.address <<1      
        GPIO.output(self.SCL, GPIO.LOW)
        data = data & 0xFF        
        self.start_conditie()        
        self.write_byte(address_write)        
        self.ack()        
        self.write_byte(data)        
        self.ack()        
        self.stop_conditie()    

    def check_address(self):        
        address_write = self.address << 1        
        self.start_conditie()        
        self.write_byte(address_write)        
        if not self.ack():  #0 => ok            
            return "Adres {0} is ok".format(self.address)        
        else : return "Adres {0} is niet gevonden".format(self.address)    
            
    @staticmethod    
    def search_addresses(SDA,SCL):        
        addresses = []        
        i2cdev = Pcf8574(SDA,SCL)        
        for i in range(0x20,0x80, 2):            
            i2cdev.address = i <<1            
            i2cdev.start_conditie()            
            i2cdev.write_byte(i)            
            if  i2cdev.ack():                
                addresses.append(i>>1)            
                i2cdev.stop_conditie()        
                return addresses 
                
    #deze code wordt niet uitgevoerd als ze wordt aangeroepen vanuit een anderefile
    
    if __name__ == "__main__":    
        SDA = 21
        SCL = 6    
        Pcf8574 = Pcf8574(SDA,SCL,0x39)
        my_address = Pcf8574.search_addresses(SDA,SCL)    
        print()    
        print("volgende adressen gevonden :")    
        print(my_address)    
        print("test om alles op 1 te zetten")    
        mypcf = Pcf8574(SDA,SCL,my_address[0])    
        mypcf.write_outputs(255)      
