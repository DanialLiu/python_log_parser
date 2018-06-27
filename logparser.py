import re

def matchDate(line):
    matchThis = ""
    matched = re.match(r'\d\d\d\d/\d\d/\d\d\ \d\d:\d\d:\d\d',line)
    if matched:
        #matches a date and adds it to matchThis            
        matchThis = matched.group() 
    else:
        matchThis = "NONE"
    return matchThis
def generateDicts(log_fh):
    currentDict = {}
    for line in log_fh:
        if line.startswith(matchDate(line)):
            if currentDict:
                yield currentDict
            print('line:' + line)
            i = line.find(']:')
            print('i:' + str(i))
            head = line[0:i]
            currentDict = {"date":head[:26], "text":line[i+3:]}
        else:
            if("text" in currentDict):
                currentDict["text"] += line
            else:
                currentDict["text"] = line
    yield currentDict

with open("log.log") as f:
    listNew= list(generateDicts(f))
    print(listNew)