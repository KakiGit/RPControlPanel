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


def file_name(file_dir):
    data = []
    for root, dirs, files in os.walk(file_dir):
        for dir in dirs:
            data.append({'folder', dir})
        for file in files:
            filePath = root+'/'+file
            fileStat = os.stat(filePath)
            time = time.strftime('%Y-%m-%d %H:%M:%S',
                                 time.localtime(fileStat.st_mtime))
            size = round(int(fileStat.st_size)/(1024*1024), 1)
            data.append({'file', file, time, size})


if __name__ == '__main__':

    file = open("/var/www/html/ajax/linuxcmd.txt", "w")
    file.write("")
    file.close()

    file = open("/var/www/html/ajax/connect.txt", "w")
    file.write("")
    file.close()
    count = 0
    while True:

        file = open("/var/www/html/ajax/connect.txt", "r")
        text = file.read()
        file.close()
        # Disk information
        count = count+1
        if(text != ""):
            count = 0
            print("Connecting ...")
            file = open("/var/www/html/ajax/connect.txt", "w")
            file.write("")
            file.close()

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

            DISK_stats = getDiskSpace()
            DISK_total = DISK_stats[0]
            DISK_used = DISK_stats[1]
            DISK_perc = DISK_stats[3]
            DISK_Avail = float(DISK_total.rstrip('G')) - \
                float(DISK_used.rstrip('G'))
            CPU_temp = getCPUtemperature()
            CPU_usage = getCPUuse()
            # RAM information
            # Output is in kb, here I convert it in Mb for readability
            RAM_stats = getRAMinfo()
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
        sleepTime = 1
        if(count > 60):
            sleepTime = 60
            print("I am going to sleep")
        time.sleep(sleepTime)
