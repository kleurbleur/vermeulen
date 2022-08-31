import socket
import time
import json

# UDP_IP = "192.168.178.54"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET,                        # Internet
                     socket.SOCK_DGRAM,                     # Setup Socket
                     socket.IPPROTO_UDP)                    # Setup UDP
sock.bind(('', UDP_PORT))

y = []
rec = 0

while True:
    data, addr = sock.recvfrom(1024)                        # buffer size is 1024 bytes
    # print(repr(data))                                     # for debug purposes
    decode_list = data.decode().split()                     # byte decode the incoming list and split in two
    if decode_list[0].startswith("REC"):                    # if the first part of the list starts with "rec"
        print(decode_list[0],decode_list[1])                    # for debug purposes
        t0 = time.time()                                        # start the timer
        f = open(decode_list[1], 'w')                           # open or new file with the chosen file in the Max4Live patch
        rec = 1
    elif decode_list[0].startswith("BOARD") and rec == 1:   # if the first part of the list starts with "board"
        t1 = time.time() - t0                                   # see how much time elapsed since the beginning of rec
        udp_value = int(decode_list[1])
        if udp_value >= 1:                                  # if the incoming value really represents an input
            print(round(t1, 3), decode_list[0],decode_list[1])                # for debug purposes
            x = {                                                   # build a dict with the info from UDP
                "time": round(t1, 3) ,
                "values": {
                    "port": decode_list[0], 
                    "value": udp_value
                    }
                }
            y.append(x)                                             # append the dict to the list 
    elif decode_list[0].startswith("stop"):                 # if the list starts with "stop"
        json_dump = json.dumps(y, sort_keys=True, ensure_ascii=False) #transfer the list of dicts into a json format
        f.write(json_dump)                                      # write it to the file opened in "rec"
        f.close()                                               # close the file
        rec = 0
        print(decode_list[0],decode_list[1])                    # debug purposes
    elif decode_list[0].startswith("exit"):                 # if the list starts with "exit"
        sock.close()                                            # close the socket
        exit()                                                  # exit the program
        

