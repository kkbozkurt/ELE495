# ELE495
ELE495 Final Project Repo

To start our program first we need to overclock our Jetson Nano developer kit in order to use our ultrasonic module. To do that we enter the "$sudo jetson_clocks" command in our terminal.
``` $sudo jetson_clocks ```
After entering this prompt we can now start our program. Our python file is using the version 3.9 so we have to start it by calling "$python3.9". To start our program you should have root priviliges because our GPIO library needs to access to the pins and we can achieve this by adding sudo command before calling our python interpreter.
``` $sudo python3.9 yolo_main.py ```
After running the code, the program should start automatically.