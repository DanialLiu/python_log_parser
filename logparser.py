import re

# def matchDate(line):
#     matchThis = ""
    
#     if matched:
#         #matches a date and adds it to matchThis            
#         matchThis = matched.group() 
#     else:
#         matchThis = "NONE"
#     return matchThis
levelToNum = {'VERBOSE':0, 'DEBUG':100, 'INFO':200, 'WARNING':300, 'ERROR':400, 'FATAL':500}

def generateDicts(log_fh):
    currentDict = {}
    for line in log_fh:
        matched = re.match(r'(\d{4}/\d\d/\d\d\ \d\d:\d\d:\d\d \d{6}) (\w+)/(\w+)\[(.*?)\]: (.*)', line)
        if matched:            
            if currentDict:
                currentDict["text"] = currentDict["text"].strip()
                yield currentDict
            print('line:' + line)
            i = line.find(']:')
            print('i:' + str(i))
            head = line[0:i]
            level = matched.group(2)
            level_num = 0
            if level in levelToNum:
                level_num = levelToNum[level]
            currentDict = {"date": matched.group(1), "level": level, 'level_num': level_num, "tag": matched.group(3), "file": matched.group(4), "text": matched.group(5)}
            
        else:
            if("text" in currentDict):
                currentDict["text"] += line
            else:
                currentDict['level_num'] = 0
                currentDict["text"] = line
    currentDict["text"] = currentDict["text"].strip()
    yield currentDict

def readlog(file):
    with open(file) as f:
        logs= list(generateDicts(f))
        return logs
if __name__ == '__main__':
    logs = readlog("log.log")
    print("log lines:", len(logs))
    for l in logs:
        print(l)