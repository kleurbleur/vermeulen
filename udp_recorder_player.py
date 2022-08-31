# SET TO TRUE WHEN RUNNING ON PI
pi = True


from dis import show_code
import time,socket,datetime,json, threading
if pi:
    from gpiozero import PWMOutputDevice, DigitalInputDevice
else:
    import random



# Set the incoming UPD port here
UDP_PORT = 6006
# Set the outgoing UDP port here
UDP_OUT_PORT = 6007


# Set the debug level
# 0 = no debug messages, 1 = PIR sensor, 2 = inverter messages, 3 = UDP, 4 = all
DEBUG = 0


# Set the to be loaded slots. 
# Has to be full paths or else it won't start on boot! 
if pi:
    play_pir = "/home/pi/Desktop/whos_afraid/PIR_SLOT.json"
    play_slow = "/home/pi/Desktop/whos_afraid/SLOW_SLOT.json"
    path_settings = "/home/pi/Desktop/whos_afraid/settings.json"
else:
    play_pir = "PIR_SLOT.json"
    play_slow = "SLOW_SLOT.json"
    path_settings = "settings.json"    





# Set the gpio out and in. 
# Check pinout.xyz for the black pin numbers aka the board numbers these are used as strings e.g. "BOARD18".
# BCM numbering are usable as integers.  
if pi:
    inv_1 = PWMOutputDevice(7)
    inv_2 = PWMOutputDevice(8)
    inv_3 = PWMOutputDevice(25)
    inv_4 = PWMOutputDevice(24)
    inv_5 = PWMOutputDevice(23)
    inv_6 = PWMOutputDevice(18)
    inv_7 = PWMOutputDevice(3)
    inv_8 = PWMOutputDevice(4)
    inv_9 = PWMOutputDevice(17)
    inv_10 = PWMOutputDevice(27)
    inv_11 = PWMOutputDevice(22)
    inv_12 = PWMOutputDevice(10)
    inv_13 = PWMOutputDevice(9)
    inv_14 = PWMOutputDevice(11)
    inv_15 = PWMOutputDevice(5)
    inv_16 = PWMOutputDevice(6)
    inv_17 = PWMOutputDevice(13)
    inv_18 = PWMOutputDevice(19)
    pir = DigitalInputDevice(26)

if pi:
    print(f"Listening on port {UDP_PORT} for UDP messages from the recorder software.") 
    print("My IP address was hard coded during the exhibition in Stedelijk Museum Schiedam at 192.168.178.49.")
    print("Commands are 'REC filename.json', 'EDIT', 'SHOW', 'STOP' and 'EXIT'.")
    print("Sending values when in EDIT mode works if inverters are connected and programmed on 0 - 3.3V input.")
else:
    print(f"Listening on port {UDP_PORT} for UDP messages from the recorder software.") 
    print("Commands are 'REC filename.json', 'EDIT', 'SHOW', 'STOP' and 'EXIT'.")
    print("Sending values when in EDIT mode works if inverters are connected and programmed on 0 - 3.3V input.")    


# Declare variables 
playing = False
pir_sensor = False
pir_sensor_active = False
standard_mode = False
stop_thread_slow = False
stop_thread_pir = False
interaction_stop = False
edit_stop = False
play_mode = 0
play_mode_active = False


# UDP setup for listening
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setblocking(1)
sock.bind(('', UDP_PORT))
#Set console color for easier UDP income reading
CRED = '\033[91m'
CEND = '\033[0m'



#load composition pir
def composition_load_pir():
    global play_pir, recording_pir,rec_dict_pir, last_time_pir
    print(f"{datetime.datetime.now().time()}: opening {play_pir}")
    try:
        f = open(play_pir, "rb")
    except:
        print("The PIR SLOT does not contain a file.")
    else:
        one_char = f.read(1) # read first character to check if it contains data 
        if one_char:
            f.seek(-1, 1)   # go back one character to make sure json.loads still understand the format
            recording_pir = json.loads(f.read())
            rec_dict_pir = {entry["time"]:entry["values"] for entry in recording_pir}
            # if DEBUG == 2 or DEBUG == 3:
            #     print(rec_dict_pir) 
            last_time_pir = list(recording_pir)[-1]["time"]
            f.close()
            print(f"{datetime.datetime.now().time()}: {play_pir} is {last_time_pir} seconds long")
        elif not one_char:
            print("The slot does not contain any data.")
composition_load_pir()

