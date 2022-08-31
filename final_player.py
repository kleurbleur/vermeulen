### 
### 10M OF SOUND PLAYBACK PROGRAM FOR PHILIP VERMEULEN @ RIJKSMUSEUM TWENTE. 
### June, 2021 Mark Ridder
import threading, time, datetime, json
from gpiozero import PWMOutputDevice, DigitalInputDevice


# Set the to be loaded slots. Has to be full paths or else it won't start on boot! 
play_pir = "/home/pi/Desktop/whos_afraid/PIR_SLOT.json"
# play_slow = "/home/pi/Desktop/whos_afraid/SLOW_SLOT.json" // only needed when there are two compositions apart. 

##
## AFTER THIS IS CODE. 
##

#Set console color for easier UDP income reading
CRED = '\033[91m'
CEND = '\033[0m'

# Declare variables 
data = ''   # Declare an empty variable
data_arr = [] 
playing = False


#load composition 1
print(f"opening {play1}")
f = open(play1, "r")
recording = json.loads(f.read())
rec_dict1 = {entry["time"]:entry["values"] for entry in recording}
last_time1 = list(recording)[-1]["time"]
print(f"{play1} is playing for {last_time1} seconds")



# Define a function for the composition playback
def player (dict, last_entry, slot):
    global playing
    playing = True
    print(f"last_entry from {slot}: {last_entry}")
    t0 = time.time()
    while True:
        t1 = time.time() - t0
        values = dict.get(round(t1, 5), None)
        if values:
            print(f"{datetime.datetime.now().time()} time: {round(t1, 5)}   port: {values['port']}  value: {values['value']}")
        if t1 >= last_entry:
            print(f"{datetime.datetime.now().time()} done playing {slot}")
            t0 = 0
            t1 = 0
            data_arr.clear()
            playing = False
            return         

# Check if there's something in the data_arr and if so start a thread according to that item
while True:
    if input1:
        print("play composition one")
