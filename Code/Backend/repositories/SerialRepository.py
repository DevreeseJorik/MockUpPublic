import time
import serial

ser = serial.Serial('/dev/ttyS0', 9600, timeout=2)
print(ser.name)

class SerialRepository:
    @staticmethod
    def get_ser():
        while True:
            try:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').rstrip()  # recieve data from arduino
                    time.sleep(0.001)
                    return line
            except UnicodeDecodeError:
                print("Unicode Error, arduino crashed...")
                return "crash"
                


                

    @staticmethod
    def send_ser(text=""):
        ser.write(f"{text}\n".encode('utf-8'))  # send data from pi