import time
from RPi import GPIO
from helpers.klasseknop import Button
import threading
import serial

from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify
from repositories.DataRepository import DataRepository

import random

# Code voor Hardware
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# led3 = 21
# knop1 = Button(20)

sensor_file_name = '/sys/bus/w1/devices/28-031897793fdc/w1_slave'
sensor_file = open(sensor_file_name, 'r')

ser = serial.Serial('/dev/ttyS0', 9600, timeout=2)
print(ser.name)

# GPIO.setup(led3, GPIO.OUT)
# GPIO.output(led3, GPIO.LOW)
# Code voor Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,
                    engineio_logger=False, ping_timeout=1)

CORS(app)


@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)

# SERIAL 

def get_ser():
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()  # recieve data from arduino
            if "Val" in line:
                print(f"\nReceiving Serial:\n{line}")
            time.sleep(0.001)


def send_ser(text=""):
    ser.write(f"{text}\n".encode('utf-8'))  # send data from pi




# START THREAD

def read_temp():
        print('\n*** Reading temperature **')
        sensor_file = open(sensor_file_name, 'r')
        for line in sensor_file:
            if 't=' in line:
                line = line.strip("\n")
                line = line.split('t=')
                temperatuur = float(line[1])/1000
                print(f"De temperatuur is: {temperatuur}° Celsius")
        sensor_file.close()
        return temperatuur

def slow_loop():
    while True:
        temp_val = read_temp()
        DataRepository.put_device_history(1,action_id=None,value=temp_val,comment=None)
        send_ser("Sen:1")
        time.sleep(10)
        


thread = threading.Timer(10, slow_loop)
thread.start()

thread2 = threading.Timer(0.001, get_ser)
thread2.start()

print("**** Program started ****")

# API ENDPOINTS

@app.route('/')
def hallo():
    return "Server is running, no API endpoints available."


@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # # Send to the client!

@socketio.on("F2B_request_data")
def return_main_data(data):
    print(data["url"])
    if data["url"] == "Menu.html":
        cocktails = DataRepository.read_all_cocktails()
        emit('B2F_cocktails', {'cocktails': cocktails})
    if data["url"] == "Stats.html":
        # print(data["limit"])
        data = DataRepository.get_latest_rows_device_history(data["limit"])
        emit('B2F_history_device', {'history': data})

@socketio.on("F2B_history_device")
def return_history_device(data):
    time.sleep(10)
    data = DataRepository.get_latest_rows_device_history(data["limit"])
    emit('B2F_history_device', {'history': data})

@socketio.on('F2B_request_cocktail')
def listen_to_cocktail_request(data):
    cocktail_id = data["cocktail_id"]

    if str(cocktail_id) == "random":
        print("\nUser chose random drink!")
        make_random_recipe()
        return

    # print(f"Received request to make cocktail: {cocktail_id}")
    recipe = DataRepository.get_recipe_by_cocktail_id(cocktail_id)
    make_cocktail(recipe,cocktail_id)

# Other functions

def make_random_recipe():
    beverage_data = DataRepository.get_all_beverages()
    count_data = len(beverage_data)
    amount_of_ingredients = random.randint(2,4)
    ingredients = random.sample(range(0, count_data), amount_of_ingredients)
    volume = random.sample(range(40,80),amount_of_ingredients)
    json_ = {ingredients[i]:volume[i] for i in range(amount_of_ingredients)}
    print(json_)

def make_cocktail(recipe,cocktail_id):
    comment = "Null"
    cocktail = DataRepository.get_cocktail_by_id(cocktail_id)
    cocktail_name = cocktail["name"]
    print(f"\nUser requested {cocktail_name}")
    print("The recipe is as follows:")
    for element in recipe:
        beverage_id = element["beverageId"]
        volume = element["volume"]
        beverage = DataRepository.get_beverage_by_id(beverage_id)
        beverage_name = beverage["beverageName"]
        print(f"\t{volume*10**3} ml {beverage_name}")

    # once cocktail has been confirmed finished:
    # DataRepository.put_cocktail_history(cocktail_id,comment)

if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')
