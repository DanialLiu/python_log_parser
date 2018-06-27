import re

# def matchDate(line):
#     matchThis = ""
    
#     if matched:
#         #matches a date and adds it to matchThis            
#         matchThis = matched.group() 
#     else:
#         matchThis = "NONE"
#     return matchThis
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
            currentDict = {"date": matched.group(1), "level": matched.group(2), "tag": matched.group(3), "file": matched.group(4), "text": matched.group(5)}
        else:
            if("text" in currentDict):
                currentDict["text"] += line
            else:
                currentDict["text"] = line
    currentDict["text"] = currentDict["text"].strip()
    yield currentDict

with open("log.log") as f:
    logs= list(generateDicts(f))
    print("log lines:", len(logs))
    for l in logs:
        print(l)