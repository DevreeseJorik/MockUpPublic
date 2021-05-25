import time
from RPi import GPIO
from helpers.klasseknop import Button
import threading

from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify
from repositories.DataRepository import DataRepository


# Code voor Hardware
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

led3 = 21
knop1 = Button(20)

GPIO.setup(led3, GPIO.OUT)
GPIO.output(led3, GPIO.LOW)
# Code voor Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,
                    engineio_logger=False, ping_timeout=1)

CORS(app)


@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)


# START een thread op. Belangrijk!!! Debugging moet UIT staan op start van de server, anders start de thread dubbel op
# werk enkel met de packages gevent en gevent-websocket.
# def all_out():
#     while True:
#         print('*** We zetten alles uit **')
#         GPIO.output(led3, 0)
#         time.sleep(15)

# thread = threading.Timer(15, all_out)
# thread.start()


print("**** Program started ****")

# API ENDPOINTS


@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."


@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # # Send to the client!
    # vraag de status op van de lampen uit de DB
    cocktails = DataRepository.read_all_cocktails()
    # print(cocktails)
    emit('B2F_cocktails', {'cocktails': cocktails}, broadcast=True)

@socketio.on('F2B_request_cocktail')
def listen_to_cocktail_request(data):
    cocktail_id = data["cocktail_id"]
    # print(f"Received request to make cocktail: {cocktail_id}")
    recipe = DataRepository.get_recipe_by_cocktail_id(cocktail_id)
    make_cocktail(recipe,cocktail_id)
    
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

# @socketio.on('F2B_switch_light')
# def switch_light(data):
#     # Ophalen van de data
#     lamp_id = data['lamp_id']
#     new_status = data['new_status']
#     print(f"Lamp {lamp_id} wordt geswitcht naar {new_status}")

#     # Stel de status in op de DB
#     res = DataRepository.update_status_lamp(lamp_id, new_status)

#     # Vraag de (nieuwe) status op van de lamp en stuur deze naar de frontend.
#     data = DataRepository.read_status_lamp_by_id(lamp_id)
#     socketio.emit('B2F_verandering_lamp', {'lamp': data}, broadcast=True)

#     # Indien het om de lamp van de TV kamer gaat, dan moeten we ook de hardware aansturen.
#     if lamp_id == '3':
#         print(f"TV kamer moet switchen naar {new_status} !")
#         GPIO.output(led3, new_status)

# ANDERE FUNCTIES


if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')
