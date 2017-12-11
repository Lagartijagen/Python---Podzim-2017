import sqlite3
import json
import sys
from pathlib import Path


def main():
    script = sys.argv[0]
    printNumber = sys.argv[1]
    #printNumber = input("Please enter print number: ")
    #printNumber = 0
    musicDict = {}

    sqlfile = Path("scorelib.dat")
    if sqlfile.is_file() == 1:
        conn = sqlite3.connect('scorelib.dat')
        cursor = conn.cursor()
    else:
        print("scorelib.dat is missing!")

    cursor.execute("select person.name from person "
                   "join score_author on person.id = score_author.composer "
                   "join edition on score_author.score = edition.score "
                   "join print on edition.id = print.edition where print.id = ? ", (printNumber,) )
    result = cursor.fetchall()
    if result != []:
        for row in result:
            musicDict.setdefault("Composer", []).append(row[0])
    else:
        print("no result")

    for k, v in musicDict.items():
        print(k, v)

    with open('getprint.json', 'w') as fp:
        print(json.dump(musicDict, fp))

if __name__ == '__main__':
    main()


