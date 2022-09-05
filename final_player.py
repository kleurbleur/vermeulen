### 
### 10M OF SOUND PLAYBACK PROGRAM FOR PHILIP VERMEULEN @ RIJKSMUSEUM TWENTE. 
### June, 2021 Mark Ridder
import threading, time, datetime, json
from gpiozero import PWMOutputDevice, DigitalInputDevice


# Set the to be loaded slots. Has to be full paths or else it won't start on boot! 
play_pir = "/home/kb/Desktop/vermeulen/SLOT_1.json"
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


# the function that will spawn as a thread continiously checking the pir sensor
def pir_input():
    global pi, pir_sensor, play_button, addr, UDP_OUT_PORT
    print(f"{datetime.datetime.now().time()}: Detecting pir sensor")
    while True: 
        if pi:
            pir_sensor = play_button.value 
            if pir_sensor and DEBUG == 1 or pir_sensor and DEBUG == 4:
                print(f"{datetime.datetime.now().time()}: pir sensor: {pir_sensor}")
        else:
            time.sleep(40)   # DEBUG for non pi checking
            pir_sensor = random.getrandbits(1) # DEBUG for non pi checking
            print(f"{datetime.datetime.now().time()}: pir sensor: {pir_sensor}")
# start the pir sensor thread 
try:
    pir_sensor_worker = threading.Thread(target=pir_input)
    pir_sensor_worker.start()
except:
    print (f"{datetime.datetime.now().time()}: Error: unable to start PIR SENSOR thread. Exit.")
    quit()



# Check if there's something in the data_arr and if so start a thread according to that item
while True:
    if input1:
        print("play composition one")
