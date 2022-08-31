### 
### 10M OF SOUND PLAYBACK PROGRAM FOR PHILIP VERMEULEN @ RIJKSMUSEUM TWENTE. 
### June, 2021 Mark Ridder
import threading, time, socket, datetime, json

# Set the to be loaded slots. Has to be full paths or else it won't start on boot! 
play1 = "SLOT_5.json"
play2 = "SLOT_5.json"

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

# UDP setup for listening
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 6006))

#load composition 1
print(f"opening {play1}")
f = open(play1, "r")
recording = json.loads(f.read())
rec_dict1 = {entry["time"]:entry["values"] for entry in recording}
last_time1 = list(recording)[-1]["time"]
print(f"{play1} is playing for {last_time1} seconds")

#load composition 2
print(f"opening {play2}")
f = open(play2, "r")
recording2 = json.loads(f.read())
rec_dict2 = {entry["time"]:entry["values"] for entry in recording2}
last_time2 = list(recording)[-1]["time"]
print(f"{play2} is playing for {last_time2} seconds")

# Define a function for the thread
def listening_thread():
    global data     # data needs to be defined as global inside the thread
    while True:
        data_raw, addr = sock.recvfrom(1024)
        data = data_raw.decode()    # My test message is encoded
        print(f"{CRED}{datetime.datetime.now().time()} UDP MESSAGE: {data}{CEND}")
        data_arr.append(data)
        print(f"{CRED}{datetime.datetime.now().time()} UDP ARRAY: {data_arr}{CEND}")

# Load the thread
try:
    threading.Thread(target=listening_thread).start()
except:
    print ("Error: unable to start thread")
    quit()

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
    if len(data_arr) >= 1 and playing == False:
        if data_arr[0].startswith("ROOM_6"):
            threading.Thread(target=player,
                             args=(rec_dict1, last_time1, play1),
                             kwargs={},
                        ).start()
        elif data_arr[0].startswith("ROOM_7") and playing == False:
            threading.Thread(target=player,
                             args=(rec_dict2, last_time2, play2),
                             kwargs={},
                        ).start()
    time.sleep(2)