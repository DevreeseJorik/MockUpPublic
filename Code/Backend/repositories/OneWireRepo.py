from RPi import GPIO

class OneWire:
    def __init__(self, device_id="28-3c01d07567bf"): #28-031897793fdc for test tempsensor
        self.device_id = device_id
        self.filename = f'/sys/bus/w1/devices/{device_id}/w1_slave'

    def read_temp(self):
        print('\n*** Reading temperature **')
        sensor_file = open(self.filename, 'r')
        for line in sensor_file:
            if 't=' in line:
                line = line.strip("\n")
                line = line.split('t=')
                temperature = float(line[1])/1000
                print(f"Current temperature is: {temperature} °C")
        sensor_file.close()
        return temperature