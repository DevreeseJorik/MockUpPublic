import time
import threading
from RPi import GPIO

from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify

from repositories.DataRepository import DataRepository
from repositories.Cocktail import Cocktail
# from repositories.Rotary import Rotary
from repositories.OneWire import OneWire
from repositories.SerialRepository import SerialRepository
# from repositories.LCDdisplay import Display
# from helpers.klasseknop import Button

GPIO.setwarnings(False)

one_wire = OneWire()
# display = Display()
cocktail = Cocktail()

# Code voor Hardware
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


# Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,
                    engineio_logger=False, ping_timeout=1)
CORS(app)

@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)

# Start Thread

def slow_loop():
        while True:
            temp_val = one_wire.read_temp()
            # DataRepository.put_device_history(1,action_id=None,value=temp_val,comment=None)
            # SerialRepository.send_ser("Sen:1")
            time.sleep(10)

def fast_loop():
        while True:
            line = SerialRepository.get_ser()
            if line == "First glass put down":
                cocktail.waiting = False
                cocktail.make_next_cocktail_from_queue()

            if "Val" in line:
                print(f"\nReceiving Serial:\n{line}")

            if line == "Finished cocktailprocess":
                print("Cocktailprocess finished")
                cocktail.waiting = False
                print(f"Drink has been completed")
                cocktail.make_next_cocktail_from_queue()
                SerialRepository.send_ser("Sen:All")

            if "Sensor" in line:
                split_line = line.split(":")
                print(split_line)
                id = split_line[1]   # add 6 when sending to database, first 6 are other devices
                value = split_line[2] + cocktail.beveragevolumes[id]
                DataRepository.put_device_history(id+6,action_id=None,value=value,comment=None)
            
                

thread = threading.Timer(10, slow_loop)
thread.start()

thread2 = threading.Timer(0.001, fast_loop)
thread2.start()

print("**** Program started ****")

# API endpoints

@app.route('/')
def hallo():
    return "Server is running, no API endpoints available."

@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # # Send to the client!

@socketio.on("F2B_request_data")
def return_main_data(data):
    # print(data["url"])

    if data["url"] == "Menu.html":
        cocktails = DataRepository.read_all_cocktails()
        emit('B2F_cocktail_menu', {'cocktails': cocktails})
        print("Cocktail data sent")

    if data["url"] == "Stats.html":
        temperature = DataRepository.get_latest_rows_device_history(1,'1')
        emit('B2F_current_temperature',round(temperature[0]['value'],2))

        pumps_volume = DataRepository.get_all_beverages()
        emit('B2F_current_volume', pumps_volume)

        latest_cocktail = DataRepository.get_latest_created_cocktails(1)
        emit('B2F_latest_cocktail',latest_cocktail)

        cocktail_history = DataRepository.get_cocktail_history()
        emit('B2F_cocktail_history',cocktail_history)

        count_cocktails = DataRepository.get_cocktail_count()
        emit('B2F_cocktail_popularity',count_cocktails)

        temperature_history = DataRepository.get_latest_rows_sensor_history(15,'1')

        volume_history = DataRepository.get_latest_rows_sensor_history(15,'2,3,4,5,6,7')
        emit('B2F_sensor_history',{'temperature':temperature_history,'volume':volume_history})

        actuator_history = DataRepository.get_latest_rows_actuator_history(20)
        emit('B2F_actuator_history', actuator_history)
        





@socketio.on("F2B_history_device")
def return_history_device(data):
    time.sleep(10)
    data = DataRepository.get_latest_rows_device_history(data["limit"])
    emit('B2F_history_device', {'history': data})

@socketio.on('F2B_request_cocktail')
def listen_to_cocktail_request(data):
    cocktail_id = data["cocktail_id"]

    if str(cocktail_id) in ["0","random"]:
        print("\nUser chose random drink!")
        cocktail.make_random_recipe()
        return

    # print(f"Received request to make cocktail: {cocktail_id}")
    recipe = DataRepository.get_recipe_by_cocktail_id(cocktail_id)
    cocktail.make_cocktail(recipe,cocktail_id)

# Other functions (redundant: moved to own repositories)

if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')