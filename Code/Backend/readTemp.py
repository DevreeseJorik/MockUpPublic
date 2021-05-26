from RPi import GPIO
import time
motor = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(motor, GPIO.OUT)
# pwm_motor = GPIO.PWM(motor, 1000)

# pwm_motor.start(0)


sensor_file_name = '/sys/bus/w1/devices/28-031897793fdc/w1_slave'
sensor_file = open(sensor_file_name, 'r')

# gevraagde_temperatuur = float(input("Geef een temperatuur op om te regelen:"))


# def calc_duty_cycle(tempverschil):
#     temp_conv = [0, 30, 50]
#     converter_tempverschil = 0
#     duty_cycle = 100
#     for i in range(len(temp_conv)):
#         converter_tempverschil += 2
#         if tempverschil <= converter_tempverschil:
#             duty_cycle = temp_conv[i]
#             break
#     return duty_cycle


try:
    prev_duty_cycle = 0
    while True:
        sensor_file = open(sensor_file_name, 'r')
        for line in sensor_file:
            if 't=' in line:
                line = line.strip("\n")
                line = line.split('t=')
                temperatuur = float(line[1])/1000
                print(f"De temperatuur is: {temperatuur}° Celsius")

        # duty_cycle = calc_duty_cycle(temperatuur-gevraagde_temperatuur)
        # print(f"De duty cycle bedraagt: {duty_cycle}")
        # if duty_cycle != prev_duty_cycle:
        #     pwm_motor.ChangeDutyCycle(duty_cycle)

        sensor_file.close()
        time.sleep(1)
        # prev_duty_cycle = duty_cycle

except KeyboardInterrupt as e:
    print(e)
finally:
    print("Script stopped.")

sensor_file.close()
