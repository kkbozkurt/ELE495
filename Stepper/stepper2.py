# Import required libraries
import RPi.GPIO as GPIO
import time

# Define pin connections & motor's steps per revolution
dirPin = 17
stepPin = 18
stepsPerRevolution = 200

# Set up pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(stepPin, GPIO.OUT)
GPIO.setup(dirPin, GPIO.OUT)

def loop():
    # Set motor direction clockwise
    GPIO.output(dirPin, GPIO.HIGH)

    # Spin motor slowly
    for x in range(stepsPerRevolution):
        GPIO.output(stepPin, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(stepPin, GPIO.LOW)
        time.sleep(0.001)
    # time.sleep(1) # Wait a second

    # Set motor direction counterclockwise
    # GPIO.output(dirPin, GPIO.LOW)

    # # Spin motor quickly
    # for x in range(stepsPerRevolution):
    #     GPIO.output(stepPin, GPIO.HIGH)
    #     time.sleep(0.001)
    #     GPIO.output(stepPin, GPIO.LOW)
    #     time.sleep(0.001)
    # time.sleep(1) # Wait a second

# Run the loop function
while True:
    loop()
