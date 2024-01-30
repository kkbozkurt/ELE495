import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

control_pins = [17,27,22,10]

for pin in control_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)
  
halfstep_seq = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]

def ileri(tur_sayisi_i):
    control_pins = [17,27,22,10]
    for i in range(tur_sayisi_i):
      for halfstep in range(8):
        for pin in range(4):
          GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
        time.sleep(0.0005)
        
def geri(tur_sayisi_g):
    control_pins = [17,27,22,10]
    for i in range(tur_sayisi_g):
      for halfstep in range(8):
        for pin in range(4):
          GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
        time.sleep(0.0005)

while True:
    tur_sayisi_i=input("İleri yönde kac tur dönecek? \n ")
    ileri(int(tur_sayisi_i)*512)
    tur_sayisi_g=input("Geri yönde kac tur dönecek? \n ")
    geri(int(tur_sayisi_g)*512)
GPIO.cleanup()