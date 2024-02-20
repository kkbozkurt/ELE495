import RPi.GPIO as GPIO
import time
import os
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, Log, saveImageRGBA
from queue import Queue 
from threading import * 

GPIO.setmode(GPIO.BCM)

def ultrasonic():
    PIN_TRIGGER = 23
    PIN_ECHO = 24
    GPIO_step = 9

    GPIO.setup(PIN_TRIGGER, GPIO.OUT)
    GPIO.setup(PIN_ECHO, GPIO.IN)
    event.set()
    while True:
        GPIO.output(PIN_TRIGGER, GPIO.LOW)
        time.sleep(0.000002)
        GPIO.output(PIN_TRIGGER, GPIO.HIGH)
        time.sleep(0.000002)
        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        while GPIO.input(PIN_ECHO)==0:
            pass
        pulse_start_time = time.time()
    
        while GPIO.input(PIN_ECHO)==1:
            pass
        pulse_end_time = time.time()
    
        pulse_duration = pulse_end_time - pulse_start_time

        distance = (pulse_duration * 34444)/2

        if distance < 5 :
            print("Stopping motor...")
            print("Processing image...")
            event.clear()
            process_image()
            event.set()
            time.sleep(5)

        print ("Distance:",distance,"cm")
        time.sleep(0.05)

def stepper():

    GPIO_dir = 25
    GPIO_step = 9
        
    GPIO.setup(GPIO_dir, GPIO.OUT) 
    GPIO.setup(GPIO_step, GPIO.OUT)
    GPIO.output(GPIO_dir, GPIO.HIGH)

    while True:
        event.wait()
        while event.isSet():
            GPIO.output(GPIO_step, GPIO.HIGH)
            time.sleep(0.002)
            GPIO.output(GPIO_step, GPIO.LOW)
            time.sleep(0.002)
        time.sleep(5)
        # event.set()


input = videoSource("/dev/video0")
# load the object detection network
net = detectNet("ssd-mobilenet-v2", 0.25)

def process_image():
    while True:
        path = os.getcwd() + "/camera/output/"
        if not os.path.exists(path):
            os.mkdir(path)
        path_output = path + str(time.time()) + ".jpg"
        output = videoOutput(path_output)
        # capture the next image
        img = input.Capture()

        if img is None: # timeout
            continue  
            
        # detect objects in the image (with overlay)
        detections = net.Detect(img, overlay="box,labels,conf")

        # print the detections
        print("detected {:d} objects in image".format(len(detections)))

        for detection in detections:
            print(detection)

        # render the image
        output.Render(img)
        break
        # update the title bar
        # output.SetStatus("{:s} | Network {:.0f} FPS".format("ssd-mobilenet-v2", net.GetNetworkFPS()))

        # exit on when output and detections are created

event = Event()
t1 = Thread(target=ultrasonic)
t2 = Thread(target=stepper)
t3 = Thread(target=process_image)

t1.start() 
t2.start() 
#t3.start()
