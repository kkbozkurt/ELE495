import RPi.GPIO as GPIO
import time

dir_pin = 27
step_pin = 17
steps_per_revolution = 200

# Initialize GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(dir_pin, GPIO.OUT)
GPIO.setup(step_pin, GPIO.OUT)

# Initialize timer
tim = GPIO.PWM(step_pin, 1000)

def step(t):
    global tim
    tim.ChangeFrequency(1000000//t)
    tim.start(50)
    time.sleep(0.001)
    tim.stop()

def rotate_motor(delay):
    # Set up timer for stepping
    tim.ChangeDutyCycle(50)
    tim.start(50)
    tim.ChangeFrequency(1000000//delay)

def loop():
    while True:
        # Set motor direction clockwise
        GPIO.output(dir_pin, GPIO.HIGH)

        # Spin motor slowly
        rotate_motor(2000)
        time.sleep(steps_per_revolution/1000)
        tim.stop()  # stop the timer
        time.sleep(1)

        # Set motor direction counterclockwise
        GPIO.output(dir_pin, GPIO.LOW)

        # Spin motor quickly
        rotate_motor(1000)
        time.sleep(steps_per_revolution/1000)
        tim.stop()  # stop the timer
        time.sleep(1)

if __name__ == '_main_':
    loop()