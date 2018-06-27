import time
def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

if __name__ == '__main__':
    logfile = open("tmp.log","r")
    for line in logfile.readlines():
        print(line.strip('\r\n'))
    loglines = follow(logfile)
    for line in loglines:
        print(line.strip('\r\n'))