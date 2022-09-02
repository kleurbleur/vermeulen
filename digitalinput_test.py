from gpiozero import DigitalInputDevice
from time import sleep

play_button = DigitalInputDevice("BOARD40", pull_up=True)

while True:
    print(play_button.value)
    sleep(0.05)