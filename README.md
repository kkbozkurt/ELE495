# ELE495
## ELE495 Final Project Repo

### Introduction

The aim of the graduation project is to realize a conveyor belt product identification system. With the camera connection to be positioned on the conveyor system, the selected products should be identified as product types and numbers. After this process, the conveyor belt should continue to move forward and the product type and number information should be sent to the phone.

![alt text](conveyor_belt.png)

To start our program first we need to overclock our Jetson Nano developer kit in order to use our ultrasonic module. To do that we enter the "$sudo jetson_clocks" command in our terminal.

``` $sudo jetson_clocks ```

After entering this prompt we can now start our program. Our python file is using the version 3.9 so we have to start it by calling "$python3.9". To start our program you should have root priviliges because our GPIO library needs to access to the pins and we can achieve this by adding sudo command before calling our python interpreter.

``` $sudo python3.9 yolo_main.py ```

After running the code, the program should start automatically.