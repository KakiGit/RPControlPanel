
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
import struct

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


def sendMessage(client, message):
    msgLen = len(message)
    backMsgList = []
    backMsgList.append(struct.pack('B', 129))

    if msgLen <= 125:
        backMsgList.append(struct.pack('b', msgLen))
    elif msgLen <= 65535:
        backMsgList.append(struct.pack('b', 126))
        backMsgList.append(struct.pack('>h', msgLen))
    elif msgLen <= (2 ^ 64-1):
        backMsgList.append(struct.pack('b', 127))
        backMsgList.append(struct.pack('>h', msgLen))
    else:
        print("the message is too long to send in a time")
        return
    message_byte = bytes()
    print(type(backMsgList[0]))
    for c in backMsgList:
        message_byte += c
    message_byte += bytes(message, encoding="utf8")

    client.send(message_byte)


def socketServer():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", port))
    sock.listen(0)
    while True:
        client, cltadd = sock.accept()
        data = client.recv(1024)
        cltadd = cltadd
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
        multiprocessing.Process(target=systemPara, args=(client,)).start()
        global connection
        connection.value = True
        print("accept a connect from:", client.getpeername())


def receiveData(client):
    while True:
        data = client.recv(1024)
        if(data):
            tmp = parse_data(data)
            print(tmp, "from", client.getpeername())
            os.system(tmp)
        else:
            break

    global connection
    connection.value = False
    print("close:", client.getpeername())


def systemPara(client):
    global connection
    while connection.value:

        DISK_stats = linuxcmd.getDiskSpace()
        DISK_total = DISK_stats[0]
        DISK_used = DISK_stats[1]
        DISK_perc = DISK_stats[3]
        DISK_Avail = float(DISK_total.rstrip('G')) - \
            float(DISK_used.rstrip('G'))
        CPU_temp = linuxcmd.getCPUtemperature()
        CPU_usage = linuxcmd.getCPUuse()

        RAM_stats = linuxcmd.getRAMinfo()
        RAM_total = round(int(RAM_stats[0]) / 1000, 1)
        RAM_used = round(int(RAM_stats[1]) / 1000, 1)
        RAM_Avail = RAM_total - RAM_used
        RAM_Usage = round(RAM_used / RAM_total, 1)
        dataToBeSent = CPU_temp + ' ' + CPU_usage + ' ' + \
            str(RAM_Avail)+' '+str(RAM_Usage)+' ' + \
            str(DISK_Avail)+' '+str(DISK_perc)+' '
        if connection.value:
            sendMessage(client, dataToBeSent)


if __name__ == "__main__":
    connection.value = False
    serv = multiprocessing.Process(target=socketServer)
    serv.start()
# Now, you can use telnet to test it, the command is "telnet 127.0.0.1 9011"
# You also can use web broswer to test, input the address of "http://127.0.0.1:9011" and press Enter button
# Enjoy it....
