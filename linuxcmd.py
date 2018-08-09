import os
import time

# Return CPU temperature as a character string


def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=", "").replace("'C\n", ""))

# Return RAM information (unit=kb) in a list
# Index 0: total RAM
# Index 1: used RAM
# Index 2: free RAM


def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            return(line.split()[1:4])

# Return % of CPU used by user as a character string


def getCPUuse():
    data = os.popen("top -bn2 | awk '/Cpu\(s\):/ {print $2}'")
    data.readline()
    return data.readline().strip()

# Return information about disk space as a list (unit included)
# Index 0: total disk space
# Index 1: used disk space
# Index 2: remaining disk space
# Index 3: percentage of disk used


def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            return(line.split()[1:5])


if __name__ == '__main__':
    file = open("/var/www/html/ajax/linuxcmd.txt", "w")
    file.write("")
    file.close()
    while True:
        # read cmd
        # CPU informatiom
        CPU_temp = getCPUtemperature()
        CPU_usage = getCPUuse()

        # RAM information
        # Output is in kb, here I convert it in Mb for readability
        RAM_stats = getRAMinfo()
        RAM_total = round(int(RAM_stats[0]) / 1000, 1)
        RAM_used = round(int(RAM_stats[1]) / 1000, 1)
        RAM_free = round(int(RAM_stats[2]) / 1000, 1)
        RAM_Avail = RAM_total - RAM_used
        RAM_Usage = round(RAM_used / RAM_total, 1)

        # Disk information
        DISK_stats = getDiskSpace()
        DISK_total = DISK_stats[0]
        DISK_used = DISK_stats[1]
        DISK_perc = DISK_stats[3]
        DISK_Avail = float(DISK_total.rstrip('G')) - \
            float(DISK_used.rstrip('G'))

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

        with open("/var/www/html/ajax/pistats.txt", "w") as f:
            # f.write(CPU_temp)
            f.write(CPU_temp+'\n')
            f.write(CPU_usage+'\n')
            f.write(str(RAM_Avail)+'\n')
            f.write(str(RAM_Usage)+'\n')
            f.write(str(DISK_Avail)+'\n')
            f.write(str(DISK_perc)+'\n')
            f.close()
        
        time.sleep(2)
