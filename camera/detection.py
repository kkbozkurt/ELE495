import sys
import argparse

from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, Log, saveImageRGBA

# create video sources and outputs
input = videoSource("/dev/video0")
output = videoOutput("./camera/output/processed.jpg")
	
# load the object detection network
net = detectNet("ssd-mobilenet-v2", 0.5)

def process_image():
    while True:
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

        # update the title bar
        output.SetStatus("{:s} | Network {:.0f} FPS".format("ssd-mobilenet-v2", net.GetNetworkFPS()))

        # exit on when output and detections are created
        if output and detections:
            break

while True:
    process_image()