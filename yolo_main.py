import time
import Jetson.GPIO as GPIO
import os
from ultralytics import YOLO
import cv2 
import Jetson.GPIO as GPIO
import requests
from queue import Queue 
from threading import * 


def api_messaging():
        message_to_send = {
        "apiKey": '7baabcd4-1741-4c91-a5c1-9898b7af75eb',
        "message": "Metal Olmayan Çöp Tespit Edildi!, Yeşil Noktaya Götürülüyor.",
        "description": "Başarılı",
        "type": "info",  #info, error, warning or success
        }
        requests.post('https://api.mynotifier.app', message_to_send)

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
    GPIO.output(GPIO_dir, GPIO.LOW)

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
    path = os.getcwd() + "/camera/output/"
    if not os.path.exists(path):
        os.mkdir(path)
    path_output = path + str(time.time()) + ".jpg"
    # path_output = path + "deneme" + ".jpg"
    # capture the next image
    results = model.predict(image, show_labels=True, show_conf=True, save_txt=True)
    for result in results:
        for box in result.boxes:
            # boxes = result.boxes  # Boxes object for bounding box outputs
            print(box.conf)
            print(box.cls)
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        print(probs)
        result.save(filename='result.jpg')  # save to disk

    
GPIO.setmode(GPIO.BCM)

PIN_TRIGGER = 23
PIN_ECHO = 24

GPIO_dir = 25
GPIO_step = 9

step_time = 0.0030

model = YOLO('yolov5n.pt')

event = Event()
t1 = Thread(target=ultrasonic)
t2 = Thread(target=stepper)

t1.start() 
t2.start() 