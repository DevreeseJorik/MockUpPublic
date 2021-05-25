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


def lees_knop(pin):
    if knop1.pressed:
        print("**** button pressed ****")
        if GPIO.input(led3) == 1:
            switch_light({'lamp_id': '3', 'new_status': 0})
        else:
            switch_light({'lamp_id': '3', 'new_status': 1})


knop1.on_press(lees_knop)


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
def all_out():
    while True:
        print('*** We zetten alles uit **')
        DataRepository.update_status_alle_lampen(0)
        GPIO.output(led3, 0)
        status = DataRepository.read_status_lampen()
        socketio.emit('B2F_status_lampen', {'lampen': status})
        time.sleep(15)


thread = threading.Timer(15, all_out)
thread.start()


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
    status = DataRepository.read_status_lampen()
    emit('B2F_status_lampen', {'lampen': status}, broadcast=True)


@socketio.on('F2B_switch_light')
def switch_light(data):
    # Ophalen van de data
    lamp_id = data['lamp_id']
    new_status = data['new_status']
    print(f"Lamp {lamp_id} wordt geswitcht naar {new_status}")

    # Stel de status in op de DB
    res = DataRepository.update_status_lamp(lamp_id, new_status)

    # Vraag de (nieuwe) status op van de lamp en stuur deze naar de frontend.
    data = DataRepository.read_status_lamp_by_id(lamp_id)
    socketio.emit('B2F_verandering_lamp', {'lamp': data}, broadcast=True)

    # Indien het om de lamp van de TV kamer gaat, dan moeten we ook de hardware aansturen.
    if lamp_id == '3':
        print(f"TV kamer moet switchen naar {new_status} !")
        GPIO.output(led3, new_status)

# ANDERE FUNCTIES


if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')
