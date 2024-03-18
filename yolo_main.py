import time
import Jetson.GPIO as GPIO
import os
from ultralytics import YOLO
import cv2 
import Jetson.GPIO as GPIO
import requests
from queue import Queue 
from threading import Thread, Event


def api_messaging(message_to_send):
        message = {
        "apiKey": '7baabcd4-1741-4c91-a5c1-9898b7af75eb',
        "message": message_to_send,
        "description": "Başarılı",
        "type": "info",  #info, error, warning or success
        }
        requests.post('https://api.mynotifier.app', message)

def ultrasonic():

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
            for i in range(600):
                GPIO.output(GPIO_step, GPIO.HIGH)
                time.sleep(step_time)
                GPIO.output(GPIO_step, GPIO.LOW)
                time.sleep(step_time)
                print("Steps count {}".format(i+1), end="\r", flush=True)
            event.set()

        print ("Distance:",distance,"cm")
        time.sleep(0.05)

def stepper():
        
    GPIO.setup(GPIO_dir, GPIO.OUT) 
    GPIO.setup(GPIO_step, GPIO.OUT)
    GPIO.output(GPIO_dir, GPIO.HIGH)

    while True:
        event.wait()
        while event.isSet():
            GPIO.output(GPIO_step, GPIO.HIGH)
            time.sleep(step_time)
            GPIO.output(GPIO_step, GPIO.LOW)
            time.sleep(step_time)
        # event.set()


def process_image():
    cam = cv2.VideoCapture("/dev/video0") 
    result, image = cam.read() 
    # capture the next image
    results = model.predict(image, show_labels=True, show_conf=True, save_txt=True)
    detected_objects_image = {"Unknown": 0}
    for result in results:
        for box in result.boxes:
            # boxes = result.boxes  # Boxes object for bounding box outputs
            print(box.conf.item())
            if box.conf.item() < 0.35:
                detected_objects.update({"Unknown": detected_objects.get("Unknown") + 1})
                detected_objects_image.update({"Unknown": detected_objects_image.get("Unknown") + 1})
            else:
                # Total Detected Object

                if not detected_objects.get(model.names[box.cls.item()], False):
                    detected_objects.update({model.names[box.cls.item()]: 1})
                else:
                    detected_objects.update({model.names[box.cls.item()]: detected_objects.get(model.names[box.cls.item()]) + 1})
                # Objects Detected in Image
                    
                if not detected_objects_image.get(model.names[box.cls.item()], False):
                    detected_objects_image.update({model.names[box.cls.item()]: 1})
                else:
                    detected_objects_image.update({model.names[box.cls.item()]: detected_objects_image.get(model.names[box.cls.item()]) + 1})
        result.save(filename='result.jpg')  # save to disk
    # print(detected_objects)
    # print(detected_objects_image)
    message_to_send = ""
    for i, (key, value) in enumerate(detected_objects_image.items()):
        message_to_send += str(value) + " " + key + ", "
    message_to_send += "detected! \nTotal "
    for i, (key, value) in enumerate(detected_objects.items()):
        message_to_send += str(value) + " " + key + ", "
    message_to_send += "detected!\n"
    print(message_to_send)
    api_messaging(message_to_send)

    
GPIO.setmode(GPIO.BCM)

PIN_TRIGGER = 23
PIN_ECHO = 24

GPIO_dir = 25
GPIO_step = 9

step_time = 0.0030

model = YOLO('yolov5su.pt')

detected_objects = {"Unknown": 0}

event = Event()
t1 = Thread(target=ultrasonic)
t2 = Thread(target=stepper)

t1.start() 
t2.start() 