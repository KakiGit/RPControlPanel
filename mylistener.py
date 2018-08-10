
# Filename: PortListner.py
# @author: RobinTang
# Created on 2012-9-5 1:42:05

import threading
import socket
import hashlib
import base64
import multiprocessing
import os
import linuxcmd
import time
from multiprocessing import Value, Array

encoding = 'utf-8'
BUFSIZE = 1024
port = 9011
headers = {}

connection = Value('b', False)


def parse_data(msg):
    v = msg[1] & 0x7f
    if v == 0x7e:
        p = 4
    elif v == 0x7f:
        p = 10
    else:
        p = 2
    mask = msg[p:p+4]
    data = msg[p+4:]
    return ''.join([chr(v ^ mask[k % 4]) for k, v in enumerate(data)])


def socketServer():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", port))
    sock.listen(0)
    while True:
        client, cltadd = sock.accept()
        data = client.recv(1024)
        header, sub = data.split(str("\r\n\r\n").encode(encoding), 1)
        for line in header.split(str('\r\n').encode(encoding))[1:]:
            key, value = line.split(str(': ').encode(encoding), 1)
            headers[key] = value
        key = (bytes.decode(headers[str('Sec-WebSocket-Key').encode(encoding)],
                            encoding) + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode(encoding)
        ser_key = hashlib.sha1(key).digest()
        token = base64.b64encode(ser_key)
        client.send(('\
HTTP/1.1 101 WebSocket Protocol Hybi-10\r\n\
Upgrade: WebSocket\r\n\
Connection: Upgrade\r\n\
Sec-WebSocket-Accept: {}\r\n\r\n\
'.format(bytes.decode(token, encoding))).encode(encoding))
        multiprocessing.Process(target=receiveData, args=(client,)).start()
        global connection
        connection.value = True
        print("accept a connect from:", client.getpeername())


def receiveData(client):
    while True:
        data = client.recv(1024)
        if(data):
            tmp = parse_data(data)
            print(tmp, "from", client.getpeername())
        else:
            break

    global connection
    connection.value = False
    print("close:", client.getpeername())


def systemPara():
    global connection
    while True:
        if connection.value:

            file = open("/var/www/html/ajax/linuxcmd.txt", "r")
            text = file.read()
            file.close()

            if(text != ""):
                    # clear cmd
                file = open("/var/www/html/ajax/linuxcmd.txt", "w")
                file.write("")
                file.close()
                # print(text)
                os.system(text)

            DISK_stats = linuxcmd.getDiskSpace()
            DISK_total = DISK_stats[0]
            DISK_used = DISK_stats[1]
            DISK_perc = DISK_stats[3]
            DISK_Avail = float(DISK_total.rstrip('G')) - \
                float(DISK_used.rstrip('G'))
            CPU_temp = linuxcmd.getCPUtemperature()
            CPU_usage = linuxcmd.getCPUuse()
            # RAM information
            # Output is in kb, here I convert it in Mb for readability
            RAM_stats = linuxcmd.getRAMinfo()
            RAM_total = round(int(RAM_stats[0]) / 1000, 1)
            RAM_used = round(int(RAM_stats[1]) / 1000, 1)
            RAM_Avail = RAM_total - RAM_used
            RAM_Usage = round(RAM_used / RAM_total, 1)

            with open("/var/www/html/ajax/pistats.txt", "w") as f:
                # f.write(CPU_temp)
                f.write(CPU_temp+'\n')
                f.write(CPU_usage+'\n')
                f.write(str(RAM_Avail)+'\n')
                f.write(str(RAM_Usage)+'\n')
                f.write(str(DISK_Avail)+'\n')
                f.write(str(DISK_perc)+'\n')
                f.close()
        time.sleep(1)


if __name__ == "__main__":
    connection.value = False
    file = open("/var/www/html/ajax/linuxcmd.txt", "w")
    file.write("")
    file.close()
    serv = multiprocessing.Process(target=socketServer)
    serv.start()

    sys = multiprocessing.Process(target=systemPara)
    sys.start()

# Now, you can use telnet to test it, the command is "telnet 127.0.0.1 9011"
# You also can use web broswer to test, input the address of "http://127.0.0.1:9011" and press Enter button
# Enjoy it....
