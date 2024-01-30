import RPi.GPIO as GPIO

# import the library
from RpiMotorLib import RpiMotorLib

#define GPIO pins

GPIO_pins = (-1, -1, -1) # Microstep Resolution MS1-MS3 -> GPIO Pin
direction = 6       # Direction -> GPIO Pin
step = 13      # Step -> GPIO Pin

# Declare an named instance of class pass GPIO pins numbers
mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")


# call the function, pass the arguments
mymotortest.motor_go(False, "Full" , 200, 0.01, True, .05)

# GPIO.cleanup()  