#load composition slow
def composition_load_slow():
    global play_slow, recording_slow, rec_dict_slow, last_time_slow
    print(f"{datetime.datetime.now().time()}: opening {play_slow}")
    try:
        f = open(play_slow, "rb")
    except:
        print("The SLOW SLOT does not contain a file.")
    else:
        one_char = f.read(1) # read first character to check if it contains data 
        if one_char:        #if it has at least 1 character
            f.seek(-1, 1)   # go back one character to make sure json.loads still understand the format
            recording_slow = json.loads(f.read())
            rec_dict_slow = {entry["time"]:entry["values"] for entry in recording_slow}
            # if DEBUG == 2 or DEBUG == 3:
            #     print(rec_dict_slow) 
            last_time_slow = list(recording_slow)[-1]["time"]
            f.close()
            print(f"{datetime.datetime.now().time()}: {play_slow} is {last_time_slow} seconds long")
        elif not one_char:
            print("The SLOW SLOT does not contain any data.")   
composition_load_slow()


# the function that will be the player for both compositions
def player (thread_name, dict, last_entry, slot):
    global stop_thread_slow, stop_thread_pir
    global pir_sensor_active, standard_mode, playing
    global pi
    playing = True
    print(f"{datetime.datetime.now().time()}: Thread {thread_name} Starting composition from {slot} and will be playing for: {last_entry}s")
    t0 = time.time()
    while True:
        t1 = time.time() - t0
        t_check = round(t1, 3)
        values = dict.get(t_check, None)
        if stop_thread_pir or stop_thread_slow: 
                break
        if values:
            if DEBUG == 2 or DEBUG == 4:
                print(f"{datetime.datetime.now().time()}: {thread_name} time: {t_check} values: {values}")   
            if pi:    
                inv_1.value = values[0]
                inv_2.value = values[1]
                inv_3.value = values[2]
                inv_4.value = values[3]
                inv_5.value = values[4]
                inv_6.value = values[5]
                inv_7.value = values[6]
                inv_8.value = values[7]
                inv_9.value = values[8]
                inv_10.value = values[9]
                inv_11.value = values[10]
                inv_12.value = values[11]
                inv_13.value = values[12]
                inv_14.value = values[13]
                inv_15.value = values[14]
                inv_16.value = values[15]
                inv_17.value = values[16]
                inv_18.value = values[17]                                           
        if t1 >= last_entry:
            print(f"{datetime.datetime.now().time()}: Thread {thread_name} done playing {slot}")
            t0 = 0
            t1 = 0
            playing = False
            pir_sensor_active = False
            standard_mode = False
            break

def interaction():
    global stop_thread_pir, stop_thread_slow, interaction_stop
    global rec_dict_pir, rec_dict_slow, last_time_pir, last_time_slow, play_slow, play_pir
    global pir_sensor_active, pir_sensor, standard_mode
    # The loop that checks wether the pir sensor is active or not and starts, or kills, the corresponding threads    
    print("interaction has started")    
    print("standard_mode", standard_mode)
    print("pir_sensor_active", pir_sensor_active)
    print("pir_sensor", pir_sensor)
    while True:
        if interaction_stop:
            print(f"{datetime.datetime.now().time()}: Interaction thread is stopping")
            break
        if not standard_mode and not pir_sensor_active:
            standard_mode = True
            stop_thread_slow = False
            try:
                t_slow = threading.Thread(target = player, args=("t_slow", rec_dict_slow, last_time_slow, play_slow )) 
                t_slow.start()
            except:
                print("No slow composition is found. Playing the pir composition.") 
                try:
                    t_pir = threading.Thread(target = player, args=("t_pir", rec_dict_pir, last_time_pir, play_pir)) 
                    t_pir.start()
                except:
                    print("No pir composition is found either, please record a composition before starting this program.")
        if pir_sensor and not pir_sensor_active:
            pir_sensor_active = True
            print(f"{datetime.datetime.now().time()}: interaction thread and not pir_sensor_active pir_sensor:", pir_sensor)
            print(f"{datetime.datetime.now().time()}: Slow player is alive:  {t_slow.is_alive()}")
            if t_slow.is_alive():
                print(f"{datetime.datetime.now().time()}: Attempting to kill player slow")
                stop_thread_slow = True
                t_slow.join()
                if not t_slow.is_alive():
                    print(f"{datetime.datetime.now().time()}: Slow player thread is not alive")
                elif t_slow.is_alive():
                    print(f"{datetime.datetime.now().time()}: Error: slow player could not be killed. Not starting pir active thread.")
            if not t_slow.is_alive():
                print(f"{datetime.datetime.now().time()}: Slow player killed")
                standard_mode = False
                stop_thread_slow = False
                try:
                    t_pir = threading.Thread(target = player, args=("t_pir", rec_dict_pir, last_time_pir, play_pir)) 
                    t_pir.start()
                except:
                    print("no pir composition is found, playing the slow composition") 
                    try:
                        t_slow = threading.Thread(target = player, args=("t_slow", rec_dict_slow, last_time_slow, play_slow )) 
                        t_slow.start()
                    except:
                        print("No slow composition is found either. Please record a composition before starting the program.")

