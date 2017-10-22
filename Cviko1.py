import re
from collections import Counter

f = open('scorelib.txt', 'r', encoding="utf8")
musicDict = {}

for line in f:
    parseData = re.match("([a-zA-Z ]*:) (.*)", line)

    if parseData != None:
        if parseData.group(2) == "":
            musicDict.setdefault(parseData.group(1), []).append("unknown")
        else:
            musicDict.setdefault(parseData.group(1), []).append(parseData.group(2))

countAllValues = {}
countOccurrences = {}

for key in musicDict:
    countAllValues[key] = (len(musicDict[key]))
    if key != "Print Number:":
        countOccurrences[key] = (Counter(musicDict[key]))

for key, val in musicDict.items():
    print(key, val)

print("\nNumber of occurrences for each value in all keys:")
for key in countOccurrences:
    print(key, countOccurrences[key])
print("\nNumber of all values in different keys:", countAllValues)