def stop_inv():
    global pi
    if pi:
        global inv_1, inv_2, inv_3, inv_4, inv_5, inv_6, inv_7, inv_8, inv_9, inv_11, inv_12, inv_13, inv_14, inv_15, inv_16, inv_17, inv_18
        inv_1.value = 0
        inv_2.value = 0
        inv_3.value = 0
        inv_4.value = 0
        inv_5.value = 0
        inv_6.value = 0    
        inv_7.value = 0
        inv_8.value = 0
        inv_9.value = 0
        inv_10.value = 0
        inv_11.value = 0
        inv_12.value = 0  
        inv_13.value = 0
        inv_14.value = 0
        inv_15.value = 0
        inv_16.value = 0
        inv_17.value = 0
        inv_18.value = 0
    print(f"{datetime.datetime.now().time()}: inverters stopped")
    return

def network_udp():
    global sock, addr, UDP_OUT_PORT
    global play_mode, play_mode_active, pir_sensor_active
    global path_settings
    global stop_thread_pir, stop_thread_slow, interaction_stop, standard_mode
    global pi
    if pi:
        global inv_1, inv_2, inv_3, inv_4, inv_5, inv_6, inv_7, inv_8, inv_9, inv_11, inv_12, inv_13, inv_14, inv_15, inv_16, inv_17, inv_18
    data = '' # empty var for incoming data
    rec = 0
    while True:
        data_raw, addr = sock.recvfrom(1024)
        data = data_raw.decode()    # My test message is encoded
        if DEBUG == 1 or DEBUG == 3:
            print(f"{CRED}{datetime.datetime.now().time()} UDP MESSAGE: {data}{CEND}")    
        if data:                                                        # only do something when there's data
            if data.startswith("status"):
                show_mode = "play_mode " + str(play_mode)
                sock.sendto((bytes(show_mode, "utf-8")), (addr[0], UDP_OUT_PORT))
            if data.startswith("SHOW"):                            # if the first part of the list starts with "rec"
                file_settings = open(path_settings, 'w')
                file_settings.write(data)    
                file_settings.close()
                standard_mode = False
                stop_thread_pir = False
                stop_thread_slow = False                
                interaction_stop = False
                play_mode_active = False
                pir_sensor_active = False                
                stop_inv() 
                play_mode = 2
                print("play_mode udp", play_mode)
            if data.startswith("EDIT"):
                file_settings = open(path_settings, 'w')
                file_settings.write(data)    
                file_settings.close()
                stop_thread_slow = True
                stop_thread_pir = True
                interaction_stop = True
                play_mode_active = False
                pir_sensor_active = False
                stop_inv() 
                play_mode = 1 
                print("play_mode udp", play_mode)
            if play_mode == 1:
                decode_list = data.split()                              # byte decode the incoming list and split in two
                if decode_list[0].startswith("REC") and rec == 0:                    # if the first part of the list starts with "rec"
                    print(decode_list[0],decode_list[1])                    # for debug purposes
                    y = []                                                  # the list that is used to store everything, empty or start it when this is called
                    if pi:
                        loc_file = "/home/pi/Desktop/whos_afraid/" + decode_list[1]
                    else:
                        loc_file = decode_list[1]
                    t0 = time.time()                                        # start the timer
                    f = open(loc_file, 'w')                           # open or new file with the chosen file in the Recorder Software
                    rec = 1
                    sock.sendto(bytes("REC", "utf-8"), (addr[0], UDP_OUT_PORT))
                elif decode_list[0].startswith("VALUES"):   # if the first part of the list starts with "VALUES"
                    if pi:
                        inv_1.value = float(decode_list[1])
                        inv_2.value = float(decode_list[2])
                        inv_3.value = float(decode_list[3])
                        inv_4.value = float(decode_list[4])
                        inv_5.value = float(decode_list[5])
                        inv_6.value = float(decode_list[6])    
                        inv_7.value = float(decode_list[7])
                        inv_8.value = float(decode_list[8])
                        inv_9.value = float(decode_list[9])
                        inv_10.value = float(decode_list[10])
                        inv_11.value = float(decode_list[11])
                        inv_12.value = float(decode_list[12])  
                        inv_13.value = float(decode_list[13])
                        inv_14.value = float(decode_list[14])
                        inv_15.value = float(decode_list[15])
                        inv_16.value = float(decode_list[16])
                        inv_17.value = float(decode_list[17])
                        inv_18.value = float(decode_list[18])  
                    if rec:
                        t1 = time.time() - t0
                        x = {                                                   # build a dict with the info from UDP
                            "time": round(t1, 3),
                            "values":[
                                    float(decode_list[1]),
                                    float(decode_list[2]),
                                    float(decode_list[3]),
                                    float(decode_list[4]),
                                    float(decode_list[5]),
                                    float(decode_list[6]),
                                    float(decode_list[7]),
                                    float(decode_list[8]),
                                    float(decode_list[9]),
                                    float(decode_list[10]),
                                    float(decode_list[11]),
                                    float(decode_list[12]),
                                    float(decode_list[13]),
                                    float(decode_list[14]),
                                    float(decode_list[15]),
                                    float(decode_list[16]),
                                    float(decode_list[17]),
                                    float(decode_list[18])                                                        
                                ]           
                            }
                        y.append(x)                                         # append the dict to the list 
                elif decode_list[0].startswith("ST_RC"):                 # if the list starts with "ST_RC"
                    print("RECEIVED STOP RECORDING ORDER")
                    rec = 0
                    try:    
                        json_dump = json.dumps(y, sort_keys=True, ensure_ascii=False) #transfer the list of dicts into a json format
                        f.write(json_dump)                                      # write it to the file opened in "rec"
                        f.close()                                               # close the file  
                        print("done writing file")                              
                        sock.sendto(bytes("load_mode 1", "utf-8"), (addr[0], UDP_OUT_PORT))
                        del y                                                   # double check to delete to free up memory
                        composition_load_pir()
                        composition_load_slow() 
                        sock.sendto(bytes("load_mode 0", "utf-8"), (addr[0], UDP_OUT_PORT))
                    except:
                        print("The recording has not started yet. Try again.")
                    stop_inv()   
                    sock.sendto(bytes("STOPPED RECORDING", "utf-8"), (addr[0], UDP_OUT_PORT))
                elif decode_list[0].startswith("STOP"):                 # if the list starts with "STOP"
                    stop_inv()
                    if rec:
                        rec = 0
                        try:    
                            json_dump = json.dumps(y, sort_keys=True, ensure_ascii=False) #transfer the list of dicts into a json format
                            f.write(json_dump)                                      # write it to the file opened in "rec"
                            f.close()                                               # close the file  
                            print("done writing file")                              
                            del y                                                   # double check to delete to free up memory
                            composition_load_pir()
                            composition_load_slow() 
                        except:
                            print("The recording has not started yet. Try again.")
                        stop_inv()   
                        sock.sendto(bytes("STOPPED RECORDING", "utf-8"), (addr[0], UDP_OUT_PORT))
try:
    network_udp_worker = threading.Thread(target=network_udp)
    network_udp_worker.start()
except:
    print (f"{datetime.datetime.now().time()}: Error: unable to start network_udp_worker thread. Exit.")
    quit()


# the function that will spawn as a thread continiously checking the pir sensor
def pir_input():
    global pi, pir_sensor, pir, addr, UDP_OUT_PORT
    print(f"{datetime.datetime.now().time()}: Detecting pir sensor")
    while True: 
        if pi:
            pir_sensor = pir.value 
            if pir_sensor and DEBUG == 1:
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



file_settings = open(path_settings, 'r')
all_char = file_settings.read(20) # read file
if all_char.startswith("EDIT"):
    print("record mode")
    play_mode = 1
elif all_char.startswith("SHOW"):
    print("play mode")
    play_mode = 2
file_settings.close()







while True:
    if play_mode == 2 and not play_mode_active: 
        play_mode_active = True
        edit_stop = True
        print("beginning play_mode")
        try:
            interaction_worker = threading.Thread(target=interaction)
            interaction_worker.start()
        except:
            print (f"{datetime.datetime.now().time()}: Error: unable to start INTERACTION thread. Exit.")
            quit()